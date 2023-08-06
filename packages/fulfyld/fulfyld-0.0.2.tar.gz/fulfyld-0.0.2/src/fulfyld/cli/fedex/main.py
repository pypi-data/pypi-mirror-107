from logging import getLogger
from pathlib import Path

import pandas as pd
import typer

logger = getLogger(__name__)

app = typer.Typer()


@app.command()
def prepare_charge_csv(input_csv: Path, output_file: Path = Path("fedex_output.csv")):
    logger.debug("Executing prepare_charge_csv command")

    logger.info("Loading file %s", str(input_csv))
    df = pd.read_csv(input_csv, dtype=str)

    required_columns = ["Ground Tracking ID Prefix", "Express or Ground Tracking ID"]
    variable_columns = ["Tracking ID Charge Description", "Tracking ID Charge Amount"]
    suffixes = ["", *[f"({x})" for x in range(2, 26)]]

    chunks = []

    for suffix in suffixes:
        logger.info("Appending chunk with suffix %s", suffix)
        column_names = required_columns + [x + suffix for x in variable_columns]
        chunk = df[column_names]
        chunk.columns = required_columns + variable_columns
        chunks.append(chunk)

    logger.info("Concatenating chunks")
    flat_df = pd.concat(chunks)

    # Filter rows where the charge amount and description are null
    flat_df = flat_df[flat_df["Tracking ID Charge Amount"].notna()]

    logger.info("Saving file %s", str(output_file))
    flat_df.to_csv(output_file, index=False)

    logger.info("Save complete")
