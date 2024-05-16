from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic_settings import BaseSettings

from surroundings import config_fast_api

main_point = APIRouter(
    prefix=''
)

templates = Jinja2Templates(directory=config_fast_api.templates_dir)


def plus_html(view_name: str) -> str:
    return f"{view_name}.j2"

class ViewList(BaseSettings):

    # layout.html main_page.html qs_theory_page.html block_system_page.html cfr_refusal_page.html cfr_unlimited_page.html about.html                                                               ─╯
    layout: str = plus_html('layout')
    main_page: str = plus_html('main_page')
    
view_list = ViewList()

@main_point.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name=view_list.layout, context={'id': 1, "title": "Your Dynamic Title", 'dynamic_page': view_list.main_page}
    )





