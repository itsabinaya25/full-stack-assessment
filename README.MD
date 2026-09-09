# Full-Stack Assessment

A full-stack web application built using **Python Flask, MySQL, HTML, CSS, and JavaScript**.

## Features

* User registration (Sign Up)
* User login
* Password hashing
* MySQL database integration
* File upload
* File download
* PDF, PNG, JPG, and JPEG file validation
* Uploaded file metadata stored in MySQL
* User-specific file association
* Session-based authentication
* Input validation and error handling

## Technology Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python Flask
* **Database:** MySQL 8.0
* **File Storage:** Server-side `uploads/` directory
* **Version Control:** Git and GitHub

---

## Local Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/itsabinaya25/full-stack-assessment.git
cd full-stack-assessment
```

### 2. Create a Python virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install flask mysql-connector-python python-dotenv werkzeug
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```text
SECRET_KEY=your-secret-key
MYSQL_HOST=127.0.0.1
MYSQL_USER=root
MYSQL_PASSWORD=your-mysql-password
MYSQL_DATABASE=fullstack_app
```

Do not commit the `.env` file to GitHub.

### 5. Run the application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

---

## Database Setup

### 1. Create the database

Open MySQL Workbench and run:

```sql
CREATE DATABASE fullstack_app;
```

Select the database:

```sql
USE fullstack_app;
```

### 2. Create the users table

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL,
    age INT,
    address VARCHAR(255),
    mobile VARCHAR(20)
);
```

### 3. Create the uploaded_files table

```sql
CREATE TABLE uploaded_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(20) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

The application stores passwords as **hashed passwords** rather than plain text.

Uploaded file metadata includes:

* Filename
* File type
* Upload timestamp
* Associated user ID

Uploaded files are stored in the server's `uploads/` directory.

---

## Hosting Details

**Hosting Platform:** To be updated after deployment.

**Deployed Application:** To be updated after deployment.

The application will be deployed to a publicly accessible hosting platform as required by the assessment.

---

## Assumptions

* MySQL 8.0 is used as the database server.
* The application uses a local MySQL database during development.
* Users provide valid registration details.
* Mobile numbers are expected to contain 10 digits.
* Passwords must contain at least 6 characters.
* Supported uploaded file types are PDF, PNG, JPG, and JPEG.
* Two file upload fields are provided as required by the assessment.
* Uploaded files are stored on the backend server.
* `.env` is used for sensitive configuration such as the MySQL password.
* The `.env` file is excluded from Git using `.gitignore`.

---

## Project Structure

```text
full-stack-assessment/
│
├── app.py
├── config.py
├── database.py
├── .gitignore
├── README.md
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   └── files.py
│
├── static/
│   └── js/
│       └── script.js
│
├── styles/
│   └── style.css
│
├── templates/
│   ├── signup.html
│   ├── login.html
│   └── dashboard.html
│
└── uploads/
    └── test_file.txt
```

## Security

* Passwords are hashed before being stored in MySQL.
* User input is validated.
* Uploaded file types are restricted.
* Uploaded filenames are secured using `secure_filename`.
* Database credentials are stored in environment variables.
* `.env` is excluded from GitHub using `.gitignore`.
