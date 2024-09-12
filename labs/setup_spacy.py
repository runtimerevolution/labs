from config import get_logger, spacy_models
import typer
import spacy

app = typer.Typer()


@app.command()
def main():
    logger = get_logger(__name__)
    logger.debug("# SPACY")
    logger.debug("    Getting installed models...")
    installed_models = spacy.util.get_installed_models()

    logger.debug("    Checking spacy models...")
    for model in spacy_models:
        if model["model"] not in installed_models:
            logger.debug(f"Installing {model['model']}...")
            spacy.cli.download(model["model"])

    logger.debug("    Spacy's models installed...")


if __name__ == "__main__":
    app()
