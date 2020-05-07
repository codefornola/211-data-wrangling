import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)
import os
import sys

import click
import pandas as pd

from cleanup_all_covid_calls import cleanup as cleanup_all_covid_calls
from cleanup_keep_calm_with_covid import (
    CONVERTERS,
    cleanup as cleanup_keep_calm_with_covid,
)
from utils import write_output_file


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cleanup(ctx, debug):
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug


@cleanup.command()
@click.pass_context
@click.option(
    "--vialink-input",
    "vl_infile",
    required=True,
    help="Path to the VIA LINK input csv file",
)
@click.option(
    "--232-input",
    "two32_infile",
    required=True,
    help="Path to the 232 HELP input csv file",
)
@click.option(
    "--output",
    default="data/all_covid_calls_cleaned.xlsx",
    help="Path to the output spreadsheet (cleaned .xlsx file)",
)
def all_covid_calls(ctx, vl_infile, two32_infile, output):
    if ctx.obj["DEBUG"]:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Running in debug mode")
    logging.debug(f"Reading VIALINK file from '{vl_infile}'")
    logging.debug(f"Reading 232-HELP file from '{two32_infile}'")
    dfs = {}
    dfvl = pd.read_csv(vl_infile, encoding="ISO-8859-1")
    dfvl = remove_first_rows(dfvl)
    dfs["VIALINK"] = dfvl
    df232 = pd.read_csv(two32_infile, encoding="ISO-8859-1")
    df232 = remove_first_rows(df232)
    dfs["TWO32"] = df232
    logging.info("Cleaning data for All COVID Calls Dashboard")
    df = cleanup_all_covid_calls(dfs)
    logging.info(f"Writing data for All COVID Calls Dashboard to '{output}'")
    write_output_file(df, output)


@cleanup.command()
@click.pass_context
@click.option(
    "--input", "infile", required=True, help="Path to the input csv file",
)
@click.option(
    "--output",
    default="data/keep_calm_with_covid_cleaned.xlsx",
    help="Path to the output spreadsheet (cleaned .xlsx file)",
)
def keep_calm_with_covid(ctx, infile, output):
    if ctx.obj["DEBUG"]:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Running in debug mode")
    logging.debug(f"Reading input file '{infile}'")
    df = pd.read_csv(infile, encoding="ISO-8859-1", converters=CONVERTERS)
    df = remove_first_rows(df)
    logging.info("Cleaning data for Keep Calm with COVID Dashboard")
    cleanup_keep_calm_with_covid(df)
    logging.info(f"Writing data for Keep Calm with COVID Dashboard to '{output}'")
    write_output_file(df, output)


def remove_first_rows(df):
    columns = df.iloc[1].values.tolist()
    df = df.iloc[2:]
    df.columns = columns
    return df


if __name__ == "__main__":
    cleanup(obj={})
