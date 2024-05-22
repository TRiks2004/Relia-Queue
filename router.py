from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response

from pydantic_settings import BaseSettings
from fastapi import FastAPI, Form
from surroundings import config_fast_api
from dataclasses import asdict
from pydantic import BaseModel
import json
from smo_rejection import run_simulation, SimulationParameters, export_to_pdf

main_point = APIRouter(
    prefix=''
)

templates = Jinja2Templates(directory=config_fast_api.templates_dir)


def plus_html(view_name: str) -> str:
    return f"{view_name}.j2"

class ViewList(BaseSettings):
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


from pydantic import BaseModel

class InputParameter(BaseModel):
    """
    Модель данных для представления отдельного числового параметра.

    Атрибуты:
        value (float): Значение параметра.
    """
    value: float

class SimulationInput(BaseModel):
    """
    Модель данных для представления входных параметров симуляции.

    Атрибуты:
        T (float): Продолжительность симуляции.
        num_channels (int): Количество каналов обслуживания.
        service_time (float): Время обслуживания.
        num_iterations (int): Количество итераций симуляции.
        alfa (int): Интенсивность потока заявок.
    """
    T: float
    num_channels: int
    service_time: float
    num_iterations: int
    alfa: int

from fastapi import FastAPI, Request

# Определение точки входа (роута) для запуска симуляции
@main_point.post('/cfr-refusal')
async def run_simulation_handler(request: Request, response_format: str = 'json'):
    """
    Обработчик HTTP POST-запросов для запуска симуляции.

    Параметры:
        request (Request): Объект запроса FastAPI.
        response_format (str): Формат ответа (по умолчанию 'json').

    Возвращает:
        Результаты симуляции в указанном формате.
    """
    # Получение данных из тела запроса
    data = await request.json()
    
    # Создание экземпляра модели SimulationInput из полученных данных
    params = SimulationInput(**data)
    
    # Вызов функции run_simulation с входными параметрами из модели
    results = run_simulation(
        T=params.T,
        num_channels=params.num_channels,
        service_time=params.service_time,
        num_iterations=params.num_iterations,
        alfa=params.alfa,
    )
    
    # Возвращение результатов симуляции
    return results