let blockCounter = 0; // Счетчик блоков
const maxBlocks = 5; // Максимальное количество блоков
const maxElements = 5; // Максимальное количество элементов в блоке





// Функция для добавления нового элемента в блок
function addElement(button) {
  const block = button.parentNode.parentNode; // Найти родительский блок
  const elements = block.querySelectorAll('.element'); // Найти все элементы в блоке

  const addElementButton = block.querySelector('.button-with-icon'); // Кнопка добавления нового элемента

  const newElement = document.createElement('div'); // Создать новый элемент
  newElement.className = 'element';
  newElement.innerHTML = `
        <div class="input-container">
          <input class="input-field" type="number" min="0" max="100" value="0">
        </div>
        <button class="delete-button" onclick="deleteElement(this)">x</button>
      `;

  block.insertBefore(newElement, addElementButton.parentNode); // Вставить новый элемент перед кнопкой добавления

  // Скрыть кнопку добавления элемента, если достигнут максимальный лимит элементов
  if (elements.length === maxElements - 1) {
    addElementButton.style.display = 'none';
  }
}

// Функция для добавления нового блока
function addBlock() {
  const blocks = document.querySelectorAll('.system-block .block'); // Найти все блоки

  blockCounter++; // Увеличить счетчик блоков
  const newBlock = document.createElement('div'); // Создать новый блок
  newBlock.className = 'block';
  newBlock.innerHTML = `
        <div class="block-title">Блок ${blockCounter}</div>
        <div class="button-container">
          <button class="button-with-icon" onclick="addElement(this)">
            <span class="icon"><i class="fas fa-plus"></i></span>
            Добавить новый элемент
          </button>
        </div>
        <button class="delete-block-button" onclick="deleteBlock(this)">Удалить блок</button>
        <div class="checkbox-container">
          <label><input type="radio" name="mode-${blockCounter}" class="mode-radio" checked> Параллельно</label>
          <label><input type="radio" name="mode-${blockCounter}" class="mode-radio"> Последовательно</label>
        </div>
      `;

  const addBlockButton = document.querySelector('#add-block-button'); // Кнопка добавления нового блока
  if (addBlockButton) {
    addBlockButton.parentNode.insertBefore(newBlock, addBlockButton); // Вставить новый блок перед кнопкой добавления блока

    // Скрыть кнопку добавления блока, если достигнут максимальный лимит блоков
    if (blocks.length === maxBlocks - 1) {
      addBlockButton.style.display = 'none';
    }
  } else {
    console.error('Add block button not found');
  }
}

// Функция для удаления элемента из блока
function deleteElement(button) {
  const element = button.parentNode; // Найти элемент
  const block = element.parentNode; // Найти родительский блок
  element.remove(); // Удалить элемент

  const addElementButton = block.querySelector('.button-with-icon'); // Кнопка добавления элемента
  addElementButton.style.display = 'inline-flex'; // Показать кнопку добавления элемента
}

// Функция для удаления блока
function deleteBlock(button) {
  const block = button.parentNode; // Найти блок
  block.remove(); // Удалить блок
  updateBlockTitles(); // Обновить заголовки блоков
  const addBlockButton = document.getElementById('add-block-button').parentNode; // Кнопка добавления блока
  addBlockButton.style.display = 'flex'; // Показать кнопку добавления блока
}

// Функция для обновления заголовков блоков после удаления блока
function updateBlockTitles() {
  const blocks = document.querySelectorAll('.system-block .block'); // Найти все блоки
  blockCounter = 0; // Сбросить счетчик блоков
  blocks.forEach((block, index) => {
    blockCounter++;
    const title = block.querySelector('.block-title');
    title.textContent = `Блок ${index + 1}`; // Обновить заголовок блока
  });
}

// Функция для отправки данных на сервер и получения надежности системы
async function fetchSystemReliability() {
  const blocks = document.querySelectorAll('.system-block .block'); // Найти все блоки
  const systemMode = document.querySelector('.checkbox-container-white input[type="radio"]:checked').parentNode.textContent.trim(); // Получить режим системы
  
  

  try {

    const systemData = buildSystemData(blocks, systemMode); // Построить данные системы

    const response = await postData('calculate/system_reliability', systemData); // Отправить данные на сервер

    if (response.ok) {
      const reliabilityData = JSON.parse(await response.json());
      console.log('Reliability data:', reliabilityData);
      displayReliabilityTables(reliabilityData); // Показать таблицы надежности
      document.getElementById('generate-pdf').style.display = 'inline-block'; // Показать кнопку генерации PDF
    } else {
      console.error('Failed to calculate system reliability', response.status, response.statusText);
    }
  } catch (error) {
    alert('Ошибка: ' + error.message); // Отобразить сообщение об ошибке в браузере
    const container = document.getElementById('Container-Table');
    container.innerHTML = '';
  }
}

// Функция для построения данных системы
function buildSystemData(blocks, systemMode) {
  const systemData = {
    systemMode: systemMode,
    blocks: []
  };

  blocks.forEach((block, index) => {
    const blockData = buildBlockData(block, index);
    systemData.blocks.push(blockData); // Добавить данные блока в данные системы
  });

  return systemData;
}

function buildBlockData(block, index) {
  const reliabilityInput = block.querySelector('.reliability-input');
  const reliabilityValue = parseFloat(reliabilityInput.value);

  // Проверка, что значение находится в диапазоне от 0 до 100
  if (reliabilityValue < 0 || reliabilityValue > 100 || isNaN(reliabilityValue)) {
    throw new Error('Недопустимое значение надежности блока ' + (index + 1) + ': ' + reliabilityValue);
  }

  return {
    id: block.dataset.id,
    name: block.querySelector('.block-name').textContent.trim(),
    reliability: reliabilityValue,
  };
}

// Функция для построения данных блока
function buildBlockData(block, index) {
  const elements = block.querySelectorAll('.element .input-field');
  const blockData = {
    blockNumber: index + 1,
    mode: block.querySelector('.checkbox-container input[type="radio"]:checked').parentNode.textContent.trim(),
    elements: []
  };

  elements.forEach(element => {
    const value = parseInt(element.value);
    if (isNaN(value) || value < 0 || value > 100) {
      throw new Error('Недопустимое значение надежности элемента в блоке ' + blockData.blockNumber + ': ' + element.value);
    }
    blockData.elements.push({ value });
  });

  return blockData;
}

// Функция для отправки данных на сервер
async function postData(url, data) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return response;
}

// Функция для отображения таблиц надежности
function displayReliabilityTables(data) {
  const container = document.getElementById('Container-Table');
  container.innerHTML = '';

  generateSystemTables(data); // Генерация таблиц системы
  generateBlockTables(data); // Генерация таблиц блоков

  displayTextElement(container, `Произведя ${data.num_trials} испытаний, получим, что в ${data.success_count} из них система работала безотказно. В качестве оценки искомой надежности Р примем относительную частоту Р*=${data.success_count}/${data.num_trials}=${data.system_probability}.`);
  displayTextElement(container, 'Найдем надежность системы Р аналитически. Вероятности безотказной работы блоков:');
  displayTextElement(container, 'P = ' + data.analytical);
  displayTextElement(container, `Искомая абсолютная погрешность равна |Р−P*| = ${data.dif}`);

  document.getElementById('generate-pdf').addEventListener('click', function() {
    const container = document.getElementById('Container-Table');
    const htmlContent = container.innerHTML;
  
    // Отправляем HTML на сервер
    sendHtmlToServer(htmlContent);
  });
  
}

function sendHtmlToServer(htmlContent) {
  fetch('/calculate/system_reliability/generate-pdf', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json; charset=UTF-8'
    },
    body: JSON.stringify({ html: htmlContent })
  })
  .then(response => {
    if (!response.ok) {
      return response.json().then(err => { throw new Error(err.error); });
    }
    return response.blob();
  })
  .then(blob => {
    const url = window.URL.createObjectURL(new Blob([blob], { type: 'application/pdf' }));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'generated.pdf');
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
  })
  .catch(error => {
    console.error('Error:', error);
  });
}




// Функция для генерации таблиц системы
function generateSystemTables(data) {
  let count = 0;
  for (const key in data.system) {
    generateTable(++count, data.system[key]);
  }
}

// Функция для генерации таблиц блоков
function generateBlockTables(data) {
  const countBlocks = Object.keys(data.system).length;

  const table = document.createElement('table');

  const firstRow = createFirstRowWithSpan(countBlocks, `Блоки - (${data.system_mode})`);
  table.appendChild(firstRow);

  const secondRow = createSecondRowWithBlockHeaders(countBlocks);
  table.appendChild(secondRow);

  appendIterationsToTable(data, table, countBlocks);

  const container = document.getElementById('Container-Table');
  container.appendChild(table);
}

// Функция для добавления итераций в таблицу
function appendIterationsToTable(data, table, countBlocks) {
  for (const key in data.system[Object.keys(data.system)[0]].iteration) {
    let row = document.createElement('tr');

    if (key == '49') {
      const cell_skip = generateSkipCells(2 + countBlocks);
      for (let i = 0; i < cell_skip.length; i++) {
        const cell = document.createElement('td');
        cell.textContent = cell_skip[i];
        row.appendChild(cell);
      }
      table.appendChild(row);
      row = document.createElement('tr');
    }

    let cell = document.createElement('td');
    cell.textContent = Number(key) + 1;
    row.appendChild(cell);

    for (const key1 in data.system) {
      cell = document.createElement('td');
      cell.textContent = getSymbolForBoolean(data.system[key1].iteration[key].blok_probability);
      row.appendChild(cell);
    }

    cell = document.createElement('td');
    cell.textContent = getSymbolForBoolean(data.blocks_choice[key]);
    row.appendChild(cell);

    table.appendChild(row);
  }
}

// Функция для отображения текстового элемента
function displayTextElement(container, text) {
  const textElement = document.createElement('p');
  textElement.classList.add('text-container');
  textElement.textContent = text;
  container.appendChild(textElement);
}

// Функция для генерации подзаголовков
function generateSubHeaders(elementCount, blockNumber) {
  const subHeaders = [];
  const startCharCode = 'A'.charCodeAt(0);

  for (let i = 0; i < elementCount; i++) {
    subHeaders.push(String.fromCharCode(startCharCode + i) + blockNumber);
  }

  return subHeaders;
}

// Функция для генерации ячеек со случайными значениями
function generateRandomValueCells(iterations) {
  return iterations.map(item => Math.round(item.random_value * 100) + '%');
}

// Функция для получения символа для булевого значения
function getSymbolForBoolean(value) {
  return value ? '+' : '-';
}

// Функция для генерации ячеек с проверками
function generateCheckCells(iterations) {
  return iterations.map(item => getSymbolForBoolean(item.probability));
}

// Функция для генерации пропущенных ячеек
function generateSkipCells(count) {
  return Array(count).fill('...');
}

// Функция для генерации таблицы
function generateTable(blockNumber, details) {
  const elementCount = details.iteration[0].iteration.length;

  const table = document.createElement('table');

  table.appendChild(createFirstRow(blockNumber, details.mode, elementCount));
  table.appendChild(createSecondRow(elementCount));
  table.appendChild(createThirdRow(elementCount, blockNumber));

  for (const key in details.iteration) {
    createDataRow(table, key, details.iteration[key], elementCount);
  }

  const container = document.getElementById('Container-Table');
  container.appendChild(table);
}

// Функция для создания первой строки таблицы
function createFirstRow(blockNumber, mode, elementCount) {
  const firstRow = document.createElement('tr');
  const firstRowCell = document.createElement('td');
  firstRowCell.colSpan = elementCount * 2 + 2;
  firstRowCell.textContent = `Блок ${blockNumber} - (${mode})`;
  firstRow.appendChild(firstRowCell);

  return firstRow;
}

// Функция для создания первой строки таблицы с объединением ячеек
function createFirstRowWithSpan(colSpan, textContent) {
  const firstRow = document.createElement('tr');
  const cell = document.createElement('td');
  cell.rowSpan = 2;
  cell.textContent = 'Номер испытания';
  firstRow.appendChild(cell);

  const firstRowCell = document.createElement('td');
  firstRowCell.colSpan = colSpan;
  firstRowCell.textContent = textContent;
  firstRow.appendChild(firstRowCell);

  const secondCell = document.createElement('td');
  secondCell.rowSpan = 2;
  secondCell.textContent = 'Система';
  firstRow.appendChild(secondCell);

  return firstRow;
}

// Функция для создания второй строки таблицы
function createSecondRow(elementCount) {
  const secondRow = document.createElement('tr');
  const headers = ['Номер испытания', 'Случайные числа моделирующие элементы', 'Элементы', 'Блок'];
  
  headers.forEach((header, index) => {
    const cell = document.createElement('td');
    if (index === 0 || index === 3) {
      cell.rowSpan = 2;
    } else if (index === 1 || index === 2) {
      cell.colSpan = elementCount;
    }
    cell.textContent = header;
    secondRow.appendChild(cell);
  });

  return secondRow;
}

// Функция для создания второй строки таблицы с заголовками блоков
function createSecondRowWithBlockHeaders(countBlocks) {
  const secondRow = document.createElement('tr');

  for (let i = 0; i < countBlocks; i++) {
    const cell_block = document.createElement('td');
    cell_block.textContent = `Блок ${i + 1}`;
    secondRow.appendChild(cell_block);
  }

  return secondRow;
}

// Функция для создания третьей строки таблицы
function createThirdRow(elementCount, blockNumber) {
  const thirdRow = document.createElement('tr');
  const subHeaders = [
    ...generateSubHeaders(elementCount, blockNumber),
    ...generateSubHeaders(elementCount, blockNumber)
  ];
  
  subHeaders.forEach(subHeader => {
    const cell = document.createElement('td');
    cell.textContent = subHeader;
    thirdRow.appendChild(cell);
  });

  return thirdRow;
}

// Функция для создания строки с данными
function createDataRow(table, key, iterationData, elementCount) {
  let row = document.createElement('tr');

  if (key === '49') {
    const skipCells = generateSkipCells(elementCount * 2 + 2);
    skipCells.forEach(cellData => {
      const cell = document.createElement('td');
      cell.textContent = cellData;
      row.appendChild(cell);
    });
    table.appendChild(row);
    row = document.createElement('tr');
  }

  const cells = [
    Number(key) + 1,
    ...generateRandomValueCells(iterationData.iteration),
    ...generateCheckCells(iterationData.iteration),
    getSymbolForBoolean(iterationData['blok_probability'])
  ];

  cells.forEach(cellData => {
    const cell = document.createElement('td');
    cell.textContent = cellData;
    row.appendChild(cell);
  });

  table.appendChild(row);
}