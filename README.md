# Portfolio AI Chatbot - Backend

Backend API built with Python and FastAPI for powering an AI chatbot integration on a portfolio website.

## Requirements

- Python 3.10+ installed

## Getting Started

### 1. Virtual Environment

A Python virtual environment isolates the dependencies of this project from your global Python installation.

#### Activate the Virtual Environment:

- **Windows (PowerShell):**
  ```powershell
  \.venv\Scripts\Activate.ps1
  ```

- **Windows (Command Prompt / CMD):**
  ```cmd
  \.venv\Scripts\activate.bat
  ```

- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 2. Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Gemini API Setup

To prepare the backend for Google Gemini integration:

1. Obtain a Gemini API Key from [Google AI Studio](https://aistudio.google.com/).
2. Set your API key in the `.env` file:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```
3. **Security Note:** Never commit `.env` or real API keys to version control. The `.gitignore` file ensures `.env` is kept private.
4. The API key is loaded safely by `app/config.py` and will be used in the next phase to power the AI chatbot.

### 4. Run the FastAPI Server

Start the application server using Uvicorn with hot-reloading enabled:

```bash
uvicorn app.main:app --reload
```

The server will start running at `http://127.0.0.1:8000`.

### 5. Testing the Server

#### Test the `/health` Endpoint:
- Open your web browser or run curl:
  ```bash
  curl http://127.0.0.1:8000/health
  ```
- Expected response:
  ```json
  {
    "status": "ok"
  }
  ```

#### Interactive API Documentation:
FastAPI automatically generates interactive API documentation. You can access it in your browser at:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`
