from labs.config import get_logger, POLYGLOT_DIR, spacy_models
import typer
from polyglot.downloader import Downloader
import spacy
from vector.queries import setup_db

app = typer.Typer()


@app.command()
def main():
    logger = get_logger(__name__)
    logger.debug("# POLYGLOT")
    polyglot_resources = [
        "embeddings2.en",
        "ner2.en",
        "pos2.en",
        "embeddings2.pt",
        "ner2.pt",
        "pos2.pt",
    ]
    dl = Downloader(download_dir=POLYGLOT_DIR)
    logger.debug("    Updating polyglot package list...")
    dl.packages()

    logger.debug("    Checking polyglot data...")
    for resource in polyglot_resources:
        if dl.status(resource) != dl.INSTALLED:
            logger.debug(f"Downloading {resource}...")
            dl.download(resource)

    logger.debug("# SPACY")
    logger.debug("    Getting installed models...")
    installed_models = spacy.util.get_installed_models()

    logger.debug("    Checking spacy models...")
    for model in spacy_models:
        if model["model"] not in installed_models:
            logger.debug(f"Installing {model['model']}...")
            spacy.cli.download(model["model"])

    logger.debug("# DATABASE")
    logger.debug("    Setting up database...")
    setup_db()
    logger.debug("    Database was set up...")


if __name__ == "__main__":
    app()
