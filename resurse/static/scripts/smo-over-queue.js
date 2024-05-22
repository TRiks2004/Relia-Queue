// Сохранение таблиц в PDF
function saveTablesToPDF() {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  // Поиск всех таблиц с классом "t-table"
  const tables = document.querySelectorAll(".t-table");

  if (tables.length === 0) {
      alert("На странице нет таблиц для сохранения в PDF.");
      return;
  }

  let currentY = 10; // Начальная позиция по Y

  tables.forEach((table, index) => {
      // Добавление заголовка для каждой симуляции
      doc.text("Simulation " + (index + 1), 10, currentY);
      currentY += 10; // Добавление пробела после заголовка

      // Добавление таблицы с отступом
      doc.autoTable({
          html: table,
          startY: currentY,
          margin: { top: 10 } // Добавление отступа сверху таблицы
      });

      currentY = doc.lastAutoTable.finalY + 20; // Обновление текущей позиции по Y, добавление пробела после таблицы
  });

  doc.save("tables.pdf");
}

// Генерация таблиц результатов симуляции
function generateCFRTables(list, sim_count, simulation_data, num_threads) {
  // Удаление существующих таблиц
  var existingTables = document.querySelectorAll(".t-table");
  for (var i = 0; i < existingTables.length; i++) {
      existingTables[i].remove();
  }

  // Удаление существующего div с верхним отступом
  var existingDiv = document.querySelector(".top-margin-div");
  if (existingDiv) {
      existingDiv.remove();
  }

  for (var i = 0; i < simulation_data.results.length; i++) {
      var table = document.createElement("table");
      table.classList.add("t-table");
      table.setAttribute("border", "1");
      table.style.textAlign = "center";

      var tableRow = document.createElement("tr");

      // Добавление номера симуляции выше таблицы
      var simulationNumber = document.createElement("div");
      simulationNumber.textContent = "Simulation" + (i + 1);
      simulationNumber.classList.add("simulation-number");
      table.appendChild(simulationNumber);

      // Добавление заголовков
      for (var j = 0; j < list.length; j++) {
          var th = document.createElement("th");
          th.textContent = list[j];
          tableRow.appendChild(th);
      }

      // Добавление столбцов серверов
      for (var j = 1; j <= num_threads; j++) {
          var th = document.createElement("th");
          th.textContent = "thread " + j;
          tableRow.appendChild(th);
      }

      table.appendChild(tableRow);

      // Добавление временных меток запросов
      for (var k = 0; k < simulation_data.results[i].iterations.length; k++) {
          var rowData = simulation_data.results[i].iterations[k];
          var row = document.createElement("tr");

          for (var key in rowData) {
              if (key !== 'server_times') {
                  var cell = document.createElement("td");
                  cell.textContent = rowData[key];
                  row.appendChild(cell);
              }
          }

          // Добавление времени обработки серверов
          for (var j = 0; j < num_threads; j++) {
              var cell = document.createElement("td");
              cell.textContent = rowData.server_times[j];
              row.appendChild(cell);
          }

          table.appendChild(row);
      }

      // Добавление строки с ожидаемым значением
      var expectedValueRow = document.createElement("tr");
      var expectedValueCell = document.createElement("td");
      expectedValueCell.setAttribute("colspan", list.length + num_threads);
      expectedValueCell.textContent = "Expected value: " + simulation_data.results[i].expected_value;
      expectedValueRow.appendChild(expectedValueCell);
      table.appendChild(expectedValueRow);

      table.style.marginBottom = "40px";
      document.body.appendChild(table);
  }

  // Добавление div с верхним отступом 30px
  var div = document.createElement("div");
  div.classList.add("top-margin-div");
  div.style.marginTop = "30px";
  document.body.appendChild(div);
}

// Асинхронная функция для выполнения симуляции
async function unlimitedSolve() {
  var serviceTime = parseFloat(document.getElementById("serviceTimeInput").value);
  var maxSimulationTime = parseFloat(document.getElementById("maxSimulationTimeInput").value);
  var alpha = parseFloat(document.getElementById("parameterInput").value);
  var channelCount = parseInt(document.getElementById("channelCountInput").value);
  var iteration = parseInt(document.getElementById("iterationCountInput").value);

  if (!serviceTime || !maxSimulationTime || !alpha || !channelCount || !iteration){
      alert("Ошибка: все поля ввода должны быть заполнены.");
      return;
  }

  if (isNaN(serviceTime) || serviceTime < 0 ||
      isNaN(maxSimulationTime) || maxSimulationTime < 0 ||
      isNaN(alpha) || alpha < 0 ||
      isNaN(channelCount) || channelCount < 0 ||
      isNaN(iteration) || iteration < 0) {
      alert("Ошибка: Пожалуйста, убедитесь, что все введенные значения являются числами и больше нуля.");
      return;
  }
  if (channelCount > 5){
      alert("Ошибка: число серверов (каналов) ограничено до 5.");
      return;
  }
  if (iteration > 100){
      alert("Ошибка: число итераций ограничено до 100.");
      return;
  }

  const formData = {
      serviceTime: serviceTime,
      maxSimulationTime: maxSimulationTime,
      alpha: alpha,
      channelCount: channelCount,
      iterationCount: iteration,
  };

  try {
      // Отправка POST-запроса на сервер с данными формы
      const response = await fetch('/cfr-unlimited', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
      });
  
      // Проверка, успешно ли прошел запрос
      if (response.ok) {
          // Если запрос успешен, преобразование ответа в JSON
          const data = await response.json();
          console.log(data);
  
          // Определение списка заголовков для таблицы
          const list = ["index", "random_value", "request_time", "service_time"];
          
          // Генерация таблиц с результатами симуляции
          generateCFRTables(list, iteration, data, channelCount);
  
          // Переход к разделу с результатами
          goToResult();
      } else {
          // Если запрос неуспешен, вывод ошибки в консоль
          console.log('Failed to run simulation: ', response.status, response.statusText);
      }
  } catch (error) {
      // Обработка ошибок, возникших при выполнении запроса
      console.log('Error: ', error);
  }
  
}
