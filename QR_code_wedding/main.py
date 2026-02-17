from flask import Flask, request, render_template, session, send_file, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv
from io import BytesIO
import requests
from zipfile import ZipFile

load_dotenv()

CLOUDINARY_NAME = os.getenv("CLOUDINARY_NAME")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
SESSION_KEY = os.getenv("SESSION_KEY")

app = Flask(__name__)
app.secret_key = SESSION_KEY
app.config['MAX_CONTENT_LENGTH'] = 600 * 1024 * 1024


cloudinary.config(
    cloud_name=CLOUDINARY_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)


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

    for file in files:
        if file.filename == "":
            continue

        try:
            mimetype = file.mimetype or ""

            # VIDEO
            if mimetype.startswith("video"):
                cloudinary.uploader.upload_large(
                    file.stream,          # ✅ FIX
                    resource_type="video",
                    folder="wedding-photos",
                    chunk_size=6000000
                )

            # IMAGE
            else:
                cloudinary.uploader.upload(
                    file.stream,          # ✅ FIX
                    resource_type="image",
                    folder="wedding-photos"
                )

        except Exception as e:
            print("Upload error:", e)
            return jsonify({'error': str(e)}), 500

    return '', 204

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
                max_results=500,  # maximum allowed per request
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




