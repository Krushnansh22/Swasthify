// File: Swasthify/frontend/assets/js/admin.js

// Get user data from session storage
const adminUser = JSON.parse(sessionStorage.getItem('swasthify_user'));

if (!adminUser) {
    // If no user, redirect to login
    window.location.href = 'login.html';
} else if (adminUser.role !== 'admin') {
    // If user is not an admin, show error and redirect
    alert('Access Denied: You must be an admin to view this page.');
    window.location.href = 'login.html';
}

// Define the base URL of your API
const API_URL = 'http://127.0.0.1:5000/api';

document.addEventListener('DOMContentLoaded', () => {
    console.log(`Welcome, ${adminUser.name}!`);
    const loadMembersBtn = document.getElementById('load-members-btn');
    const addMemberForm = document.getElementById('add-member-form');
    const formMessage = document.getElementById('form-message');

    // --- Event Listener for Loading Members ---
    loadMembersBtn.addEventListener('click', fetchAndDisplayMembers);

    // --- Event Listener for Adding a Member ---
    addMemberForm.addEventListener('submit', handleAddMember);

    // Auto-load members on page start
    fetchAndDisplayMembers();
});

/**
 * Fetches all policyholders from the API and displays them in the table.
 */
async function fetchAndDisplayMembers() {
    const tableBody = document.getElementById('members-table-body');
    tableBody.innerHTML = '<tr><td colspan="5">Loading...</td></tr>'; // Clear table
    
    try {
        const response = await fetch(`${API_URL}/policyholders`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const members = await response.json();
        
        tableBody.innerHTML = ''; // Clear "Loading..."
        
        if (members.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5">No members found.</td></tr>';
            return;
        }

        members.forEach(member => {
            // Ensure all keys are lowercase and handle null values
            const row = `
                <tr>
                    <td>${member.policyholderid}</td>
                    <td>${member.firstname}</td>
                    <td>${member.lastname || ''}</td>
                    <td>${member.email}</td>
                    <td>${member.phonenumber || ''}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });

    } catch (error) {
        console.error('Error fetching members:', error);
        tableBody.innerHTML = '<tr><td colspan="5">Error loading members.</td></tr>';
    }
}

/**
 * Handles the form submission for adding a new member.
 */
async function handleAddMember(event) {
    event.preventDefault(); // Stop the form from reloading the page
    
    const form = event.target;
    const formMessage = document.getElementById('form-message');
    formMessage.textContent = ''; // Clear previous messages
    formMessage.className = '';

    // --- 1. FRONTEND VALIDATION ---
    const firstName = form.firstName.value;
    const email = form.email.value;

    if (firstName.trim() === '') {
        formMessage.textContent = 'Error: First Name is required.';
        formMessage.className = 'error';
        return; // Stop execution
    }

    if (email.trim() === '' || !validateEmail(email)) {
        formMessage.textContent = 'Error: A valid Email is required.';
        formMessage.className = 'error';
        return; // Stop execution
    }
    
    // --- 2. Get data from the form (if validation passes) ---
    const memberData = {
        FirstName: firstName,
        LastName: form.lastName.value,
        Email: email,
        DateOfBirth: form.dob.value || null,
        PhoneNumber: form.phone.value || null,
        Address: form.address.value || null
    };

    // 3. Send the data to the API (POST request)
    try {
        const response = await fetch(`${API_URL}/policyholders`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(memberData),
        });
        
        const result = await response.json();

        if (!response.ok) {
            // Show error message from API (e.g., "Email already exists")
            throw new Error(result.error || `HTTP error! status: ${response.status}`);
        }
        
        // 4. Handle success
        formMessage.textContent = 'Member added successfully!';
        formMessage.className = 'success';
        form.reset(); // Clear the form
        fetchAndDisplayMembers(); // Refresh the table

    } catch (error) {
        console.error('Error adding member:', error);
        formMessage.textContent = `Error: ${error.message}`;
        formMessage.className = 'error';
    }
}

/**
 * A simple helper function to validate email format.
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}