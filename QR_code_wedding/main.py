from flask import Flask, request, render_template, session, send_file, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv
from io import BytesIO
import requests
from zipfile import ZipFile
from PIL import Image
from pillow_heif import register_heif_opener
import io
from werkzeug.exceptions import RequestEntityTooLarge

load_dotenv()
register_heif_opener()

CLOUDINARY_NAME = os.getenv("CLOUDINARY_NAME")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
SESSION_KEY = os.getenv("SESSION_KEY")

app = Flask(__name__)
app.secret_key = SESSION_KEY
app.config['MAX_CONTENT_LENGTH'] = 600 * 1024 * 1024

MAX_VIDEO = 100 * 1024 * 1024
MAX_FILES = 50

ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/heic', 'image/heif'}
ALLOWED_VIDEO_TYPES = {'video/mp4', 'video/quicktime', 'video/x-m4v'}
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.heic', '.heif', '.mp4', '.mov', '.m4v'}

cloudinary.config(
    cloud_name=CLOUDINARY_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)

@app.errorhandler(RequestEntityTooLarge)
def handle_too_large(e):
    if session.get("language") == "it":
        msg = "Il file è troppo grande. Il limite totale è 600MB per invio."
    else:
        msg = "El archivo es demasiado grande. El límite total es 600MB por envío."
    return jsonify({'error': msg}), 413

@app.route("/", methods=["GET"])
def index():
    language = session.get('language')

    # Load first 10 photos from Cloudinary
    result = cloudinary.api.resources(
        type="upload",
        prefix="wedding-photos",
        max_results=10
    )
    urls = [res["secure_url"] for res in result.get("resources", [])]

    return render_template("index.html", photos=urls, language=language)

@app.route("/upload", methods=['POST'])
def upload():
    files = request.files.getlist("file")

    if not files:
        return jsonify({'error': 'No files uploaded'}), 400

    if len(files) > MAX_FILES:
        return jsonify({'error': f'Too many files. Maximum is {MAX_FILES}.'}), 400

    for file in files:
        if file.filename == "":
            continue

        try:
            mimetype = file.mimetype or ""
            ext = os.path.splitext(file.filename.lower())[1]

            # Validate file type
            if mimetype not in ALLOWED_IMAGE_TYPES and mimetype not in ALLOWED_VIDEO_TYPES \
               and ext not in ALLOWED_EXTENSIONS:
                return jsonify({'error': f'Unsupported file type: {file.filename}'}), 400

            # Get file size
            file.seek(0, 2)
            size = file.tell()
            file.seek(0)

            # VIDEO
            if mimetype.startswith("video") or ext in {'.mp4', '.mov', '.m4v'}:
                if size > MAX_VIDEO:
                    return jsonify({'error': f'{file.filename} is too large. Maximum is 100MB.'}), 400
                print(f"Uploading video: {file.filename}, size={size}")
                cloudinary.uploader.upload_large(
                    file.stream,
                    resource_type="video",
                    folder="wedding-photos",
                    chunk_size=6_000_000,
                    timeout=600,
                    secure=True
                )

            # HEIC/HEIF — convert to JPEG first
            elif ext in {'.heic', '.heif'} or mimetype in {'image/heic', 'image/heif'}:
                print(f"Converting HEIC image: {file.filename}")
                img = Image.open(file.stream)
                output = io.BytesIO()
                img.convert("RGB").save(output, format="JPEG", quality=85)
                output.seek(0)
                cloudinary.uploader.upload(
                    output,
                    resource_type="image",
                    folder="wedding-photos",
                    secure=True
                )

            # IMAGE
            else:
                print(f"Uploading image: {file.filename}, size={size}")
                cloudinary.uploader.upload(
                    file.stream,
                    resource_type="image",
                    folder="wedding-photos",
                    secure=True
                )

        except Exception as e:
            print(f"Upload error for {file.filename}: {e}")
            return jsonify({'error': str(e)}), 500

    return jsonify({'success': True}), 200

@app.route("/gallery", methods=["GET"])
def gallery():
    language = session.get("language")
    cursor = request.args.get("cursor")

    items = []

    # ---------- IMAGES ----------
    img_result = cloudinary.api.resources(
        resource_type="image",
        type="upload",
        prefix="wedding-photos",
        max_results=10,
        next_cursor=cursor
    )

    for res in img_result.get("resources", []):
        items.append({
            "url": res["secure_url"],
            "type": "image"
        })

    next_cursor = img_result.get("next_cursor") or ""

    # ---------- VIDEOS (only first load) ----------
    if not cursor:
        next_vid_cursor = None
        all_videos = []

        while True:
            vid_result = cloudinary.api.resources(
                resource_type="video",
                type="upload",
                prefix="wedding-photos",
                max_results=500,
                next_cursor=next_vid_cursor
            )

            for res in vid_result.get("resources", []):
                all_videos.append({
                    "url": res["secure_url"],
                    "type": "video"
                })

            next_vid_cursor = vid_result.get("next_cursor")
            if not next_vid_cursor:
                break  # no more videos

        # Insert videos first
        for video in reversed(all_videos):  # reverse to keep newest first
            items.insert(0, video)

    # ---------- AJAX ----------
    if request.args.get("ajax"):
        return jsonify({
            "urls": items,
            "next_cursor": next_cursor
        })

    # ---------- FIRST PAGE ----------
    return render_template(
        "gallery.html",
        gallery_pics=items,
        next_cursor=next_cursor,
        language=language
    )

@app.route("/download")
def download_image():
    url = request.args.get("url")
    if not url:
        return "No URL provided", 400

    # Fetch the image from the external server
    resp = requests.get(url)
    if resp.status_code != 200:
        return "Image not found", 404

    # Wrap image in BytesIO so Flask can send it
    img_bytes = BytesIO(resp.content)

    # Extract filename from URL
    filename = url.split("/")[-1].split("?")[0]

    # Send the file with attachment headers
    return send_file(
        img_bytes,
        download_name=filename,
        as_attachment=True
    )

@app.route("/download_multiple")
def download_multiple():
    # urls comes as ?url=url1&url=url2...
    urls = request.args.getlist("url")
    if not urls:
        return "No images selected", 400

    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, "w") as zipf:
        for url in urls:
            r = requests.get(url)
            if r.status_code == 200:
                filename = url.split("/")[-1].split("?")[0] or "photo.jpg"
                zipf.writestr(filename, r.content)

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        download_name="selected_photos.zip",
        as_attachment=True,
        mimetype="application/zip"
    )

@app.route("/it",  methods=["GET"])
def italiano():
    session['language'] = 'it'
    # Load first 10 photos from Cloudinary
    result = cloudinary.api.resources(
        type="upload",
        prefix="wedding-photos",
        max_results=10
    )
    urls = [res["secure_url"] for res in result.get("resources", [])]
    return render_template("index.it.html", photos=urls)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)




