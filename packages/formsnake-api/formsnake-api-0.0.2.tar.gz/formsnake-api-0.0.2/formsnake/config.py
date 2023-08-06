"""
Functions and constants for setting up the configuration
of the Flask server.
"""

from dotenv import load_dotenv
from pathlib import Path
from os import environ

load_dotenv()


def get_base_dir():
    """
    Return the BASE_PATH. Used as function for
    patching ability.
    """
    BASE_PATH = Path.home().joinpath(".config", "formsnake")
    if not Path.exists(BASE_PATH):
        Path.mkdir(BASE_PATH, parents=True)
    return BASE_PATH


SQLITE_DB_PATH = Path(__file__).parent.absolute()
FLASK_SQLALCHEMY_DATABASE_URI = environ.get(
    "FORMSNAKE_DB_URI", f"sqlite:///{SQLITE_DB_PATH}/local.db"
)
JWT_SIGNING_KEY = environ.get("FORMSNAKE_SIGNING_KEY", "this_should_be_changed")


def get_flask_config() -> dict:
    """
    Returns a dict of values to set-up
    the app.config() object based on the
    selected env.
    """
    env = environ.get("FLASK_ENV", "dev")
    dev_mode_on = env == "dev"
    return {
        "FLASK_ENV": environ.get("FLASK_ENV", "dev"),
        "AUTO_RELOAD_TEMPLATES": True,
        "DEBUG": dev_mode_on,
        "TESTING": dev_mode_on,
        "SQLALCHEMY_DATABASE_URI": FLASK_SQLALCHEMY_DATABASE_URI,
        "SQLALCHEMY_ECHO": False,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
