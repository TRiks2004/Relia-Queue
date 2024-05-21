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

    async function calculateData() {
      const blocks = document.querySelectorAll('.system-block .block');
      const systemMode = document.querySelector('.checkbox-container-white input[type="radio"]:checked').parentNode.textContent.trim();
      let result = {
        systemMode: systemMode,
        blocks: []
      };
    
      blocks.forEach((block, index) => {
        let blockData = {
          blockNumber: index + 1,
          mode: block.querySelector('.checkbox-container input[type="radio"]:checked').parentNode.textContent.trim(),
          elements: []
        };
    
        const elements = block.querySelectorAll('.element .input-field');
        elements.forEach((element) => {
          blockData.elements.push({
            value: parseInt(element.value)
          });
        });
    
        result.blocks.push(blockData);
      });
    
      console.log(JSON.stringify(result, null, 2));
    
      try {
        const response = await fetch('calculate/system_reliability', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(result)
        });
    
        if (response.ok) {
          const responseData = await response.json();
          console.log('System Reliability:', responseData);
        } else {
          console.error('Failed to calculate system reliability', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error:', error);
      }
    }
    