# SQL Bootcamp Challenge App

This project is a Streamlit-based web application that showcases solutions to SQL challenges from the "Jornada de Dados" SQL Bootcamp. The app connects to a PostgreSQL database (running in a Docker container) to fetch and display query results for different questions and challenges.

---

## Table of Contents
1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Setup Instructions](#setup-instructions)
4. [Environment Variables](#environment-variables)
5. [Usage](#usage)
6. [Troubleshooting](#troubleshooting)

---

## Features

- **Data Visualization:** Displays SQL query results using Streamlit.
- **Interactive Widgets:** Toggle buttons to view SQL code for each challenge.
- **Database Integration:** Connects to PostgreSQL using `psycopg2`.
- **Containerized Services:** Docker Compose configuration for PostgreSQL, pgAdmin, and the Streamlit app.

---

## Technologies Used

- **Streamlit:** Interactive web interface for data visualization.
- **PostgreSQL:** Relational database for storing data.
- **pgAdmin:** Web-based UI to manage PostgreSQL.
- **Docker & Docker Compose:** Containerized environment for all services.
- **Poetry:** Python dependency management.
- **Python Libraries:** 
  - `psycopg2` for PostgreSQL connection
  - `pandas` for data handling
  - `streamlit` for UI

---

## Setup Instructions

### Prerequisites
- Docker and Docker Compose installed on your machine
- Python 3.12 installed (for local development)

### Steps

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <your-project-directory>
   ```

2. Build and start the services:
   ```bash
   docker-compose up --build
   ```

3. Access the app:
   - Streamlit App: [http://localhost:8501](http://localhost:8501)
   - pgAdmin: [http://localhost:8080](http://localhost:8080)
     - Login: `user@domain.com`
     - Password: `adminpassword`

---

## Environment Variables

The application uses the following environment variables (defined in `docker-compose.yml`):

- `DB_NAME`: Database name (`mydatabase`)
- `DB_USER`: Database user (`myuser`)
- `DB_PASS`: Database password (`mypassword`)
- `DB_HOST`: Database host (`postgres`, the service name)
- `DB_PORT`: Database port (`5432`)

These variables are used in the Streamlit app to establish the database connection.

---

## Usage

- Launch the Streamlit app and browse through the challenges.
- Use the toggle buttons to view the SQL code for each challenge.
- Results from the database are displayed in tabular format.
