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
    "--input",
    "infile",
    required=True,
    help="Path to the input spreadsheet (.xlsx file)",
)
@click.option("--sheetname", default=None, help="Name of the sheet to use")
@click.option(
    "--output",
    default="data/all_covid_calls_cleaned.xlsx",
    help="Path to the output spreadsheet (cleaned .xlsx file)",
)
def all_covid_calls(ctx, infile, sheetname, output):
    if ctx.obj["DEBUG"]:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Running in debug mode")
    logging.debug(f"Reading input file '{infile}'")
    df = pd.read_excel(infile, sheet_name=sheetname)
    logging.info("Cleaning data for All COVID Calls Dashboard")
    df = cleanup_all_covid_calls(df)
    logging.info(f"Writing data for All COVID Calls Dashboard to '{output}'")
    write_output_file(df, output)


@cleanup.command()
@click.pass_context
@click.option(
    "--input",
    "infile",
    required=True,
    help="Path to the input spreadsheet (.xlsx file)",
)
@click.option("--sheetname", required=True, help="Name of the sheet to use")
@click.option(
    "--output",
    default="data/keep_calm_with_covid_cleaned.xlsx",
    help="Path to the output spreadsheet (cleaned .xlsx file)",
)
def keep_calm_with_covid(ctx, infile, sheetname, output):
    if ctx.obj["DEBUG"]:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Running in debug mode")
    logging.debug(f"Reading input file '{infile}'")
    df = pd.read_excel(infile, sheet_name=sheetname, converters=CONVERTERS)
    logging.info("Cleaning data for Keep Calm with COVID Dashboard")
    cleanup_keep_calm_with_covid(df)
    logging.info(f"Writing data for Keep Calm with COVID Dashboard to '{output}'")
    write_output_file(df, output)


if __name__ == "__main__":
    cleanup(obj={})
