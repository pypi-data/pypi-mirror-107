import logging

import coloredlogs
import typer

from fulfyld.cli import fedex

level = "INFO"
logger = logging.getLogger(__name__)

formatter = logging.Formatter(
    "%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler = logging.StreamHandler()
handler.setLevel(level)
handler.setFormatter(formatter)

pkg_logger = logging.getLogger("fulfyld")
pkg_logger.setLevel(level)
pkg_logger.addHandler(handler)
coloredlogs.install(level=level, logger=pkg_logger, milliseconds=True)


app = typer.Typer()

app.add_typer(fedex.app, name="fedex")

if __name__ == "__main__":
    app()
