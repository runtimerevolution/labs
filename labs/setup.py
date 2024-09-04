from labs.config import get_logger
import typer
from setup_spacy import main as setup_spacy
from vector.queries import setup_db

app = typer.Typer()


@app.command()
def main():
    logger = get_logger(__name__)
    setup_spacy()
    logger.debug("# DATABASE")
    logger.debug("    Setting up database...")
    setup_db()
    logger.debug("    Database was set up...")


if __name__ == "__main__":
    app()
