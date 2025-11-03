// File: Swasthify/frontend/assets/js/provider.js

const API_URL = 'http://127.0.0.1:5000/api';

// This would be set after the provider logs in
const MY_PROVIDER_ID = 1; // Hard-coded for testing

document.addEventListener('DOMContentLoaded', () => {
    console.log("Provider Portal Loaded");
    
    const claimForm = document.getElementById('submit-claim-form');
    claimForm.addEventListener('submit', handleSubmitClaim);
    
    // You would also fetch and display this provider's past claims
    // fetchMySubmittedClaims(MY_PROVIDER_ID);
});

async function handleSubmitClaim(event) {
    event.preventDefault();
    const form = event.target;
    const formMessage = document.getElementById('form-message');
    formMessage.textContent = '';

    const claimData = {
        EnrollmentID: form.enrollmentId.value,
        ProviderID: MY_PROVIDER_ID, // Use the logged-in provider's ID
        DateOfService: form.dateOfService.value,
        DiagnosisCode: form.diagnosisCode.value,
        Description: form.description.value,
        AmountBilled: form.amountBilled.value
    };

    try {
        const response = await fetch(`${API_URL}/claims`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(claimData)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Failed to submit claim');
        }

        formMessage.textContent = 'Claim submitted successfully!';
        formMessage.className = 'success';
        form.reset();
        // You would refresh the claims table here
        // fetchMySubmittedClaims(MY_PROVIDER_ID);

    } catch (error) {
        formMessage.textContent = `Error: ${error.message}`;
        formMessage.className = 'error';
    }
}