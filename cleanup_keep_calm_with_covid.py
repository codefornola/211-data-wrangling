import pandas as pd
import numpy as np
from datetime import datetime

from constants import (
    VIALINK_REQUIRED_COLUMNS_CALLS,
    VIALINK_NEEDS_COLUMNS,
    VIALINK_REQUIRED_COLUMNS_DISASTER,
    VIALINK_CALLS_KEY,
    VIALINK_DISASTER_KEY,
    HANGUP_VALUES,
)
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


def cleanup(dfs):
    ### Cleanup for Keeping Calm with COVID dashboard
    # step 1
    # select only the required columns
    df = dfs[VIALINK_CALLS_KEY][VIALINK_REQUIRED_COLUMNS_CALLS]

    # step 2
    # remove calls not from LA Spirit line
    df = df[df["Call Information - Program"].str.contains("LA Spirit")]

    # step 3
    # combine all needs column into 1 column
    all_needs = "Concerns/Needs - Concerns/Needs"
    df[all_needs] = df[VIALINK_NEEDS_COLUMNS].apply(lambda x: "; ".join(x[x.notnull()]), axis=1)
    df = explode_needs(df, all_needs)

    # step 4
    # add "Data From" column
    df["Data From"] = "VIA LINK"

    # step 5
    # cleanup Concerns/Needs Data
    df[all_needs] = df[all_needs].str.strip()
    df.replace(to_replace=replacements, value=None, inplace=True)

    # step 6
    # drop all the original needs columns
    df.drop(columns=VIALINK_NEEDS_COLUMNS, inplace=True)

    # use the same process from the all covid calls dashboard
    df_disaster = dfs[VIALINK_DISASTER_KEY][VIALINK_REQUIRED_COLUMNS_DISASTER]
    # only include LA Spirit Crisis calls
    df_disaster = df_disaster[
        df_disaster["Contact Source - Program "].str.contains("LA Spirit")
    ]
    # cleanup invalid values
    df_disaster["Contact Source - Program "].replace(
        to_replace=datetime(2001, 2, 1, 0, 0), value=np.nan, inplace=True
    )

    df_disaster["Data From"] = "VIA LINK"

    master_df = pd.concat([df, df_disaster], join="outer", ignore_index=True)

    # add lat/lon columns
    master_df["Latitude"] = master_df["PostalCode"].apply(get_lat)
    master_df["Longitude"] = master_df["PostalCode"].apply(get_lng)

    # first put the values from "Needs - Basic Needs Requested" into "Concerns/Needs - Concerns/Needs"
    cn = "Concerns/Needs - Concerns/Needs"
    master_df["all_needs"] = master_df[[cn, "Needs - Basic Needs Requested"]].apply(
        lambda x: "; ".join(x[x.notnull()]), axis=1
    )
    master_df.drop(columns=[cn, "Needs - Basic Needs Requested"], inplace=True)
    master_df.rename(columns={"all_needs": cn}, inplace=True)
    master_df = explode_needs(master_df, cn)

    # cleanup Concerns/Needs
    master_df[cn] = master_df[cn].str.strip()
    master_df.replace(to_replace=replacements, value=None, inplace=True)

    # remove hangups
    master_df = master_df[~master_df[cn].isin(HANGUP_VALUES)]
    master_df = master_df[~master_df["Call Information - Counseling agency MHC BHC etc. "].isin(HANGUP_VALUES)]
    master_df = master_df[~master_df["Call Information - Mental Health Region"].isin(HANGUP_VALUES)]
    master_df = master_df[~master_df["Call Information - Contact Type"].isin(HANGUP_VALUES)]

    return master_df
