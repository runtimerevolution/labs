from configparser import ConfigParser
import pathlib


def db_config(section: str = "postgresql"):
    filename = f"{pathlib.Path().resolve()}/database.ini"
    parser = ConfigParser()
    parser.read(filename)
    if parser.has_section(section):
        params = parser.items(section)
        db = {param[0]: param[1] for param in params}
    else:
        raise Exception(f"Section {section} not found in the {filename} file")
    return db
