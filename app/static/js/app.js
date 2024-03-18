function registerPlayer() {
    const playerName = document.getElementById('playerName').value;

    fetch('/register', { // Adjust this URL if your registration endpoint is different
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: playerName }),
    })
    .then(response => response.json())
    .then(data => {
        // Assuming the server responds with the generated token and player ID
        if(data.token && data.player_id) {
            // Store token and player ID in sessionStorage or localStorage
            sessionStorage.setItem('token', data.token);
            sessionStorage.setItem('player_id', data.player_id);
            // Redirect or update UI
            window.location.href = '/choose_characters.html'; // Redirect to character selection
        } else {
            // Handle registration error or invalid response
            console.error('Registration failed or invalid response');
        }
    })
    .catch(error => {
        console.error('Error registering player:', error);
    });
}
