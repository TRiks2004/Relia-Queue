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

function generateCFRTables(list, sim_count) {
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

    for (var i = 1; i <= sim_count; i++) {
        var table = document.createElement("table");
        table.classList.add("t-table");
        table.setAttribute("border", "1");
        table.style.textAlign = "center";

        var tableRow = document.createElement("tr");

        // Add simulation number above the table
        var simulationNumber = document.createElement("div");
        simulationNumber.textContent = "Симуляция №" + i;
        simulationNumber.classList.add("simulation-number");
        table.appendChild(simulationNumber);

        // Add additional columns
        for (var j = 0; j < list.length; j++) {
            var th = document.createElement("th");
            th.textContent = list[j];
            tableRow.appendChild(th);
        }

        var channelCount = parseInt(document.getElementById("channelCountInput").value);

        // Add server columns
        for (var j = 1; j <= channelCount; j++) {
            var th = document.createElement("th");
            th.textContent = "Сервер " + j;
            tableRow.appendChild(th);
        }
        
        table.style.marginBottom = "40px";
        table.appendChild(tableRow);
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
        service_time: parseFloat(serviceTimeInput),
        max_simulation_time: parseFloat(maxSimulationTimeInput),
        alpha: parseFloat(alphaInput),
        channel_count: channelCount,
        iteration_count: iterationCount,
    };

    try{
        const response = await fetch('cfr-unlimited', {
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
            generateCFRTables(list, iterationCount);
            goToResult();
        } else {
            alert('Failed to run simulation: ', response.status, response.statusText);
        }
    } catch (error) {
        alert('Error: ', error);
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