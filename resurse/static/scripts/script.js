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
            const responseData = await response.json();
            console.log('Simulation Results:', responseData);
            
            // Здесь вы можете обработать полученные результаты на сайте
            // и вызвать функции для генерации таблиц и перехода к результатам
            const list = ["Индекс", "Случайное число", "МЕЖ", "Время в очереди", "Обслужено", "Отказов"];
            generateTables(list, simulationCount);
            goToResult();
        } else {
            console.error('Failed to run simulation', response.status, response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }}
function generateTables(list, sim_count) {
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