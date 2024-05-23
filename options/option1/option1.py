from selenium import webdriver
import time
import json
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Объявление веб-драйвера
driver = webdriver.Chrome()
driver.get('https://neo.xn--n1afb.site')

# Объявление действий для веб-драйвера
actions = ActionChains(driver)

# Добавляем задержку в 3 секунды
time.sleep(2)

# Находим все элементы с атрибутом class name='choice-button'
buttons = driver.find_elements(by='class name', value = 'choice-button')
title = driver.find_element(by='xpath', value='/html/body/div[3]/p[3]')

# Выбираем кнопку "Многоканальные СМО с неограниченной очередью"
unlimited_button = buttons[0]

# Выполняем скролл до заголовка
actions.move_to_element(title).perform()
print('\n' + '-' * 20 + '\n' + 'Выполнен скролл' + '\n' + '-' * 20 + '\n')
time.sleep(2)

# Нажимаем кнопку
unlimited_button.click()
print('\n' + '-' * 20 + '\n' + 'Нажата кнопка "Многоканальные СМО с неограниченной очередью"' + '\n' + '-' * 20 + '\n')
time.sleep(1)

# Вывод того, что мы перешли на страницу "СМО с неограниченными очередями"
print('\n' + '-' * 20 + '\n' + 'Переход на страницу "СМО с неограниченными очередями"' + '\n' + '-' * 20 + '\n')
time.sleep(2)

# Находим все элементы с атрибутом class name='skip-button'
buttons = driver.find_elements(by='class name', value = 'skip-button')

# Выбираем кнопку "Ввод параметров"
input_button = buttons[1]

# Нажимаем кнопку
input_button.click()
print('\n' + '-' * 20 + '\n' + 'Нажата кнопка "Ввод параметров"' + '\n' + '-' * 20 + '\n')
time.sleep(2)

# Находим все элементы с атрибутом class name='form-input'
inputs = driver.find_elements(by='class name', value = 'form-input')

# Считываем данные из json файла
with open('options/option1/data.json', 'r') as f:
    data = json.load(f)

parameters = data['parameters']
param_array = list(parameters.values())

# Вводим параметры
for i in range(len(param_array)):
    inputs[i].send_keys(param_array[i])
    print('\n' + '-' * 20 + '\n' + 'Ввод параметров' + '\n' + '-' * 20 + '\n')
    time.sleep(1)

# Находим кнопку "Решить"
solve_button = driver.find_element(by='class name', value = 'solve-button')

# Нажимаем кнопку
solve_button.click()
print('\n' + '-' * 20 + '\n' + 'Нажата кнопка "Решить"' + '\n' + '-' * 20 + '\n')

# Выводим сообщение после решения
print('\n' + '-' * 20 + '\n' + 'Вывод результатов' + '\n' + '-' * 20 + '\n')
time.sleep(7)

# Находим заголовок "Результат"
result_title = driver.find_element(by='id', value='resultTitle')

# Считаем Y координату
y = result_title.location['y']
scroll_y = y - 200

# Скроллим вниз
print('\n' + '-' * 20 + '\n' + 'Скроллим вниз' + '\n' + '-' * 20 + '\n')
# Функция для плавного скролла
def smooth_scroll():
    SCROLL_PAUSE_TIME = 0.05
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_step = 80  # Изменение координаты Y после каждой паузы

    while True:
        for i in range(scroll_y, last_height, scroll_step):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(SCROLL_PAUSE_TIME)
        
        # Скроллим вверх
        print('\n' + '-' * 20 + '\n' + 'Скроллим вверх' + '\n' + '-' * 20 + '\n')

        for i in range(last_height, scroll_y, -scroll_step):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(SCROLL_PAUSE_TIME)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# Вызов функции для плавного скролла
smooth_scroll()

time.sleep(2)

# Находим кнопку "Сохранить решение в PDF"
pdf_button = driver.find_element(by='id', value = 'pdfButton')

# Нажимаем кнопку
pdf_button.click()
print('\n' + '-' * 20 + '\n' + 'Нажата кнопка "Сохранить решение в PDF"' + '\n' + '-' * 20 + '\n')
time.sleep(2)

# Переходим на страницу с загрузками
driver.get('chrome://downloads/')

# Выводим сообщение после загрузки
print('\n' + '-' * 20 + '\n' + 'Файл загружен' + '\n' + '-' * 20 + '\n')
time.sleep(3)

# Вывод сообщения
print('\n' + '-' * 20 + '\n' + 'Сценарий окончен' + '\n' + '-' * 20 + '\n')

# Ждем некоторое время, чтобы страница загрузок полностью загрузилась
time.sleep(2)

# Добавляем задержку в 5 секунд перед закрытием браузера
time.sleep(5)

driver.quit()