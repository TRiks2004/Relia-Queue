const goToTheory = () => {
    const theoryTitle = document.getElementById("theoryTitle");
    theoryTitle.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest' });
}

const goToForm = () => {
    const formTitle = document.getElementById("formTitle");
    formTitle.scrollIntoView({ behavior: 'smooth' });
}

const goToResult = () => {
    const resultTitle = document.getElementById("saveContainer");
    resultTitle.scrollIntoView({ behavior: 'smooth' });
}


async function refusalSolve() {
    const intensityInput = document.getElementById('intensityInput').value;
    const serviceTimeInput = document.getElementById('serviceTimeInput').value;
    const simulationDurationInput = document.getElementById('simulationDurationInput').value;
    const channelCountInput = document.getElementById('channelCountInput').value;
    const simulationCountInput = document.getElementById('simulationCountInput').value;

    const channelCount = parseInt(channelCountInput);
    const simulationCount = parseInt(simulationCountInput);

    if (isNaN(simulationCount) || simulationCount <= 0) {
        alert("Ошибка: Количество симуляций не может быть символом или числом меньше 0");
        return;
    }

    if (isNaN(channelCount) || channelCount <= 0) {
        alert("Ошибка: Количество каналов не может быть символом или числом меньше 0");
        return;
    }

    if (channelCount > 5) {
        alert("Ошибка: число серверов (каналов) ограничено до 5.");
        return;
    }

    const formData = {
        T: parseFloat(simulationDurationInput),
        num_channels: channelCount,
        service_time: parseFloat(serviceTimeInput),
        num_iterations: simulationCount,
        alfa: parseFloat(intensityInput),
    };

    try {
        const response = await fetch('/cfr-refusal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        if (response.ok) {
            const responseData = await response.json(); // парсим JSON
            console.log(responseData);
            console.log(typeof(responseData));

            const list = ["Индекс", "Случайное число", "МЕЖ", "Время программы", "Обслужено", "Отказов"];
            generateTables(list, simulationCount, responseData); // передаем responseData
            goToResult();
        } else {
            console.error('Failed to run simulation', response.status, response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }}
    
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

    async function downloadPDF() {
        const intensityInput = document.getElementById('intensityInput').value;
        const serviceTimeInput = document.getElementById('serviceTimeInput').value;
        const simulationDurationInput = document.getElementById('simulationDurationInput').value;
        const channelCountInput = document.getElementById('channelCountInput').value;
        const simulationCountInput = document.getElementById('simulationCountInput').value;
    
        const channelCount = parseInt(channelCountInput);
        const simulationCount = parseInt(simulationCountInput);
    
        if (isNaN(simulationCount) || simulationCount <= 0) {
            alert("Ошибка: Количество симуляций должно быть положительным числом");
            return;
        }
    
        if (isNaN(channelCount) || channelCount <= 0) {
            alert("Ошибка: Количество каналов должно быть положительным числом");
            return;
        }
    
        if (channelCount > 5) {
            alert("Ошибка: количество серверов (каналов) ограничено до 5.");
            return;
        }
    
        const formData = {
            T: parseFloat(simulationDurationInput),
            num_channels: channelCount,
            service_time: parseFloat(serviceTimeInput),
            num_iterations: simulationCount,
            alfa: parseFloat(intensityInput),
            response_format: 'pdf', // Указываем формат ответа как PDF
        };
    
        try {
            const response = await fetch('/cfr-refusal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });
    
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
    
                // Создаем ссылку для скачивания PDF-файла
                const a = document.createElement('a');
                a.href = url;
                a.download = 'simulation_results.pdf';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            } else {
                console.error('Failed to retrieve PDF', response.status, response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
    
    
    
function unlimitedSolve() {
    var channelCount = parseInt(document.getElementById("channelCountInput").value);
    var iterationCount = parseInt(document.getElementById("iterationCountInput").value);

    if (isNaN(iterationCount) || iterationCount <= 0) {
        alert("Ошибка: Количество итераций не может быть символом или числом меньше 0");
        return;
    }
    if (isNaN(channelCount) || channelCount <= 0) {
        alert("Ошибка: Количество потоков не может быть символом или числом меньше 0");
        return;
    }
    if (channelCount > 5){
        alert("Ошибка: число серверов (каналов) ограничено до 5.")
    }
    else{
        list = ["Индекс", "Случайное значение", "Интервал между заявками", "Время обслуживания"];
        generateTables(list, iterationCount);
        goToResult();
    }
}

function blockSystemSolve(){
    // Get input values
    var probability = parseFloat(document.getElementById("probabilityInput").value);

    if (isNaN(probability) || probability <= 0) {
        alert("Ошибка: Вероятность не может быть символом или числом меньше 0");
        return;
    }
    if (probability > 1) {
        alert("Ошибка: Вероятность не может быть больше 1");
        return;    
    }
}