from flask import Flask, request, redirect, render_template, session, url_for, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv

load_dotenv()

CLOUDINARY_NAME = os.getenv("CLOUDINARY_NAME")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
SESSION_KEY = os.getenv("SESSION_KEY")

app = Flask(__name__)
app.secret_key = SESSION_KEY

cloudinary.config(
    cloud_name=CLOUDINARY_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)


@app.route("/", methods=["GET"])
def index():
    session.pop('language', None)
    return render_template("index.html")


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        files = request.files.getlist("file")
        uploaded_urls = []

        for file in files:
            if file.filename == "":
                continue
            result = cloudinary.uploader.upload(file, folder="wedding-photos")
            uploaded_urls.append(result["secure_url"])

        # Check language AFTER processing files
        language = session.get('language')

        if language == 'it':
            return render_template("upload.it.html")

        return render_template("upload.html")
    # For GET requests
    if session.get('language') == 'it':
        return render_template("upload.it.html")

    return render_template("upload.html")


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
        next_cursor = None

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


@app.route("/it")
def italiano():
    session['language'] = 'it'
    return render_template("index.it.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)