from logging import getLogger
from pathlib import Path

import clevercsv
import typer

logger = getLogger(__name__)

app = typer.Typer()


@app.command()
def prepare_charge_csv(input_csv: Path, output_file: Path = Path("fedex_output.csv")):
    logger.debug("Executing prepare_charge_csv command")

    logger.info("Loading file %s", str(input_csv))
    df = clevercsv.read_dataframe(input_csv)
    logger.info("Done")
