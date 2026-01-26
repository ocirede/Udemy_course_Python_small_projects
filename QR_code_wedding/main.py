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
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024


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
    uploaded_urls = []

    for file in files:
        if file.filename == "":
            continue
        try:
            result = cloudinary.uploader.upload(file, folder="wedding-photos")
            uploaded_urls.append(result["secure_url"])
        except Exception as e:
            print(f"Upload error: {e}")
            return jsonify({'error': str(e)}), 500

    return '', 204



@app.route("/gallery", methods=["GET"])
def gallery():
    language = session.get('language')
    cursor = request.args.get("cursor")
    result = cloudinary.api.resources(
        type="upload",
        prefix="wedding-photos",
        max_results=10,
        next_cursor=cursor
    )

    urls = [res["secure_url"] for res in result.get("resources", [])]
    next_cursor = result.get("next_cursor")

    if not urls or not next_cursor:
        next_cursor = ""

    if request.args.get("ajax"):
        return jsonify({
            "urls": urls,
            "next_cursor": next_cursor
        })

    return render_template(
        "gallery.html",
        gallery_pics=urls,
        next_cursor=next_cursor,
        language= language
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

@app.route("/it")
def italiano():
    session['language'] = 'it'
    return render_template("index.it.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)



