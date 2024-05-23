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

# Выбираем кнопку "Многоканальные СМО с отказами"
monte_button = buttons[2]

# Выполняем скролл до конца страницы
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
print('\n' + '-' * 20 + '\n' + 'Выполнен скролл' + '\n' + '-' * 20 + '\n')
time.sleep(2)

# Нажимаем кнопку
monte_button.click()
print('\n' + '-' * 20 + '\n' + 'Нажата кнопка "Оценка надежности системы методом Монте-Карло"' + '\n' + '-' * 20 + '\n')
time.sleep(1)

# Вывод того, что мы перешли на страницу "СМО с неограниченными очередями"
print('\n' + '-' * 20 + '\n' + 'Переход на страницу "Оценка надежности системы методом Монте-Карло"' + '\n' + '-' * 20 + '\n')
time.sleep(2)

# Находим все элементы с атрибутом class name='skip-button'
buttons = driver.find_elements(by='class name', value = 'skip-button')

# Выбираем кнопку "Ввод параметров"
input_button = buttons[1]

# Нажимаем кнопку
input_button.click()
print('\n' + '-' * 20 + '\n' + 'Нажата кнопка "Ввод параметров"' + '\n' + '-' * 20 + '\n')
time.sleep(2)

# Заполняем форму на основе данных из json файла
with open('options/option3/data.json', 'r') as f:
    data = json.load(f)

for key, value in data['reliabilities'].items():
    add_block_button = driver.find_element(by='id', value='add-block-button')
    add_block_button.click()
    print('\n' + '-' * 20 + '\n' + 'Нажата кнопка "Добавить блок"' + '\n' + '-' * 20 + '\n')
    
    # Делаем скролл чуть ниже
    driver.execute_script('window.scrollTo(0, 2600)')

    block = driver.find_elements(by='css selector', value='div.block')[-1]  # Находим только что созданный блок
    element_index = 0
    for element in value:
        add_element_button = block.find_element(by='css selector', value='div.button-container-block > button')
        driver.execute_script('arguments[0].click();', add_element_button)
        print('\n' + '-' * 20 + '\n' + 'Нажата кнопка "Добавить элемент"' + '\n' + '-' * 20 + '\n')
        time.sleep(1)

        input_elements = block.find_elements(by='class name', value='input-field')
        if element_index < len(input_elements):
            input_elements[element_index].clear()
            input_elements[element_index].send_keys(element)
            element_index += 1
            print('\n' + '-' * 20 + '\n' + 'Ввод элемента' + '\n' + '-' * 20 + '\n')
            time.sleep(1)

time.sleep(3)

# Поставим последовательное подключение в первом блоке
sequence_radio = driver.find_element(by='xpath', value='/html/body/div[3]/div[2]/div[2]/div[1]/div[6]/label[2]/input')
sequence_radio.click()
print('\n' + '-' * 20 + '\n' + 'Нажата кнопка "Последовательное подключение"' + '\n' + '-' * 20 + '\n')
time.sleep(2)

# Выполняем скролл, чтобы была видна кнопка
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
print('\n' + '-' * 20 + '\n' + 'Выполнен скролл' + '\n' + '-' * 20 + '\n')
time.sleep(2)

# Находим кнопку "Вычислить"
solve_button = driver.find_element(by='class name', value = 'calculate-button')

# Нажимаем кнопку
solve_button.click()
print('\n' + '-' * 20 + '\n' + 'Нажата кнопка "Решить"' + '\n' + '-' * 20 + '\n')

# Выводим сообщение после решения
print('\n' + '-' * 20 + '\n' + 'Вывод результатов' + '\n' + '-' * 20 + '\n')
time.sleep(4)

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
    scroll_step = 40  # Изменение координаты Y после каждой паузы

    while True:
        for i in range(scroll_y, last_height, scroll_step):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(SCROLL_PAUSE_TIME)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# Вызов функции для плавного скролла
smooth_scroll()

time.sleep(3)

# Находим кнопку "Сохранить решение в PDF"
pdf_button = driver.find_element(by='id', value = 'generate-pdf')

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