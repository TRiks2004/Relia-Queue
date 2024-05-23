// Переход к разделу "Теория"
const goToTheory = () => {
    const theoryTitle = document.getElementById("theoryTitle");
    theoryTitle.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest' });
}

// Переход к разделу "Форма"
const goToForm = () => {
    const formTitle = document.getElementById("formTitle");
    formTitle.scrollIntoView({ behavior: 'smooth' });
}

// Переход к разделу "Результат"
const goToResult = () => {
    const resultTitle = document.getElementById("saveContainer");
    resultTitle.scrollIntoView({ behavior: 'smooth' });
}
