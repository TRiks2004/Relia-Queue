import pathlib
from uvicorn import run

from app import api_factory 

import environ

from surroundings import config_container

app = api_factory()

if __name__ == "__main__":
    run(
        "uvicorn_service:app",
        host="127.0.0.1",
        port=config_container.api_port_container,
        reload=True,
    )