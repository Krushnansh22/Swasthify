# Swasthify: Health Insurance Management Platform 🏥
HEllo changes



Swasthify is a comprehensive health insurance management platform designed to streamline policyholder management and provide a user-friendly interface for both administrators and patients. It offers a backend API built with Flask for managing policyholder data, and a frontend with admin and patient portals for interacting with the system. The platform aims to simplify health insurance processes, making them more accessible and efficient.

## 🚀 Features

- **Policyholder Management:** Create, read, update, and delete policyholder records via a RESTful API.
- **Admin Portal:** A dedicated interface for administrators to manage policyholders, add new members, and view existing records.
- **Patient Portal:** A user-friendly interface for patients to view their profile information, claims history, and other relevant data.
- **Provider Portal:** (Currently under development) Intended to provide functionalities specific to healthcare providers.
- **Authentication:** Secure login functionality for different user roles (admin, provider, patient).
- **Database Integration:** Seamless integration with a PostgreSQL database for persistent data storage.
- **API Documentation:** Clear and concise API documentation to facilitate integration with other systems.
- **CORS Enabled:** Cross-Origin Resource Sharing (CORS) enabled to allow frontend applications to securely access the backend API.

## 🛠️ Tech Stack

*   **Frontend:**
    *   HTML5
    *   CSS3 (Inline Styling & External Stylesheet)
    *   JavaScript
*   **Backend:**
    *   Python 3.x
    *   Flask: Web framework for building the API.
    *   Flask-CORS: Enables Cross-Origin Resource Sharing.
    *   psycopg2: PostgreSQL adapter for Python.
    *   psycopg2.extras: Provides extra features for `psycopg2`, including the `DictCursor`.
*   **Database:**
    *   PostgreSQL
*   **Build Tools:**
    *   pip (Python Package Installer)

## 📦 Getting Started / Setup Instructions

### Prerequisites

Before you begin, ensure you have the following installed:

-   Python 3.x
-   pip (Python Package Installer)
-   PostgreSQL
-   A PostgreSQL client (e.g., pgAdmin)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Set up the backend:**

    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Configure the database:**

    -   Create a PostgreSQL database named `swasthify`.
    -   Update the database connection parameters in `backend/db.py` with your PostgreSQL credentials (DB_HOST, DB_NAME, DB_USER, DB_PASS).  Ideally, these should be set as environment variables.

4.  **Set up the frontend:**

    -   Navigate to the `frontend` directory. No specific installation steps are needed for the HTML/CSS/JS files, but you'll need a web server to serve them.

### Running Locally

1.  **Start the backend:**

    ```bash
    cd backend
    flask run --debug
    ```

    This will start the Flask development server.

2.  **Serve the frontend:**

    -   Open the `frontend/admin.html`, `frontend/patient.html`, `frontend/provider.html`, and `frontend/login.html` files in your web browser.  Alternatively, use a simple HTTP server (e.g., `python -m http.server` in the `frontend` directory) to serve the files.

## 💻 Usage

1.  **Access the Admin Portal:** Open `frontend/admin.html` in your browser. Use the form to add new policyholders and click "Load Members" to view existing policyholders.
2.  **Access the Patient Portal:** Open `frontend/patient.html` in your browser.  This portal allows patients to view their information and manage their profile.
3.  **Access the Provider Portal:** Open `frontend/provider.html` in your browser. (Note: Functionality may be limited as `provider.js` is currently empty).
4.  **Use the API:** The backend API provides endpoints for managing policyholders. Refer to the `backend/app.py` file for details on the available endpoints and their usage.

## 📂 Project Structure

```
Swasthify/
├── backend/
│   ├── app.py          # Flask application for the backend API
│   ├── db.py           # Database connection utilities
│   ├── requirements.txt # Python dependencies
│   └── venv/           # Virtual environment (not tracked in Git)
├── frontend/
│   ├── admin.html      # Admin portal HTML
│   ├── patient.html    # Patient portal HTML
│   ├── provider.html   # Provider portal HTML
│   ├── login.html      # Login page HTML
│   ├── assets/
│   │   ├── css/
│   │   │   └── style.css   # Stylesheet for the frontend
│   │   ├── js/
│   │   │   ├── admin.js    # JavaScript for the admin portal
│   │   │   ├── patient.js  # JavaScript for the patient portal
│   │   │   └── provider.js # JavaScript for the provider portal (currently empty)
│   └── ...
├── README.md       # This file
└── ...
```

## 📸 Screenshots

(Add screenshots of the admin portal, patient portal, and other relevant parts of the application here)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with clear, descriptive messages.
4.  Submit a pull request.

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 📬 Contact

For questions or issues, please contact: [Your Name/Organization] - [Your Email]

## 💖 Thanks

Thank you for using Swasthify! We hope this platform helps you streamline your health insurance management processes.

This is written by [readme.ai](https://readme-generator-phi.vercel.app/).
