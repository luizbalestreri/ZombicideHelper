document.addEventListener('DOMContentLoaded', function() {
    fetchCharacters();
});

function fetchCharacters() {
    // Fetch available characters from the backend
    fetch('/characters', {
        headers: {
            'Authorization': 'Bearer ' + sessionStorage.getItem('token')  // Assuming you're using token-based auth
        }
    })
    .then(response => response.json())
    .then(characters => {
        const form = document.getElementById('characterForm');
        characters.forEach(char => {
            const label = document.createElement('label');
            label.innerHTML = `${char.name}<input type="checkbox" name="character" value="${char.id}">`;
            form.appendChild(label);
            form.appendChild(document.createElement("br"));  // For better readability
        });
    });
}

function submitCharacters() {
    const selectedCharacterIds = Array.from(document.querySelectorAll('input[name="character"]:checked')).map(input => input.value);
    const token = sessionStorage.getItem('token');  // Retrieve the token from session storage

    // Assuming your backend expects a list of character IDs and the player's token
    fetch('/register_characters', {  // The endpoint URL might be different in your app
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify({ character_ids: selectedCharacterIds })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            // On success, redirect to the character details page or show success message
            console.log('Characters successfully registered!');
            window.location.href = '/character_details.html';  // Redirect to character details page
        } else {
            // Handle errors or unsuccessful registration
            console.error('Failed to register characters:', data.message);
        }
    })
    .catch(error => {
        console.error('Error submitting characters:', error);
    });
}
