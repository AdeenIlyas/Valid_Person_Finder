# Valid Person Finder

This project is a Flask web application that uses a team of AI agents (powered by CrewAI) to find and validate contact information for individuals based on their company and job title.

## Features

-   **Single Search:** Find a person by entering their company and designation.
-   **Batch Processing:** Process a list of companies and titles from an Excel file (`Test data.xlsx`).
-   **AI-Powered Agents:**
    -   **Researcher:** Finds potential names and source URLs.
    -   **Validator:** Verifies the information found by the researcher.
    -   **Reporter:** Formats the validated information into a clean JSON output.
-   **Modern UI:** A visually appealing and user-friendly interface built with Flask, HTML, CSS, and JavaScript.

## Project Structure

```
task/
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   └── index.html
├── .env
├── agents.py
├── app.py
├── crew_runner.py
├── requirements.txt
├── tasks.py
└── Test data.xlsx
```

## Setup Instructions

1.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

2.  **Activate the virtual environment:**

    -   On Windows:
        ```bash
        venv\Scripts\activate
        ```
    -   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Required Environment Variables

Create a file named `.env` in the `task` directory and add the following environment variables. You can use the `.env.example` file as a template.

```
OPENAI_API_KEY="your_openai_api_key"
SERPER_API_KEY="your_serper_api_key"
```

-   `OPENAI_API_KEY`: Your API key for OpenAI services.
-   `SERPER_API_KEY`: Your API key for the Serper.dev search API.

## How to Run the Project Locally

1.  **Start the Flask application:**

    ```bash
    python app.py
    ```

2.  **Open your web browser:**

    Navigate to `http://127.0.0.1:5000` to use the application.

## How It Works

-   The **Flask backend** (`app.py`) serves the frontend and provides API endpoints for `/search` (single search) and `/batch` (batch processing).
-   The **frontend** (`index.html`, `style.css`, `script.js`) provides the user interface and makes asynchronous calls to the backend.
-   **CrewAI agents** (`agents.py`, `tasks.py`, `crew_runner.py`) handle the logic for finding and validating the contact information.
-   The results from batch processing are saved in `results.json`.
