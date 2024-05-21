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

function generateCFRTables(list, sim_count, simulation_data, num_threads) {
    // Remove existing tables
    var existingTables = document.querySelectorAll(".t-table");
    for (var i = 0; i < existingTables.length; i++) {
        existingTables[i].remove();
    }

    // Remove existing div with top margin
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

        // Add simulation number above the table
        var simulationNumber = document.createElement("div");
        simulationNumber.textContent = "Симуляция №" + (i + 1);
        simulationNumber.classList.add("simulation-number");
        table.appendChild(simulationNumber);

        // Add headers
        for (var j = 0; j < list.length; j++) {
            var th = document.createElement("th");
            th.textContent = list[j];
            tableRow.appendChild(th);
        }

        // Add server columns
        for (var j = 1; j <= num_threads; j++) {
            var th = document.createElement("th");
            th.textContent = "Сервер " + j;
            tableRow.appendChild(th);
        }

        table.appendChild(tableRow);

        // Add request times
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
        
            // Add server times
            for (var j = 0; j < num_threads; j++) {
                var cell = document.createElement("td");
                cell.textContent = rowData.server_times[j];
                row.appendChild(cell);
            }
        
            table.appendChild(row);
        }

        // Add expected value row
        var expectedValueRow = document.createElement("tr");
        var expectedValueCell = document.createElement("td");
        expectedValueCell.setAttribute("colspan", list.length + num_threads);
        expectedValueCell.textContent = "Ожидаемое значение: " + simulation_data.results[i].expected_value;
        expectedValueRow.appendChild(expectedValueCell);
        table.appendChild(expectedValueRow);

        table.style.marginBottom = "40px";
        document.body.appendChild(table);
    }

    // Add a div with top margin of 60px
    var div = document.createElement("div");
    div.classList.add("top-margin-div");
    div.style.marginTop = "60px";
    document.body.appendChild(div);
}

async function unlimitedSolve() {
    var serviceTimeInput = document.getElementById("serviceTimeInput").value;
    var maxSimulationTimeInput = document.getElementById("maxSimulationTimeInput").value;
    var alphaInput = document.getElementById("parameterInput").value;
    var channelCountInput = document.getElementById("channelCountInput").value;
    var iterationCountInput = document.getElementById("iterationCountInput").value;

    const channelCount = parseInt(channelCountInput);
    const iterationCount = parseInt(iterationCountInput);

    if (channelCount > 5){
        alert("Ошибка: число серверов (каналов) ограничено до 5.")
    }

    const formData = {
        serviceTime: parseFloat(serviceTimeInput),
        maxSimulationTime: parseFloat(maxSimulationTimeInput),
        alpha: parseFloat(alphaInput),
        channelCount: channelCount,
        iterationCount: iterationCount,
    };

    try{
        const response = await fetch('/cfr-unlimited', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (response.ok){
            const data = await response.json();
            console.log(data);
            const list = ["Индекс", "Случайное значение", "Интервал между заявками", "Время обслуживания"];
            generateCFRTables(list, iterationCount, data, channelCount);
            goToResult();
        } else {
            console.log('Failed to run simulation: ', response.status, response.statusText);
        }
    } catch (error) {
        console.log('Error: ', error);
    }

}

function refusalSolve() {
    var channelCount = parseInt(document.getElementById("channelCountInput").value);
    var simulationCount = parseInt(document.getElementById("simulationCountInput").value);

    if (isNaN(simulationCount) || simulationCount <= 0){
        alert("Ошибка: Количество симуляций не может быть символом или числом меньше 0")
    }    
    
    if (isNaN(channelCount) || channelCount <= 0) {
        alert("Ошибка: Количество каналов не может быть символом или числом меньше 0");
        return;
    }

    if (channelCount > 5){
        alert("Ошибка: число серверов (каналов) ограничено до 5.")
    }
    else{
        var list = ["Индекс", "Случайное число", "МЕЖ", "Время в очереди", "Обслужено", "Отказов"];''
        generateCFRTables(list, simulationCount);
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