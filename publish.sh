#!/bin/bash

# Увеличиваем версию
poetry run bump2version patch

# Публикуем пакет
poetry publish --build
