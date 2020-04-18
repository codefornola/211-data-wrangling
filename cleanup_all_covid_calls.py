import pandas as pd
import numpy as np
from datetime import datetime
from utils import explode_needs, get_lat, get_lng, replacements
pd.options.mode.chained_assignment = None



def cleanup(dfs):
    ### Cleanup for All COVID Calls dashboard

    # step 1
    # select required columns from VIA LINK’s Disaster Form
    # pretty sure the distaster form is "Uncleaned data type 1 VIA LINK"
    VIA_LINK_REQUIRED_COLUMNS_DISASTER = [
        "CallReportNum",
        "ReportVersion",
        "CallDateAndTimeStart",
        "CityName",
        "CountyName",
        "StateProvince",
        "PostalCode",
        "Client Information - Age Group",
        "Client Information - Call Type",
        "Client Information - Identifies as",
        "Concerns/Needs - Concerns/Needs",
        "Contact Source - Program ",  # ending space is needed
        "Needs - Basic Needs Requested",
    ]
    vialink1_df = dfs["Uncleaned data type 1 VIA LINK"][
        VIA_LINK_REQUIRED_COLUMNS_DISASTER
    ]

    # step 2
    # select required columns from 232-Help’s Disaster Form
    TWO32_HELP_REQUIRED_COLUMNS = [
        "CallReportNum",
        "ReportVersion",
        "CallDateAndTimeStart",
        "CityName",
        "CountyName",
        "StateProvince",
        "PostalCode",
        "Client Information - Date of Birth",
        "Client Information - Call Type",
        "Call Outcome - What concerns/needs were identified?",
        "Client Information - Identifies as",
        "Needs - Basic Needs Requested",
    ]
    two32_help_df = dfs["Uncleaned Data from 232-Help"][TWO32_HELP_REQUIRED_COLUMNS]

    # step 3
    # Create age ranges from date of birth
    # use ranges 0-5, 6-12, 13-17, 18-24, 25-40, 41-59, 60+.
    now = datetime.now()
    bins = [0, 5, 12, 17, 24, 40, 59, 150]
    labels = ["0-5", "6-12", "13-17", "18-24", "24-40", "41-49", "60+"]
    dob = pd.to_datetime(
        two32_help_df["Client Information - Date of Birth"], errors="coerce"
    )
    years_old = (now - dob).astype("timedelta64[Y]")
    age_range = pd.cut(years_old, bins=bins, labels=labels, include_lowest=True)
    two32_help_df["Client Information - Age Group"] = age_range
    # remove original Date of Birth column
    two32_help_df.drop(columns=["Client Information - Date of Birth"], inplace=True)

    # step 4
    # add "Data From" column
    vialink1_df["Data From"] = "VIA LINK"
    two32_help_df["Data From"] = "232-HELP"

    # step 5
    # add data to master spreadsheet
    # first merge "Call Outcome - What concerns/needs were identified" from 232-HELP
    # into "Concerns/Needs - Concerns/Needs"
    two32_help_df.rename(
        columns={
            "Call Outcome - What concerns/needs were identified?": "Concerns/Needs - Concerns/Needs"
        },
        inplace=True,
    )

    # new steps
    # cleanup invalid values
    vialink1_df["Contact Source - Program "].replace(
        to_replace=datetime(2001, 2, 1, 0, 0), value=np.nan, inplace=True
    )

    # then combine data
    master_df = pd.concat([vialink1_df, two32_help_df], join="outer", ignore_index=True)

    # step 6
    # add lat/lon columns
    master_df["Latitude"] = master_df["PostalCode"].apply(get_lat)
    master_df["Longitude"] = master_df["PostalCode"].apply(get_lng)

    # step 7
    # first put the values from "Needs - Basic Needs Requested" into "Concerns/Needs - Concerns/Needs"
    cn = "Concerns/Needs - Concerns/Needs"
    master_df["all_needs"] = master_df[[cn, "Needs - Basic Needs Requested"]].apply(
        lambda x: "; ".join(x[x.notnull()]), axis=1
    )
    master_df.drop(columns=[cn, "Needs - Basic Needs Requested"], inplace=True)
    master_df.rename(columns={"all_needs": cn}, inplace=True)
    master_df = explode_needs(master_df, cn)

    # step 8
    # cleanup Concerns/Needs
    master_df[cn] = master_df[cn].str.strip()
    master_df = master_df[master_df[cn] != "Hangup / Wrong Number"]
    master_df = master_df[master_df[cn] != "Hangup / Wrong #"]
    master_df.replace(to_replace=replacements, value=None, inplace=True)

    return master_df


if __name__ == "__main__":
    file = "Data from 4.2.20 Fake Data.xlsx"

    # read all sheets, returns a dict of dataframes
    dfs = pd.read_excel(file, sheet_name=None)

    df = cleanup(dfs)

    # write out spreadsheet
    df.to_excel("data/all_covid_calls_cleaned.xlsx", sheet_name="codefornola cleaned")
