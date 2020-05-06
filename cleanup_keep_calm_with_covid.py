import pandas as pd
import numpy as np
from datetime import datetime
from utils import explode_needs, get_lat, get_lng, replacements

CONVERTERS = {
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


def cleanup(df):
    ### Cleanup for Keeping Calm with COVID dashboard
    # step 1
    # select only the required columns
    needs_columns = [
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
    df = df[VIA_LINK_REQUIRED_COLUMNS_CALLS]

    # step 2
    # remove calls not from LA Spirit line
    df = df[df["Call Information - Program"] == "LA Spirit Crisis Line"]

    # step 3
    # combine all needs column into 1 column
    all_needs = "Concerns/Needs - Concerns/Needs"
    df[all_needs] = df[needs_columns].apply(lambda x: "; ".join(x[x.notnull()]), axis=1)
    df = explode_needs(df, all_needs)

    # step 4
    # add "Data From" column
    df["Data From"] = "VIA LINK"

    # step 5
    # cleanup Concerns/Needs Data
    df[all_needs] = df[all_needs].str.strip()
    df = df[df[all_needs] != "Wrong #"]
    df = df[df[all_needs] != "hangup"]
    df.replace(to_replace=replacements, value=None, inplace=True)

    # step 6
    # drop all the original needs columns
    df.drop(columns=needs_columns, inplace=True)

    # step 7
    # add the Lat/Lng columns
    df["Latitude"] = df["PostalCode"].apply(get_lat)
    df["Longitude"] = df["PostalCode"].apply(get_lng)

    return df
