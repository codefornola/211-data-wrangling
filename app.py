from datetime import date
import logging

import pandas as pd

from constants import VIALINK_DISASTER_KEY, VIALINK_CALLS_KEY, TWO32_HELP_CALLS_KEY
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
    request,
    redirect,
    render_template,
    send_from_directory,
)

from cleanup_keep_calm_with_covid import (
    cleanup as cleanup_keep_calm_with_covid,
)
from cleanup_all_covid_calls import cleanup as cleanup_all_covid_calls

UPLOADS_DIR = "/tmp/uploads/"
DOWNLOADS_DIR = "/tmp/downloads/"
ALLOWED_EXTENSIONS = {"csv"}
DEFAULT_ENCODING = "ISO-8859-1"

app = Flask(__name__, static_url_path="/public", template_folder="public")
app.config["UPLOADS_DIR"] = UPLOADS_DIR
app.config["DOWNLOADS_DIR"] = DOWNLOADS_DIR

# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/#improving-uploads
# limit upload size upto 50MB
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.files is not None and request.form["script_name"]:
            return process_files(request.form["script_name"], request.files)
    return render_template("index.html")


def process_files(script_name, files):
    vialink_disaster = files["vialink_disaster"]
    file2 = files["file2"]
    if not (is_valid(vialink_disaster) and is_valid(file2)):
        logging.warning("invalid filename")
        return redirect(request.url)
    logging.info(f"Processing {script_name}")
    output_filename = f"{script_name}_cleaned_{date.today().strftime('%Y%m%d')}.xlsx"
    if script_name == "keep_calm_with_covid":
        dfs = files_to_dfs(script_name, vialink_disaster, file2)
        logging.info("Cleaning data for Keep Calm with COVID Dashboard")
        df = cleanup_keep_calm_with_covid(dfs)
        download_filename = os.path.join(app.config["DOWNLOADS_DIR"], output_filename)
        logging.info(
            f"Writing data for Keep Calm with COVID Dashboard to '{download_filename}'"
        )
        write_output_file(df, download_filename)
        return send_from_directory(
            app.config["DOWNLOADS_DIR"], output_filename, as_attachment=True
        )
    if script_name == "all_covid":
        dfs = files_to_dfs(script_name, vialink_disaster, file2)
        logging.info("Cleaning data for All COVID Calls Dashboard")
        df = cleanup_all_covid_calls(dfs)
        download_filename = os.path.join(app.config["DOWNLOADS_DIR"], output_filename)
        logging.info(
            f"Writing data for All COVID Calls Dashboard to '{download_filename}'"
        )
        write_output_file(df, download_filename)
        return send_from_directory(
            app.config["DOWNLOADS_DIR"], output_filename, as_attachment=True
        )


def files_to_dfs(script_name, vialink_disaster, file2):
    dfs = {}
    dfs[VIALINK_DISASTER_KEY] = csv_to_df(vialink_disaster)
    if script_name == "all_covid":
        dfs[TWO32_HELP_CALLS_KEY] = csv_to_df(file2)
    else:
        dfs[VIALINK_CALLS_KEY] = csv_to_df(file2)
    return dfs


def csv_to_df(file):
    df = pd.read_csv(file, encoding=DEFAULT_ENCODING)
    df = remove_first_rows(df)
    return df


def is_valid(file):
    return file is not None and file.filename != "" and allowed_file(file.filename)


@app.before_first_request
def create_dirs():
    for directory in [UPLOADS_DIR, DOWNLOADS_DIR]:
        if not os.path.exists(directory):
            logging.info(f"creating {directory}")
            os.makedirs(directory)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    create_dirs()
    app.run(host="0.0.0.0", port=port)
