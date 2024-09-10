import logging
import typer
from setup_spacy import main as setup_spacy
from vector.queries import setup_db

logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def main():
    setup_spacy()
    logger.debug("# DATABASE")
    logger.debug("    Setting up database...")
    setup_db()
    logger.debug("    Database was set up...")


if __name__ == "__main__":
    app()
