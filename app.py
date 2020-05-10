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
    render_template,
    send_from_directory,
)
from werkzeug.utils import secure_filename

from cleanup_keep_calm_with_covid import (
    cleanup as cleanup_keep_calm_with_covid,
    CONVERTERS,
)
from cleanup_all_covid_calls import cleanup as cleanup_all_covid_calls

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
        if request.files is not None and request.form["script_name"]:
            return process_files(request.form["script_name"], request.files)
    return render_template("index.html")


def process_files(script_name, files):
    # this could be a good use case for the strategy pattern
    if script_name == "keep_calm_with_covid":
        if "file1" not in files:
            print("did not have required files")
            return redirect(request.url)
        file = request.files["file1"]
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
            return send_from_directory(
                app.config["DOWNLOADS_DIR"], output_filename, as_attachment=True
            )
    if script_name == "all_covid":
        if "file1" not in files or "file2" not in files:
            print("did not have required files")
            return redirect(request.url)
        file1 = request.files["file1"]
        file2 = request.files["file2"]
        if file1.filename == "" or file2.filename == "":
            print("invalid filename")
            return redirect(request.url)
        dfs = {}
        dfvl = pd.read_csv(file1, encoding="ISO-8859-1")
        dfvl = remove_first_rows(dfvl)
        dfs["VIALINK"] = dfvl
        df232 = pd.read_csv(file2, encoding="ISO-8859-1")
        df232 = remove_first_rows(df232)
        dfs["TWO32"] = df232
        logging.info("Cleaning data for All COVID Calls Dashboard")
        df = cleanup_all_covid_calls(dfs)
        output_filename = f"all_covid_cleaned.xlsx"
        download_filename = os.path.join(app.config["DOWNLOADS_DIR"], output_filename)
        logging.info(
            f"Writing data for All COVID Calls Dashboard to '{download_filename}'"
        )
        write_output_file(df, download_filename)
        return send_from_directory(
            app.config["DOWNLOADS_DIR"], output_filename, as_attachment=True
        )


if __name__ == "__main__":
    for directory in [UPLOADS_DIR, DOWNLOADS_DIR]:
        if not os.path.exists(directory):
            print(f"creating {directory}")
            os.makedirs(directory)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
