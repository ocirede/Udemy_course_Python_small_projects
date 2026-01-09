from flask import Flask, request, redirect, render_template, session, url_for
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
    session.pop('language', None)  # Clear session when visiting root
    return render_template("index.html")




@app.route("/upload", methods=['GET', 'POST'])
def upload():
    print(f"Upload route - Session language: {session.get('language')}")

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
        print(f"After upload - Language in session: {language}")

        if language == 'it':
            print("Returning Italian upload page")
            return render_template("upload.it.html")

        print("Returning Spanish upload page")
        return render_template("upload.html")

    # For GET requests
    if session.get('language') == 'it':
        return render_template("upload.it.html")

    return render_template("upload.html")


@app.route("/gallery", methods=["GET"])
def gallery():
    next_cursor = None
    all_urls = []

    while True:
        result = cloudinary.api.resources(
            type="upload",
            prefix="wedding-photos",
            max_results=500,
            next_cursor=next_cursor
        )
        resources = result.get("resources", [])
        urls = [res["secure_url"] for res in resources]
        all_urls.extend(urls)

        next_cursor = result["next_cursor"] if "next_cursor" in result else None
        if not next_cursor:
            break

    return render_template("gallery.html", gallery_pics=all_urls)


@app.route("/it")
def italiano():
    session['language'] = 'it'
    return render_template("index.it.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)