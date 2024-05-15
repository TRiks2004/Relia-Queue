import pathlib
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from surroundings import config_fast_api

from router import main_point

async def lifespan(app: FastAPI):
    ml_models = {}

    yield ml_models

def api_factory() -> FastAPI:

    app = FastAPI(
        title=config_fast_api.title,
        docs_url=config_fast_api.docs_url,
        debug=config_fast_api.debug,
        lifespan=lifespan,
    )
    
    app.mount("/static", StaticFiles(directory=config_fast_api.static_dir), name="static")
    
    app.include_router(main_point)
    
    return app