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
    main_page: str = plus_html('index')
    about_page: str = plus_html('about')
    block_system_page: str = plus_html('block_system_page')
    cfr_refusal_page: str = plus_html('cfr_refusal_page')
    cfr_unlimited_page: str = plus_html('cfr_unlimited_page')
    
view_list = ViewList()

@main_point.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name=view_list.layout, context={"title": "ReliaQueue - Главная", 'dynamic_page': view_list.main_page}
    )

@main_point.get('/about', response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse(
        request=request, name=view_list.layout, context={"title": "ReliaQueue - О нас", 'dynamic_page': view_list.about_page}
    )

@main_point.get('/block-system', response_class=HTMLResponse)
def block_system(request: Request):
    return templates.TemplateResponse(
        request=request, name=view_list.layout, context={"title": "ReliaQueue - Система блоков", 'dynamic_page': view_list.block_system_page}
    )

@main_point.get('/cfr-refusal', response_class=HTMLResponse)
def cfr_refusal(request: Request):
    return templates.TemplateResponse(
        request=request, name=view_list.layout, context={"title": "ReliaQueue - МСМО с отказами", 'dynamic_page': view_list.cfr_refusal_page}
    )

@main_point.get('/cfr-unlimited', response_class=HTMLResponse)
def cfr_unlimited(request: Request):
    return templates.TemplateResponse(
        request=request, name=view_list.layout, context={"title": "ReliaQueue - МСМО c неограниченной очередью ", 'dynamic_page': view_list.cfr_unlimited_page}
    )

class InputParameters(BaseSettings):
    value: int

class CFRUnlimitedParameters(BaseSettings):
    serviceTime: int
    maxSimulationTime: int
    parameter: int
    channelCount: int
    iterationCount: int

@main_point.post('/cfr-unlimited')
async def run_simulation_handler(request: Request):
    data = await request.json()
    parameters = CFRUnlimitedParameters(**data)
    