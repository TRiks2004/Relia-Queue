from fastapi import APIRouter, Request, FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from pydantic_settings import BaseSettings

from dataclasses import asdict
from io import BytesIO
import json

import pdfkit

import system_reliability
import system_reliability.components.block
import system_reliability.components.element
from system_reliability import enums as enums_system_reliability

from surroundings import config_fast_api

from smo_rejection import run_simulation
from smo_over_queue import simulate_queue


from schemas import (
    CFRUnlimitedParameters, SimulationInput, SystemReliabilityForm
)


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



def get_css_file(name: str) -> str:
    return f'static/style/{name}.css'

class CSSFile(BaseSettings):
    layout: str = get_css_file('layout')

css_file = CSSFile()

def get_js_file(name: str) -> str:
    return f'static/scripts/{name}.js'

class JSFile(BaseSettings):
    script: str = get_js_file('script')
    block_system_page: str = get_js_file('block_system_page')
    smo_rejection: str = get_js_file('smo_rejection')
    smo_over_queue: str = get_js_file('smo-over-queue')

js_file = JSFile()


@main_point.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name=view_list.layout, context={
            "title": "ReliaQueue - Главная", 
            'dynamic_page': view_list.main_page,
            'styles': [css_file.layout],
            'javascripts': [js_file.script],
        }
    )

@main_point.get('/about', response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse(
        request=request, name=view_list.layout, context={
            "title": "ReliaQueue - О нас", 
            'dynamic_page': view_list.about_page,
            'styles': [css_file.layout],
            'javascripts': [js_file.script],
        }
    )

@main_point.get('/block-system', response_class=HTMLResponse)
def block_system(request: Request):
    return templates.TemplateResponse(
        request=request, name=view_list.layout, context={
            "title": "ReliaQueue - Система блоков", 
            'dynamic_page': view_list.block_system_page,
            'styles': [css_file.layout],
            'javascripts': [js_file.script, js_file.block_system_page],
        }
    )

@main_point.get('/cfr-refusal', response_class=HTMLResponse)
def cfr_refusal(request: Request):
    return templates.TemplateResponse(
        request=request, name=view_list.layout, context={
            "title": "ReliaQueue - МСМО с отказами", 
            'dynamic_page': view_list.cfr_refusal_page,
            'styles': [css_file.layout],
            'javascripts': [js_file.script, js_file.smo_rejection],
        }
    )

@main_point.get('/cfr-unlimited', response_class=HTMLResponse)
def cfr_unlimited(request: Request):
    return templates.TemplateResponse(
        request=request, name=view_list.layout, context={
            "title": "ReliaQueue - МСМО c неограниченной очередью", 
            'dynamic_page': view_list.cfr_unlimited_page,
            'styles': [css_file.layout],
            'javascripts': [js_file.script, js_file.smo_over_queue],
        }
    )


# Обработчик POST-запроса для симуляции CFR Unlimited
@main_point.post('/cfr-unlimited')
async def run_simulation_handler(request: Request):
    # Получение данных из запроса в формате JSON
    data = await request.json()

    # Преобразование данных в объект класса CFRUnlimitedParameters
    parameters = CFRUnlimitedParameters(**data)

    # Запуск симуляции с использованием параметров
    results = simulate_queue(
        service_time=parameters.serviceTime,
        max_time=parameters.maxSimulationTime,
        alpha=parameters.alpha,
        num_threads=parameters.channelCount,
        num_iterations=parameters.iterationCount
    )
    
    # Возврат результатов симуляции
    return results

def with_connection(mode: str) -> enums_system_reliability.MethodConnection:
    match mode:
        case 'Последовательно':
            return enums_system_reliability.MethodConnection.Serial
        case 'Параллельно':
            return enums_system_reliability.MethodConnection.Parallel

def custom_serializer(obj):
    if isinstance(obj, enums_system_reliability.MethodConnection):
        return obj.value
    if hasattr(obj, '__dataclass_fields__'):
        return asdict(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
    

@main_point.post('/calculate/system_reliability')
def calculate_system_reliability(form: SystemReliabilityForm):

    system = []
    for block in form.blocks:
        elements = []
        for element in block.elements:
            elements.append(system_reliability.components.element.Element(probability=element.value / 100))

        system.append(
            system_reliability.components.block.Block(
                *elements, connection=with_connection(block.mode)
            )
        )

    result = system_reliability.components.block.Block(*system, connection=with_connection(form.systemMode))

    result_calc = result.calculate()

    json_result = json.dumps(result_calc, default=custom_serializer, indent=4)

    blok_list = {}

    blok_list['system'] = {}
    blok_list['blocks_choice'] = {}

    selected_indices = [0, 1, 2, len(result_calc.simulated_results.details) - 1]  # Select 1st, 2nd, 3rd, and last
    for i in selected_indices:
        iteration = result_calc.simulated_results.details[i]
        for j, blok in enumerate(iteration.components):
            if f'block_{j}' not in blok_list['system']:
                blok_list['system'][f'block_{j}'] = {
                    'mode': blok.connection,
                    'iteration': {}
                }

            blok_list['system'][f'block_{j}']['iteration'][i] = {
                'blok_probability': blok.probability,
                'iteration': [
                    {
                        'random_value': element.random_value,
                        'probability': element.probability,
                        'probability_analytical': element.probability_analytical
                    } for element in blok.components
                ]
            }
            
            blok_list['blocks_choice'][i] = iteration.probability
            
    blok_list['system_mode'] = result_calc.simulated_results.details[0].connection
    blok_list['system_probability'] = result_calc.simulated_results.probability
    blok_list['success_count'] = result_calc.simulated_results.success_count
    blok_list['num_trials'] = result_calc.simulated_results.num_trials

    blok_list['analytical'] = result_calc.analytical_results
    blok_list['analytical_probability'] = float(result_calc.analytical_results.split('=')[1].replace(' ', ''))
    blok_list['dif'] = round(abs(blok_list['system_probability'] - blok_list['analytical_probability']), 4)
    json_result = json.dumps(blok_list, default=custom_serializer, indent=4)

    return json_result

config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

@main_point.post("/calculate/system_reliability/generate-pdf")
async def generate_pdf(request: Request):
    data = await request.json()
    html = data.get("html")

    if not html:
        return JSONResponse(content={"error": "No HTML content provided"}, status_code=400)

    # Добавление стиля для поддержки кириллицы
    styled_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: DejaVu Sans, sans-serif;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            th, td {{
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        {html}
    </body>
    </html>
    """

    # Генерация PDF
    try:
        pdf = pdfkit.from_string(styled_html, False, configuration=config)
        pdf_bytes = BytesIO(pdf)
        pdf_bytes.seek(0)

        return StreamingResponse(pdf_bytes, media_type="application/pdf", headers={
            "Content-Disposition": "attachment; filename=generated.pdf"
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

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