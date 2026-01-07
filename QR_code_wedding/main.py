from flask import Flask, request, redirect, render_template
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv

load_dotenv()

CLOUDINARY_NAME = os.getenv("CLOUDINARY_NAME")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

app = Flask(__name__)

cloudinary.config(
    cloud_name= CLOUDINARY_NAME,
    api_key= API_KEY,
    api_secret= API_SECRET
)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("file")

    uploaded_urls = []

    for file in files:
        if file.filename == "":
            continue
        result = cloudinary.uploader.upload(file, folder="wedding-photos")
        uploaded_urls.append(result["secure_url"])

    return """
        <h3>Thank you for uploading ❤️</h3>
        <p>Redirecting to home...</p>
        <script>
            setTimeout(function(){
                window.location.href = "/";
            }, 3000);
        </script>
        """

@app.route("/gallery", methods=["GET"])
def gallery():
    result = cloudinary.api.resources(
        type="upload",
        prefix= "wedding-photos",
        max_results=2000
    )
    resources = result.get("resources", [])
    urls = [res["secure_url"] for res in resources]
    gallery_pics = "".join(
        f"<a href='{url}' target='_blank'><img src='{url}' width='200' style='margin:10px' /></a>"
        for url in urls
    )
    return render_template("gallery.html", gallery_pics = gallery_pics)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)