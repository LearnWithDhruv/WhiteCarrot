
# Project Documentation

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Backend](#backend)
  - [Description](#backend-description)
  - [Setup](#backend-setup)
  - [API Overview](#api-overview)
- [Frontend](#frontend)
  - [Description](#frontend-description)
  - [Setup](#frontend-setup)
  - [Key Components](#key-components)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [Contributing](#contributing)
- [License](#license)

## Overview
This project consists of a **Django backend** and a **React frontend** designed to provide a complete full-stack solution. The backend handles API requests and database interactions, while the frontend provides a user-friendly interface.

## Project Structure
```
project/
│
├── backend/                 # Django backend
│   ├── manage.py
│   ├── backend/             # Main Django app
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   ├── wsgi.py
│   ├── api/                 # Custom app for API handling
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       ├── urls.py
│       ├── views.py
│       ├── migrations/
│           ├── __init__.py
│
├── frontend/                # React frontend
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Calendar.js
│   │   │   ├── Login.js
│   │   │   ├── Navbar.js
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── services/        # API calls
│   │       ├── api.js
│   ├── package.json
│   ├── .env
│   ├── README.md
│
├── .gitignore
└── README.md
```

---

## Backend

### Backend Description
The backend is a Django application responsible for serving API endpoints and managing database operations. It includes the following key modules:

- **`backend/`**: Main Django app with configuration files.
- **`api/`**: Custom Django app for API handling, including models, views, serializers, and migrations.

### Backend Setup
1. **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

3. **Start the development server:**
    ```bash
    python manage.py runserver
    ```

### API Overview
- **Models:** Defined in `api/models.py`.
- **Views:** Defined in `api/views.py`.
- **Serializers:** Handle data transformation in `api/serializers.py`.
- **Routes:** Listed in `api/urls.py`.

---

## Frontend

### Frontend Description
The frontend is a React application providing the user interface. It includes reusable components and a service layer for API calls.

### Frontend Setup
1. **Install Node.js dependencies:**
    ```bash
    npm install
    ```

2. **Start the development server:**
    ```bash
    npm start
    ```

### Key Components
- **`Navbar.js`:** Navigation bar component.
- **`Login.js`:** Handles user authentication.
- **`Calendar.js`:** Displays calendar functionality.
- **`api.js`:** Contains methods for API calls to interact with the backend.

---

## Environment Variables
Both the frontend and backend use environment variables for configuration. Ensure the following variables are set:

**Backend (`.env`):**
- `SECRET_KEY`: Django secret key.
- `DATABASE_URL`: URL for the database connection.

**Frontend (`.env`):**
- `REACT_APP_API_URL`: Base URL for the backend API.

---

## Running the Project
1. Start the backend server.
2. Start the frontend server.
3. Access the application at `http://localhost:3000` (frontend) or `http://localhost:8000` (backend).

---

## Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -m 'Add feature'`.
4. Push to branch: `git push origin feature-name`.
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
