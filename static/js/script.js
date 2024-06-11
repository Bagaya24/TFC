function _cloneAnswerBlock() {
    const output = document.querySelector("#gpt-output");
    const template = document.querySelector('#chat-template');
    const clone = template.cloneNode(true);
    clone.id = "";
    output.appendChild(clone);
    clone.classList.remove("hidden")
    return clone.querySelector(".message");
}

function addToLog(message) {
    const infoBlock = _cloneAnswerBlock();

    if (!infoBlock) {
        console.error("Échec de la création du bloc d'information");
        return null;
    }

    infoBlock.innerText = message;
    return infoBlock;
}

function getChatHistory() {
    const infoBlocks = document.querySelectorAll(".message:not(#chat-template .message)");

    if (!infoBlocks.length) {
        console.warn('Aucun bloc d\'information trouvé');
        return [];
    }

    return Array.from(infoBlocks).map(block => block.innerHTML);
}

async function fetchPromptResponse(prompt) {
    const response = await fetch("/prompt", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({messages: getChatHistory()}),
    });

    return response.body.getReader();
}

async function readResponseChunks(reader, gptOutput) {
    const decoder = new TextDecoder();
    const converter = new showdown.Converter();

    let chunks = "";
    while (true) {
        const {done, value} = await reader.read();
        if (done) {
            break;
        }
        chunks += decoder.decode(value);
        gptOutput.innerHTML = converter.makeHtml(chunks);
    }
}


document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#prompt-form");
    const spinnerIcon = document.querySelector("#spinner-icon");
    const sendIcon = document.querySelector("#send-icon");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        spinnerIcon.classList.remove("hidden");
        sendIcon.classList.add("hidden");

        const prompt = form.elements.prompt.value;
        form.elements.prompt.value = "";
        addToLog(prompt);

        try {
            const gptOutput = addToLog("L'assistant en train de reflechir...");
            const reader = await fetchPromptResponse(prompt);
            await readResponseChunks(reader, gptOutput);
        } catch (error) {
            console.error('Une erreur est survenue:', error);
        } finally {
            spinnerIcon.classList.add("hidden");
            sendIcon.classList.remove("hidden");
            hljs.highlightAll();
        }
    });
});

function showAjouterModal(){
    let ajouter_modal = document.getElementById("ajouter_modal");
    ajouter_modal.classList.remove("hidden");
    ajouter_modal.classList.add("flex");
    
};

function closeModalAjouter(){
    let ajouter_modal = document.getElementById("ajouter_modal");
    ajouter_modal.classList.remove("flex");
    ajouter_modal.classList.add("hidden");
}

function showMenuModal(button){
    let menu_modal = document.getElementById("menu_modal");
    let buttonRect = button.getBoundingClientRect();
    var row = button.parentNode.parentNode;
    var inputs = document.getElementById('id');
    menu_modal.style.top = buttonRect.top + buttonRect.height - 10 + 'px';
    menu_modal.style.left = buttonRect.left - 80 + 'px';
    menu_modal.classList.remove("hidden");
    menu_modal.classList.add("block");
    inputs.value = row.cells[0].textContent;
    
    if (button.name == "alimentaire") {
        var nom = document.getElementById("nom_aliment");
        var prix = document.getElementById("prix_aliment");
        var quantite = document.getElementById("quantite_aliment");
        var nutriment = document.getElementById("nutriment_aliment");
        var description = document.getElementById("description_aliment");
        nom.value = row.cells[1].textContent;    
        prix.value = row.cells[2].textContent;
        quantite.value = row.cells[3].textContent;
        description.value = row.cells[6].textContent;
        nutriment.value = row.cells[7].textContent;
    }
    else if (button.name == "boisson") {
        var nom = document.getElementById("nom_boisson");
        var prix = document.getElementById("prix_boisson");
        var quantite = document.getElementById("quantite_boisson");
        var nutriment = document.getElementById("nutriment_boisson");
        var description = document.getElementById("description_boisson");
        nom.value = row.cells[1].textContent;    
        prix.value = row.cells[2].textContent;
        quantite.value = row.cells[3].textContent;
        description.value = row.cells[6].textContent;
        nutriment.value = row.cells[7].textContent;
    }

    else if (button.name == "cosmetique") {
        var nom = document.getElementById("nom_cosmetique"); 
        var prix = document.getElementById("prix_cosmetique");
        var quantite = document.getElementById("quantite_cosmetique");
        var type = document.getElementById("type_cosmetique");
        var description = document.getElementById("description_cosmetique");
        nom.value = row.cells[1].textContent;    
        prix.value = row.cells[2].textContent;
        quantite.value = row.cells[3].textContent;
        type.value = row.cells[6].textContent;
        description.value = row.cells[7].textContent;

    }
    else if (button.name == "electromenager") {
        var nom = document.getElementById("nom_electromenager"); 
        var prix = document.getElementById("prix_electromenager");
        var quantite = document.getElementById("quantite_electromenager");
        var type = document.getElementById("type_electromenager");
        var description = document.getElementById("description_electromenager");
        nom.value = row.cells[1].textContent;    
        prix.value = row.cells[2].textContent;
        quantite.value = row.cells[3].textContent;
        type.value = row.cells[4].textContent;
        description.value = row.cells[5].textContent;
        
    }
    

}

function openEffacerModal(button){
    let menu_modal = document.getElementById("menu_modal");
    let effacer_model = document.getElementById("effacer_modal");

    effacer_model.classList.remove("hidden");
    effacer_model.classList.add("flex");
    menu_modal.classList.remove("flex");
    menu_modal.classList.add("hidden");
    
}
function displayRowData(btn) {
    var row = btn.parentNode.parentNode;
    var inputs = document.getElementById('id');
    inputs.value = row.cells[0].textContent;

}

function closeEffacerModal() {
    let effacer_model = document.getElementById("effacer_modal");

    effacer_model.classList.remove("flex");
    effacer_model.classList.add("hidden");
    
}

function openModifierModal() {
    let modifier_modal = document.getElementById("modifier_modal");
    let menu_modal = document.getElementById("menu_modal");
    modifier_modal.classList.remove("hidden");
    modifier_modal.classList.add("flex");
    menu_modal.classList.remove("flex");
    menu_modal.classList.add("hidden");
}

function closeModifierModal(){
    let modifier_modal = document.getElementById("modifier_modal");
    modifier_modal.classList.remove("flex");
    modifier_modal.classList.add("hidden");
}