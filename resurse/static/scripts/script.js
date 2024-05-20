const goToTheory = () => {
    const theoryTitle = document.getElementById("theoryTitle");
    theoryTitle.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest' });
}

const goToForm = () => {
    const formTitle = document.getElementById("formTitle");
    formTitle.scrollIntoView({ behavior: 'smooth' });
}

const goToResult = () => {
    const resultTitle = document.getElementById("resultTitle");
    resultTitle.scrollIntoView({ behavior: 'smooth' });
}

function refusalSolve() {
    // Get input values
    var intensity = parseFloat(document.getElementById("intensityInput").value);
    var serviceTime = parseFloat(document.getElementById("serviceTimeInput").value);
    var simulationDuration = parseFloat(document.getElementById("simulationDurationInput").value);
    var channelCount = parseInt(document.getElementById("channelCountInput").value);
    var simulationCount = parseInt(document.getElementById("simulationCountInput").value);

    // Example: Validate input values
    if (isNaN(intensity) || intensity <= 0) {
        alert("Ошибка: Интенсивность пуассоновского потока не может быть символом или числом меньше 0");
        return;
    }
    if (isNaN(serviceTime) || serviceTime <= 0) {
        alert("Ошибка: Время обслуживания не может быть символом или числом меньше 0");
        return;
    }
    if (isNaN(simulationDuration) || simulationDuration <= 0) {
        alert("Ошибка: Продолжительность симуляции не может быть символом или числом меньше 0");
        return;
    }
    if (isNaN(channelCount) || channelCount <= 0) {
        alert("Ошибка: Количество каналов не может быть символом или числом меньше 0");
        return;
    }
    if (isNaN(simulationCount) || simulationCount <= 0) {
        alert("Ошибка: Количество симуляций не может быть символом или числом меньше 0");
        return;
    }

    // Continue with the solution
    // ...
}

function unlimitedSolve() {
    // Get input values
    var serviceTime = parseFloat(document.getElementById("serviceTimeInput").value);
    var maxSimulationTime = parseFloat(document.getElementById("maxSimulationTimeInput").value);
    var parameter = parseFloat(document.getElementById("parameterInput").value);
    var channelCount = parseInt(document.getElementById("channelCountInput").value);
    var iterationCount = parseInt(document.getElementById("iterationCountInput").value);

    // Example: Validate input values
    if (isNaN(serviceTime) || serviceTime <= 0) {
        alert("Ошибка: Время обслуживания заявки не может быть символом или числом меньше 0");
        return;
    }
    if (isNaN(maxSimulationTime) || maxSimulationTime <= 0) {
        alert("Ошибка: Максимальное время симуляции не может быть символом или числом меньше 0");
        return;
    }
    if (isNaN(parameter) || parameter <= 0) {
        alert("Ошибка: Параметр для расчета интервала между заявками не может быть символом или числом меньше 0");
        return;
    }
    if (isNaN(channelCount) || channelCount <= 0) {
        alert("Ошибка: Количество потоков не может быть символом или числом меньше 0");
        return;
    }
    if (isNaN(iterationCount) || iterationCount <= 0) {
        alert("Ошибка: Количество итераций не может быть символом или числом меньше 0");
        return;
    }

    // Continue with the solution
    // ...
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