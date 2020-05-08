import os
from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    render_template,
    send_from_directory,
)
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "/tmp/uploads/"
DOWNLOAD_FOLDER = "tmp/downloads/"
ALLOWED_EXTENSIONS = {"csv", "CSV"}

app = Flask(__name__, static_url_path="/public", template_folder="public")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER

# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/#improving-uploads
# limit upload size upto 10MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            process_file(os.path.join(app.config["UPLOAD_FOLDER"], filename), filename)
            return redirect(url_for("uploaded_file", filename=filename))
    return render_template("index.html")


def process_file(input_path, output_filename):
    print("processing file")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["DOWNLOAD_FOLDER"], filename, as_attachment=True
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
