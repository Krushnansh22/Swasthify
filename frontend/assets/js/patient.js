// File: Swasthify/frontend/assets/js/patient.js
const patientUser = JSON.parse(sessionStorage.getItem('swasthify_user'));

if (!patientUser) {
    window.location.href = 'login.html';
} else if (patientUser.role !== 'patient') {
    alert('Access Denied: You must be a patient to view this page.');
    window.location.href = 'login.html';
}

const API_URL = 'http://127.0.0.1:5000/api';

document.addEventListener('DOMContentLoaded', () => {
    console.log(`Patient Portal Loaded for ${patientUser.name} (ID: ${patientUser.id})`);
    
    // You would add functions here to:
    // 1. Check if user is logged in (once you add authentication)
    // 2. Fetch and display their policy details
    // 3. Fetch and display their claim history from '/api/claims'
    
    // Example:
    // fetchMyClaims(patientId); 
});

// Example function to be built later
async function fetchMyClaims(patientId) {
    // Note: You'll need to modify the '/api/claims' endpoint
    // to accept a patientId and filter by it.
    
    // const response = await fetch(`${API_URL}/claims?patient_id=${patientId}`);
    // const claims = await response.json();
    // ... then render them in the table
}