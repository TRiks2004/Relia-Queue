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

    for (var i = 0; i < sim_count; i++) {
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

        // Проверяем, что simulation_data содержит результаты
        if (simulation_data.results && simulation_data.results.length > i) {
            var iterationsData = simulation_data.results[i].iterations;
            if (iterationsData && iterationsData.length > 0) {
                for (var j = 0; j < iterationsData.length; j++) {
                    var tableRow = document.createElement("tr");
                    var iterationData = iterationsData[j];

                    for (var k = 0; k < list.length; k++) {
                        var td = document.createElement("td");
                        td.textContent = iterationData[list[k].toLowerCase()] || "";
                        tableRow.appendChild(td);
                    }

                    for (var k = 0; k < num_threads; k++) {
                        var td = document.createElement("td");
                        td.textContent = iterationData.server_times ? iterationData.server_times[k] || "" : "";
                        tableRow.appendChild(td);
                    }

                    table.appendChild(tableRow);
                }
            }
        }

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
            console.log('Simulation Results: ', data);
            var list = ["Индекс", "Случайное значение", "Интервал между заявками", "Время обслуживания"];
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