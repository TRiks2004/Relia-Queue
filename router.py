from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic_settings import BaseSettings
import system_reliability.components.block
import system_reliability.components.element

from surroundings import config_fast_api

import system_reliability 
from system_reliability import enums as enums_system_reliability
from system_reliability import date as date_system_reliability

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
        request=request, name=view_list.layout, context={"title": "ReliaQueue - Система блоков", 'dynamic_page': 'block_system_page1.html'}
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


class SystemReliabilityElement(BaseSettings):
    value: int

class SystemReliabilityBlock(BaseSettings):
    blockNumber: int
    mode: str
    elements: list[SystemReliabilityElement]

class SystemReliabilityForm(BaseSettings):
    systemMode: str
    blocks: list[SystemReliabilityBlock]


def with_connection(mode: str) -> enums_system_reliability.MethodConnection:
    match mode:
        case 'Последовательно':
            return enums_system_reliability.MethodConnection.Serial
        case 'Параллельно':
            return enums_system_reliability.MethodConnection.Parallel

import json
from dataclasses import asdict

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

    print(json_result)
    
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

    json_result = json.dumps(blok_list, default=custom_serializer, indent=4)

    return json_result

    

# {
#   "systemMode": "Последовательно",
#   "blocks": [
#     {
#       "blockNumber": 1,
#       "mode": "Параллельно",
#       "elements": [
#         {
#           "value": "0"
#         }
#       ]
#     },
#     {
#       "blockNumber": 2,
#       "mode": "Параллельно",
#       "elements": [
#         {
#           "value": "0"
#         },
#         {
#           "value": "0"
#         }
#       ]
#     }
#   ]
# }




