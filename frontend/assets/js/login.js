// File: Swasthify/frontend/assets/js/login.js

const API_URL = 'http://127.0.0.1:5000/api';

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', handleLogin);
});

async function handleLogin(event) {
    event.preventDefault();
    const form = event.target;
    const messageEl = document.getElementById('login-message');
    const credential = form.credential.value;

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ credential: credential })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Login failed');
        }

        // --- THIS IS THE MOST IMPORTANT PART ---
        // Save the user's data in the browser's session
        sessionStorage.setItem('swasthify_user', JSON.stringify(result));

        // Redirect based on role
        switch (result.role) {
            case 'admin':
                window.location.href = 'admin.html';
                break;
            case 'patient':
                window.location.href = 'patient.html';
                break;
            case 'provider':
                window.location.href = 'provider.html';
                break;
            default:
                throw new Error('Unknown user role');
        }

    } catch (error) {
        messageEl.textContent = `Error: ${error.message}`;
        messageEl.className = 'error';
    }
}