import pandas as pd
from uszipcode import SearchEngine
import numpy as np
from datetime import datetime

file = "Data from 4.2.20 Fake Data.xlsx"

# read all sheets, returns a dict of dataframes
dfs = pd.read_excel(file, sheet_name=None)


### Cleanup for Keeping Calm with COVID dashboard
converters = {
    "Concerns/Needs  - Disaster Services ": str,
    "Concerns/Needs  - Domestic Abuse/IPV": str,
    "Concerns/Needs  - Early Childhood Education ": str,
    "Concerns/Needs  - Education/ Employment ": str,
    "Concerns/Needs  - Environmental Quality & Prtcn ": str,
    "Concerns/Needs  - Health Care ": str,
    "Concerns/Needs  - Interpersonal": str,
    "Concerns/Needs  - Mental Health": str,
    "Concerns/Needs  - Mental Health Concerns": str,
    "Concerns/Needs  - Organizational Development": str,
    "Concerns/Needs  - Other ": str,
    "Concerns/Needs  - Other Community Services": str,
    "Concerns/Needs  - Protective Service/Abuse": str,
    "Concerns/Needs  - Public Asst & Social Insurance": str,
    "Concerns/Needs  - Relationship Concerns / Issues ": str,
    "Concerns/Needs  - Self-Harm": str,
    "Concerns/Needs  - Sexuality": str,
}
df = pd.read_excel(
    file, sheet_name="Uncleaned data type 2 VIA LINK", converters=converters
)


# step 1
# pretty sure the call reports form is "Uncleaned data type 2 VIA LINK"

# todo: why not use all conerns/needs?  why only DD-DT?
# needs_columns = [c for c in dfs["Uncleaned data type 2 VIA LINK"] if c.startswith("Concerns/Needs")]
needs_columns = [
    # "Concerns/Needs  - N/A - must list WHY",
    # "Concerns/Needs  - Addictive Disorders",
    # "Concerns/Needs  - Arts & Culture ",
    # "Concerns/Needs  - Basic Needs ",
    # "Concerns/Needs  - Campus Information",
    # "Concerns/Needs  - Consumer Services ",
    # "Concerns/Needs  - Criminal Justice & Legal Srvcs ",
    "Concerns/Needs  - Disaster Services ",
    "Concerns/Needs  - Domestic Abuse/IPV",
    "Concerns/Needs  - Early Childhood Education ",
    "Concerns/Needs  - Education/ Employment ",
    "Concerns/Needs  - Environmental Quality & Prtcn ",
    "Concerns/Needs  - Health Care ",
    "Concerns/Needs  - Interpersonal",
    "Concerns/Needs  - Mental Health",
    "Concerns/Needs  - Mental Health Concerns",
    "Concerns/Needs  - Organizational Development",
    "Concerns/Needs  - Other ",
    "Concerns/Needs  - Other Community Services",
    "Concerns/Needs  - Protective Service/Abuse",
    "Concerns/Needs  - Public Asst & Social Insurance",
    "Concerns/Needs  - Relationship Concerns / Issues ",
    "Concerns/Needs  - Self-Harm",
    "Concerns/Needs  - Sexuality",
    # "Concerns/Needs  - Suicide Related",
    # "Concerns/Needs  - Validity Question",
    # "Concerns/Needs  - Victim Assistance / Survivor Support ",
    # "Concerns/Needs  - Violence",
    # "Concerns/Needs  - xxx1",
    # "Concerns/Needs  - xxx2",
]

VIA_LINK_REQUIRED_COLUMNS_CALLS = [
    "CallReportNum",
    "ReportVersion",
    "CallDateAndTimeStart",
    "CityName",
    "CountyName",
    "StateProvince",
    "PostalCode",
    "Call Information - Program",
    "Demographics - Age",
    "Demographics - Gender",
] + needs_columns
vialink2_df = dfs["Uncleaned data type 2 VIA LINK"][VIA_LINK_REQUIRED_COLUMNS_CALLS]

# step 2
# remove calls not from LA Spirit line
vialink2_df = vialink2_df[
    vialink2_df["Call Information - Program"] == "LA Spirit Crisis Line"
]


# step 3
# combine all needs column into 1 column
all_needs = "Concerns/Needs - Concerns/Needs"
vialink2_df[all_needs] = vialink2_df[needs_columns].apply(
    lambda x: "; ".join(x[x.notnull()]), axis=1
)


# todo: pull this into a utils module
def explode_needs(df, need_column):
    df["tmp_needs"] = df[need_column].str.split(";")
    df = df.explode("tmp_needs")
    df.drop(columns=[need_column], inplace=True)
    df.rename(columns={"tmp_needs": need_column}, inplace=True)
    return df


vialink2_df = explode_needs(vialink2_df, all_needs)

# step 4
# add "Data From" column
vialink2_df["Data From"] = "VIA LINK"

# step 5
# cleanup Concerns/Needs Data

vialink2_df = vialink2_df[vialink2_df[all_needs] != "Wrong #"]
vialink2_df = vialink2_df[vialink2_df[all_needs] != "hangup"]
vialink2_df = vialink2_df.replace(
    {
        "Concerns/Needs  - Interpersonal": "Interpersonal Conflict",
        "Food": "Food/Meals",
        "Interpersonal Conflict": "Income Support/Assistance",
    }
)


# step 6
# drop all the original needs columns
vialink2_df.drop(columns=needs_columns, inplace=True)


# step 7
# add the Lat/Lng columns

# todo: pull this into a utils module
search = SearchEngine(simple_zipcode=True)


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


vialink2_df["Latitude"] = vialink2_df["PostalCode"].apply(get_lat)
vialink2_df["Longitude"] = vialink2_df["PostalCode"].apply(get_lng)


vialink2_df.to_excel(
    "data/keep_calm_with_covid_cleaned.xlsx", sheet_name="codefornola cleaned"
)
