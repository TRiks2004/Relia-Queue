import environ
from pydantic_settings import BaseSettings

import pathlib

env = environ.Env()

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR / ".env")

class ConfigFastAPI(BaseSettings):
    title: str = env("FAST_API_TITLE")
    docs_url: str = env("FAST_API_DOCS_URL")
    debug: bool = env.bool("FAST_API_DEBUG", False)
    
    static_dir: pathlib.Path = (pathlib.Path(__file__).resolve().parent / 'resurse' / 'static')
    
    templates_dir: pathlib.Path = (pathlib.Path(__file__).resolve().parent / 'resurse' / 'template')   

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"

config_fast_api = ConfigFastAPI()

class ConfigContainer(BaseSettings):
    api_port_container: int = env.int("PORT_CONTAINER_API")

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"

config_container = ConfigContainer()