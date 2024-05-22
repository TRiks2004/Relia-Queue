
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



// -----------------------------------------------------------------------------------------------------------------------------











