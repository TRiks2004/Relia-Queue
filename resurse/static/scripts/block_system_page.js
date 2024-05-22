let blockCounter = 0;
const maxBlocks = 5;
const maxElements = 5;

function addElement(button) {
  const block = button.parentNode.parentNode;
  const elements = block.querySelectorAll('.element');

  const addElementButton = block.querySelector('.button-with-icon');

  const newElement = document.createElement('div');
  newElement.className = 'element';
  newElement.innerHTML = `
        <div class="input-container">
          <input class="input-field" type="number" min="0" max="100" value="0">
        </div>
        <button class="delete-button" onclick="deleteElement(this)">x</button>
      `;

  block.insertBefore(newElement, addElementButton.parentNode);

  if (elements.length === maxElements - 1) {
    addElementButton.style.display = 'none';
  }
}

function addBlock() {
  const blocks = document.querySelectorAll('.system-block .block');

  blockCounter++;
  const newBlock = document.createElement('div');
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

  const addBlockButton = document.querySelector('.system-block > .button-container');
  addBlockButton.parentNode.insertBefore(newBlock, addBlockButton);

  if (blocks.length === maxBlocks - 1) {
    addBlockButton.style.display = 'none';
  }
}

function deleteElement(button) {
  const element = button.parentNode;
  const block = element.parentNode;
  element.remove();

  const addElementButton = block.querySelector('.button-with-icon');
  addElementButton.style.display = 'inline-flex';
}

function deleteBlock(button) {
  const block = button.parentNode;
  block.remove();
  updateBlockTitles();
  const addBlockButton = document.getElementById('add-block-button').parentNode;
  addBlockButton.style.display = 'flex';
}

function updateBlockTitles() {
  const blocks = document.querySelectorAll('.system-block .block');
  blockCounter = 0;
  blocks.forEach((block, index) => {
    blockCounter++;
    const title = block.querySelector('.block-title');
    title.textContent = `Блок ${index + 1}`;
  });
}

async function fetchSystemReliability() {
  const blocks = document.querySelectorAll('.system-block .block');
  const systemMode = document.querySelector('.checkbox-container-white input[type="radio"]:checked').parentNode.textContent.trim();
  
  const systemData = buildSystemData(blocks, systemMode);

  try {
    const response = await postData('calculate/system_reliability', systemData);

    if (response.ok) {
      const reliabilityData = JSON.parse(await response.json());
      console.log('Reliability data:', reliabilityData);
      displayReliabilityTables(reliabilityData);
    } else {
      console.error('Failed to calculate system reliability', response.status, response.statusText);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

function buildSystemData(blocks, systemMode) {
  const systemData = {
    systemMode: systemMode,
    blocks: []
  };

  blocks.forEach((block, index) => {
    const blockData = buildBlockData(block, index);
    systemData.blocks.push(blockData);
  });

  return systemData;
}

function buildBlockData(block, index) {
  const blockData = {
    blockNumber: index + 1,
    mode: block.querySelector('.checkbox-container input[type="radio"]:checked').parentNode.textContent.trim(),
    elements: []
  };

  const elements = block.querySelectorAll('.element .input-field');
  elements.forEach((element) => {
    blockData.elements.push({ value: parseInt(element.value) });
  });

  return blockData;
}

async function postData(url, data) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return response;
}

function displayReliabilityTables(data) {
  const container = document.getElementById('Container-Table');
  container.innerHTML = '';

  let count = 0;
  for (const key in data.system) {
   
    generateTable(++count, data.system[key]);
  }

  generateTableBlocks(data);


  // Произведя 50 испытаний, получим, что в 28 из них система работала безотказно. 
  // В качестве оценки искомой надежности Р примем относительную частоту Р*=28/50=0.56.

  const textElement = document.createElement('p');
  textElement.classList.add('text-container');

  const content = `Произведя ${data['num_trials']} испытаний, получим, что в ${data['success_count']} из них система работала безотказно. В качестве оценки искомой надежности Р примем относительную частоту Р*=${data['success_count']}/${data['num_trials']}=${data['system_probability']}.`;

  textElement.textContent = content;
  container.appendChild(textElement);
}

function generateTableBlocks(data) {

  console.log(data);

  const countBlocks = Object.keys(data.system).length;

  const table = document.createElement('table');

  const firstRow = document.createElement('tr');
  
  const cell = document.createElement('td');
  cell.rowSpan = 2;
  cell.textContent = 'Номер испытания';
  firstRow.appendChild(cell);

  const firstRowCell = document.createElement('td');
  firstRowCell.colSpan = countBlocks;
  firstRowCell.textContent = `Блоки - (${data.system_mode})`;
  firstRow.appendChild(firstRowCell);

  const cell2 = document.createElement('td');
  cell2.rowSpan = 2;
  cell2.textContent = 'Система';
  firstRow.appendChild(cell2);

  table.appendChild(firstRow);


  const SecondRow = document.createElement('tr');

  for (let i = 0; i < countBlocks; i++) {
    const cell_block = document.createElement('td');
    cell_block.textContent = `Блок ${i + 1}`;
    SecondRow.appendChild(cell_block);
  }

  table.appendChild(SecondRow);


  let system_create = false;

  for (const key in data.system[Object.keys(data.system)[0]].iteration) {

    let row = document.createElement('tr');

    

    if (key == '49'){
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
  // for (const key in data) {
  //   
    

  //   const cells = []

  //   
    
  //   row.appendChild(cell);
  // }


  const container = document.getElementById('Container-Table');
  container.appendChild(table);
}



function generateSubHeaders(elementCount, blockNumber) {
  const subHeaders = [];
  const startCharCode = 'A'.charCodeAt(0);

  for (let i = 0; i < elementCount; i++) {
    subHeaders.push(String.fromCharCode(startCharCode + i) + blockNumber);
  }

  return subHeaders;
}

function generateRandomValueCells(iterations) {
  return iterations.map(item => Math.round(item.random_value * 100) + '%');
}

function getSymbolForBoolean(value) {
  return value ? '+' : '-';
}

function generateCheckCells(iterations) {
  return iterations.map(item => getSymbolForBoolean(item.probability));
}

function generateSkipCells(count) {
  return Array(count).fill('...');
}

function generateTable(blockNumber, details) {
  console.log(details);
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

function createFirstRow(blockNumber, mode, elementCount) {
  const firstRow = document.createElement('tr');
  const firstRowCell = document.createElement('td');
  firstRowCell.colSpan = elementCount * 2 + 2;
  firstRowCell.textContent = `Блок ${blockNumber} - (${mode})`;
  firstRow.appendChild(firstRowCell);

  return firstRow;
}

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

function createDataRow(table, key, iterationData, elementCount) {
  let row = document.createElement('tr');

  // Добавляем ячейки с '...' для ключа '49'
  if (key === '49') {
    const skipCells = generateSkipCells(elementCount * 2 + 2);
    skipCells.forEach(cellData => {
      const cell = document.createElement('td');
      cell.textContent = cellData;
      row.appendChild(cell);
    });
    table.appendChild(row);

    row = document.createElement('tr')
  }

  // Добавляем данные для текущего ключа
  
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


