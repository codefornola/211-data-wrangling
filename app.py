import logging
import os

import pandas as pd

from utils import remove_first_rows, write_output_file

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)
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

from cleanup_keep_calm_with_covid import (
    cleanup as cleanup_keep_calm_with_covid,
    CONVERTERS,
)

UPLOADS_DIR = "/tmp/uploads/"
DOWNLOADS_DIR = "/tmp/downloads/"
ALLOWED_EXTENSIONS = {"csv"}

app = Flask(__name__, static_url_path="/public", template_folder="public")
app.config["UPLOADS_DIR"] = UPLOADS_DIR
app.config["DOWNLOADS_DIR"] = DOWNLOADS_DIR

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
            uploaded_filename = os.path.join(app.config["UPLOADS_DIR"], filename)
            file.save(uploaded_filename)
            output_filename = f"{filename.rsplit('.', 1)[0]}_cleaned.xlsx"
            download_filename = os.path.join(
                app.config["DOWNLOADS_DIR"], output_filename
            )
            process_file(request.form["script_name"], uploaded_filename, download_filename)
            return send_from_directory(
                app.config["DOWNLOADS_DIR"], output_filename, as_attachment=True
            )
    return render_template("index.html")


def process_file(script_name, uploaded_filename, download_filename):
    print(
        f"processing file from {uploaded_filename} and writing to {download_filename}"
    )
    # this could be a good use case for the strategy pattern
    if script_name == "keep_calm_with_covid":
        df = pd.read_csv(
            uploaded_filename, encoding="ISO-8859-1", converters=CONVERTERS
        )
        df = remove_first_rows(df)
        logging.info("Cleaning data for Keep Calm with COVID Dashboard")
        df = cleanup_keep_calm_with_covid(df)
        logging.info(
            f"Writing data for Keep Calm with COVID Dashboard to '{download_filename}'"
        )
        write_output_file(df, download_filename)
    else:
        print("not implemented")


if __name__ == "__main__":
    for directory in [UPLOADS_DIR, DOWNLOADS_DIR]:
        if not os.path.exists(directory):
            print(f"creating {directory}")
            os.makedirs(directory)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
