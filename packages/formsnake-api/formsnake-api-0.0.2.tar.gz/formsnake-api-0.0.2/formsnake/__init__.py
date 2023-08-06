__version__ = "0.0.2"

import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
MODULE_DIR = Path(__file__).parent.absolute()


def run_server():
    """
    Run the server on the address and
    port specified in the environment.
    """
    from formsnake.server import app
    from alembic import command
    from alembic.config import Config

    command.upgrade(Config(f"{MODULE_DIR}/alembic.ini"), "head")
    listen_addr = os.environ.get("FORMSNAKE_LISTEN_ADDR", "127.0.0.1")
    listen_port = int(os.environ.get("FORMSNAKE_LISTEN_PORT", "5000"))
    print(f"Running the server at http://{listen_addr}:{listen_port}")
    app.run(
        host=listen_addr, port=listen_port,
    )
