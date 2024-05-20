const form = document.getElementById('user-input');
form.addEventListener('submit', handleSubmit);

function handleSubmit(event) {
    event.preventDefault();
    const userMessage = document.getElementById('user-message').value;
    fetch('/process-message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        const botResponse = data.message;
        document.getElementById('bot-response').innerText = botResponse;
    });
}