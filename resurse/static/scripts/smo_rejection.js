async function refusalSolve() {
  // Получаем значения из input-элементов на странице
  const intensityInput = document.getElementById('intensityInput').value;
  const serviceTimeInput = document.getElementById('serviceTimeInput').value;
  const simulationDurationInput = document.getElementById('simulationDurationInput').value;
  const channelCountInput = document.getElementById('channelCountInput').value;
  const simulationCountInput = document.getElementById('simulationCountInput').value;

  // Преобразуем значения channelCountInput и simulationCountInput в целые числа
  const channelCount = parseInt(channelCountInput);
  const simulationCount = parseInt(simulationCountInput);

  // Проверяем, что количество симуляций - целое число больше 0
  if (isNaN(simulationCount) || simulationCount <= 0) {
      alert("Ошибка: Количество симуляций не может быть символом или числом меньше 0");
      return;
  }

  // Проверяем, что количество каналов - целое число больше 0
  if (isNaN(channelCount) || channelCount <= 0) {
      alert("Ошибка: Количество каналов не может быть символом или числом меньше 0");
      return;
  }

  // Проверяем, что количество каналов не превышает 5
  if (channelCount > 5) {
      alert("Ошибка: число серверов (каналов) ограничено до 5.");
      return;
  }

  // Создаем объект formData с параметрами для симуляции
  const formData = {
      T: parseFloat(simulationDurationInput),
      num_channels: channelCount,
      service_time: parseFloat(serviceTimeInput),
      num_iterations: simulationCount,
      alfa: parseFloat(intensityInput),
  };

  try {
      // Отправляем POST-запрос на сервер для запуска симуляции
      const response = await fetch('/cfr-refusal', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
      });

      if (response.ok) {
          // Если запрос успешен, парсим JSON-ответ от сервера
          const responseData = await response.json();
          console.log(responseData);
          console.log(typeof(responseData));

          // Создаем массив заголовков столбцов таблиц
          const list = ["Индекс", "Случайное число", "МЕЖ", "Время программы", "Обслужено", "Отказов"];

          // Генерируем таблицы и заполняем их данными из responseData
          generateTables(list, simulationCount, responseData);
          goToResult(); // Переходим к результатам

          // Добавляем обработчики событий для кнопок сохранения в Excel и TXT
          document.getElementById('saveExcelButton').addEventListener('click', function() {
              downloadExcel(responseData);
          });
          document.getElementById('saveTxtButton').addEventListener('click', function() {
              downloadTextFile(responseData);
          });

      } else {
          console.error('Failed to run simulation', response.status, response.statusText);
      }
  } catch (error) {
      console.error('Error:', error);
  }
}

  
  function generateTables(list, sim_count, responseData) {
      console.log('Starting generateTables');
      console.log('Response data:', responseData);
  
      // Удаляем существующие таблицы
      var existingTables = document.querySelectorAll(".t-table");
      for (var i = 0; i < existingTables.length; i++) {
          existingTables[i].remove();
      }
  
      // Удаляем существующие блоки с номерами итераций
      var existingIterationNumbers = document.querySelectorAll(".iteration-number");
      for (var i = 0; i < existingIterationNumbers.length; i++) {
          existingIterationNumbers[i].remove();
      }
  
      // Удаляем существующие блоки с краткими итогами по итерациям
      var existingSummaries = document.querySelectorAll(".summary");
      for (var i = 0; i < existingSummaries.length; i++) {
          existingSummaries[i].remove();
      }
  
      // Удаляем существующий блок с общими результатами
      var totalSummaryDiv = document.querySelector(".total-summary");
      if (totalSummaryDiv) {
          totalSummaryDiv.remove();
      }
  
      var totalServedRequests = 0;
      var totalRejectedRequests = 0;
  
      for (var i = 0; i < responseData.length; i++) {
          var table = document.createElement("table");
          table.classList.add("t-table");
          table.setAttribute("border", "1");
          table.style.textAlign = "center";
  
          var tableHeaderRow = document.createElement("tr");
  
          // Добавляем номер итерации над таблицей
          var iterationNumber = document.createElement("div");
          iterationNumber.textContent = "Итерация №" + responseData[i].iteration;
          iterationNumber.classList.add("iteration-number");
          iterationNumber.style.color = "black"; // Установим черный цвет текста
          document.body.appendChild(iterationNumber);
  
          // Добавляем заголовки столбцов
          for (var j = 0; j < list.length; j++) {
              var th = document.createElement("th");
              th.textContent = list[j];
              tableHeaderRow.appendChild(th);
          }
  
          var channelCount = parseInt(document.getElementById("channelCountInput").value);
  
          // Добавляем заголовки столбцов серверов
          for (var j = 1; j <= channelCount; j++) {
              var th = document.createElement("th");
              th.textContent = "Сервер " + j;
              tableHeaderRow.appendChild(th);
          }
  
          table.appendChild(tableHeaderRow);
  
          // Добавляем строки с результатами запросов
          for (var k = 0; k < responseData[i].request_times.length; k++) {
              var rowData = responseData[i].request_times[k];
              var row = document.createElement("tr");
  
              for (var key in rowData) {
                  var cell = document.createElement("td");
                  cell.textContent = rowData[key];
                  row.appendChild(cell);
              }
  
              table.appendChild(row);
          }
  
          table.style.marginBottom = "20px";
          document.body.appendChild(table);
  
          // Добавляем блок с количеством обслуженных и отклоненных заявок
          var summaryDiv = document.createElement("div");
          summaryDiv.classList.add("summary");
          summaryDiv.textContent = "Количество Обслуженных заявок: " + responseData[i].served_requests + ", Количество отказов: " + responseData[i].rejected_requests;
          summaryDiv.style.color = "black"; // Установим черный цвет текста
          summaryDiv.style.marginBottom = "40px";
          document.body.appendChild(summaryDiv);
  
          // Суммируем обслуженные и отклоненные заявки
          totalServedRequests += responseData[i].served_requests;
          totalRejectedRequests += responseData[i].rejected_requests;
  
          console.log('Added table and summary for iteration', responseData[i].iteration);
      }
  
      // Вычисляем среднее количество обслуженных заявок на одну симуляцию
      var averageServedRequests = totalServedRequests / responseData.length;
  
      // Выводим общее количество обслуженных и отклоненных заявок
      var totalSummaryDiv = document.createElement("div");
      totalSummaryDiv.classList.add("total-summary");
      totalSummaryDiv.textContent = "Общее количество Обслуженных заявок: " + totalServedRequests + ", Общее количество отказов: " + totalRejectedRequests + ", Среднее количество обслуженных заявок на симуляцию: " + averageServedRequests.toFixed(2);
      totalSummaryDiv.style.color = "black"; // Установим черный цвет текста
      totalSummaryDiv.style.marginTop = "60px";
      document.body.appendChild(totalSummaryDiv);
  
      console.log('Added total summary');
  }    

// Функция скачивания Excel
function downloadExcel(responseData) {
  const channelCount = parseInt(document.getElementById('channelCountInput').value);
  let csvContent = "data:text/csv;charset=utf-8,";

  // Заголовок CSV
  csvContent += "Index,Random Number,MEZH,Program Time,Served,Refusals";

  // Добавляем заголовки для каждого канала
  for (let i = 1; i <= channelCount; i++) {
      csvContent += `,Server ${i}`;
  }

  csvContent += "\n";

  // Данные из responseData
  responseData.forEach(iteration => {
      iteration.request_times.forEach(rowData => {
          csvContent += Object.values(rowData).join(",") + ",";
          // Добавляем пустые значения для каналов, если они отсутствуют в данных
          for (let i = 0; i < channelCount; i++) {
              csvContent += ",";
          }
          csvContent += "\n";
      });
      csvContent += "\n"; // Разделитель между итерациями
  });

  // Создаем ссылку для скачивания
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", "simulation_data.csv");
  document.body.appendChild(link);

  // Симулируем клик по ссылке для автоматического скачивания
  link.click();
}


function generateTextContent(list, responseData, channelCount) {
  let textContent = '';

  for (let i = 0; i < responseData.length; i++) {
      // Добавляем номер итерации
      textContent += `Итерация №${responseData[i].iteration}\n`;

      // Добавляем заголовки столбцов, включая каналы
      const columns = list.concat(Array.from({ length: channelCount }, (_, index) => `Сервер ${index + 1}`));
      textContent += columns.join('\t') + '\n';

      // Добавляем строки с результатами запросов
      for (let k = 0; k < responseData[i].request_times.length; k++) {
          const rowData = responseData[i].request_times[k];
          const rowValues = Object.values(rowData);
          // Добавляем пустые значения для каждого канала
          const emptyChannels = Array.from({ length: channelCount }, () => '');
          textContent += rowValues.concat(emptyChannels).join('\t') + '\n';
      }

      // Добавляем блок с количеством обслуженных и отклоненных заявок
      textContent += `Количество Обслуженных заявок: ${responseData[i].served_requests}, Количество отказов: ${responseData[i].rejected_requests}\n\n`;
  }

  // Добавляем общее количество обслуженных и отклоненных заявок
  const totalServedRequests = responseData.reduce((total, item) => total + item.served_requests, 0);
  const totalRejectedRequests = responseData.reduce((total, item) => total + item.rejected_requests, 0);
  textContent += `Общее количество Обслуженных заявок: ${totalServedRequests}, Общее количество отказов: ${totalRejectedRequests}\n`;

  return textContent;
}

function downloadTextFile(responseData) {
  // Массив заголовков столбцов
  const list = ["Индекс", "Случайное число", "МЕЖ", "Время программы", "Обслужено", "Отказов"];

  // Получаем количество каналов из input-элемента
  const channelCount = parseInt(document.getElementById('channelCountInput').value);

  // Генерируем содержимое текстового файла
  const textContent = generateTextContent(list, responseData, channelCount);

  // Создаем Blob из сгенерированного текстового содержимого
  const blob = new Blob([textContent], { type: 'text/plain' });

  // Создаем временный URL для Blob
  const url = URL.createObjectURL(blob);

  // Создаем ссылку для скачивания файла
  const a = document.createElement('a');
  a.href = url;
  a.download = 'simulation_results.txt';

  // Добавляем ссылку на страницу, чтобы можно было кликнуть по ней
  document.body.appendChild(a);
  a.click(); // Симулируем клик по ссылке для начала скачивания

  // Удаляем ссылку со страницы и освобождаем временный URL
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}