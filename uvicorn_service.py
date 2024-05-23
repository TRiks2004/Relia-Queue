from uvicorn import run

from app import api_factory 

from surroundings import config_container

app = api_factory()

if __name__ == "__main__":
    run(
        "uvicorn_service:app",
        host="0.0.0.0",
        port=config_container.api_port_container,
        reload=True,
    )