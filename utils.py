import logging
import os
import pandas as pd
from uszipcode import SearchEngine

search = SearchEngine(simple_zipcode=True)


def write_output_file(df, filename, sheet_name="codefornola cleaned"):
    if filename.startswith("data") and not os.path.exists("data"):
        logging.debug("Creating data directory")
        os.makedirs("data")
    logging.debug(f"Writing sheet '{sheet_name}' into '{filename}'")
    df.to_excel(filename)


def get_lat(zipcode):
    if pd.isnull(zipcode):
        return None
    else:
        lat = search.by_zipcode(int(zipcode)).lat
        return lat if lat else None


def get_lng(zipcode):
    if pd.isnull(zipcode):
        return None
    else:
        lng = search.by_zipcode(int(zipcode)).lng
        return lng if lng else None


def explode_needs(df, need_column):
    logging.debug(f"exploding needs into {need_column}")
    df["tmp_needs"] = df[need_column].str.split(";")
    df = df.explode("tmp_needs")
    df.drop(columns=[need_column], inplace=True)
    df.rename(columns={"tmp_needs": need_column}, inplace=True)
    return df


replacements = {
    "†": "For some reason this cross mark is showing up in some of the entries, so just removing it",
    "Employment": "Employment Services",
    "Food": "Food/Meals",
    "Food/Meal": "Food/Meals",
    "I'm Sick (what next?)": "I'm Sick (What's Next?)",
    "I'm Sick (Whats Next?)": "I'm Sick (What's Next?)",
    "Income support/assistance": "Income Support/Assistance",
    "information only call": "",
    "Inquires about Health Complications / Concerns": "Inquires about Health Complications",
    "International Travel Concerns": "International / General Travel Concerns",
    "Legal Consumer": "Legal Assistance",
    "Other - Interpersonal": "Other",
    "Other (PLEASE Specify Caller Need in Call Notes)": "Other",
    "other 2-1-1 referral": "Other",
    "Unemployment": "Unemployment Benefits",
}
