# Название проекта
Проект: RELIA-QUEUE

## Описание
RELIA-QUEUE - это веб-приложение, разработанное для решения задач, связанных с системами массового обслуживания
(СМО) с использованием математического моделирования. Приложение предоставляет инструменты для анализа производительности и оптимизации процессов в различных типах СМО, а
также ознакомления с методическими указаниями, связанным с системами массового обслуживания и удобным калькулятором для подсчета с конкретными значениями.

## Системные требования
- Наличие современного браузера, поддерживающий HTTML5, CSS3
- Наличие стабильного интернета

## Использумые технологии
1. Poetry
-    Poetry - это инструмент для управления зависимостями и виртуальными средами в Python. Он облегчает создание, управление и публикацию пакетов Python, а также управление их зависимостями и виртуальными окружениями. Poetry также предоставляет инструменты для управления проектами и их зависимостями.
2. Ginga2
-    Ginga2 - это фреймворк для создания интерактивных источников данных в Python. Он предоставляет мощные инструменты для визуализации и анализа данных, а также поддерживает различные форматы изображений. Ginga2 может использоваться для создания пользовательских интерфейсов для визуализации данных и их взаимодействия с пользователями.
3. FastAPI
-    FastAPI - это современный веб-фреймворк для создания API на Python. Он быстрый, прост в использовании и поддерживает автоматическую документацию через интеграцию с Swagger UI и ReDoc. FastAPI позволяет создавать эффективные и масштабируемые веб-сервисы с помощью асинхронной обработки запросов.
4. Unicorn
-    Unicorn - это WSGI-сервер для запуска веб-приложений на Python. Он известен своей высокой производительностью и эффективностью при обработке запросов. Unicorn поддерживает асинхронную обработку и может быть использован совместно с различными веб-фреймворками, включая FastAPI.
5. Django Environ
-    Django Environ - это инструмент для загрузки настроек Django из переменных окружения. Он облегчает управление конфигурацией приложения и обеспечивает безопасное хранение конфиденциальной информации, такой как секреты и ключи доступа.
6. Pydantic
-    Pydantic - это библиотека для валидации данных и создания схем в Python. Она обеспечивает простой и декларативный способ определения структуры данных и их валидации. Pydantic интегрируется хорошо с различными фреймворками и библиотеками, включая FastAPI.

## Установка
1. Клонируйте репозиторий на свой локальный компьютер.
2. Убедитесь, что у вас установлен Python версии 3
3. Установить все зависимости
4. Запустите unicorn сервер для работы веб-сайта
5. Перейдите по адресу `http://localhost:820` в вашем браузере.

## Использование
После установки и запуска приложения вы сможете:
- Создавать модели СМО с различными параметрами.
- Проводить анализ производительности системы.
- Оптимизировать параметры СМО для достижения заданных целей.
- Изучать методические указания касательно это темы.

![image](https://drive.google.com/uc?export=view&id=1ANlZKGccKASJbJ8nE0euQjbhcYqyKZk0)

## Примеры 
- пример главного окна
- пример метода смо с отказом
- пример метода смо с неограниченной очередью
- пример систем из двух блоков
- пример страницы о нас

## Состояние
В данные момент проект RELIA-QUEUE находится в активной разработке. Он хорошо справляется со своими поставленными задачами, но ему не хватает некоторых функций, а страницы все еще находятся в процессе изменения. В следующая версиях будут серьезные изменения...

## Контактные данные
- Разработка метода СМО с отказом ([teneda](@teneda))
- Разработка метода СМО с неограниченной очередью(@triks)
- Разработка систем из двух блоков(@weidermartenn)

## Описание используемых файлов
1. app.py:
- Этот файл является фабрикой FastAPI, где создается экземпляр приложения FastAPI и настраиваются его параметры. Здесь определяются обработчики маршрутов и конфигурация приложения.
2. routes.py:
- Файл описывает маршруты приложения. Здесь определяются эндпоинты API и их обработчики. Routes.py определяет, какие действия выполняются при обращении к различным URL-адресам приложения.
3. surroundings.py:
- В этом файле реализована логика получения значений окружения и их сборки в дата классы. Surroundings.py отвечает за загрузку конфигурации приложения из переменных окружения и предоставляет ее для использования в других частях приложения.
4. res.py:
- Файл содержит настройки приложения. Res.py хранит различные параметры конфигурации, такие как настройки базы данных, порты, адреса серверов и другие параметры, которые используются при запуске и настройке приложения.

## Шрифт по умолчанию
- Mononoki.ttf: Версия 1.6 (https://madmalik.github.io/mononoki/) 