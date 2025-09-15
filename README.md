# Job Runner API (FastAPI + Async + Tests)

This is a simple but powerful API for running shell commands as background jobs using FastAPI. It was built to understand how background processing works with async code, and how to structure a backend project with proper routing, task handling, and tests.

---

## Features

* Submit shell commands (like `echo`, `ls`, `dir`, etc.)
* Track job status (`queued`, `running`, `completed`, `failed`)
* Get output and exit codes of commands
* Async job execution using `threading`
* REST API using FastAPI
* Swagger Docs at `/docs`
* Unit + integration tests with `pytest`

---

## How it works

* You send a shell command using `POST /jobs`
* A background thread runs the command
* You can fetch the result anytime with `GET /jobs/{job_id}`
* You can also list all submitted jobs using `GET /jobs`

All job data is stored in an in-memory dictionary (`jobs` store).

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/usv240/job-runner-api.git
cd job-runner-api
```

### 2. Set up a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt`, you can do:

```bash
pip install fastapi uvicorn httpx pytest pytest-asyncio
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

Visit the docs:
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## Directory Structure

```
job-runner-api/
|
├── app/
│   ├── main.py          # App entry point
│   ├── routes.py        # All endpoints (GET, POST)
│   ├── tasks.py         # Job execution logic
│   ├── models.py        # Pydantic models
│   ├── store.py         # In-memory job store
│   └── utils.py         # Utility functions
|
├── tests/
│   └── test_jobs.py     # Test cases using HTTPX + pytest
|
├── frontend/            # Simple HTML/JS UI (optional)
│   ├── index.html
│   ├── app.js
│   └── styles.css
|
├── README.md
└── requirements.txt
```

---

## How to Run Tests

Make sure you’ve installed `pytest`, `pytest-asyncio`, and `httpx`.

```bash
pytest tests/
```

You should see:

```
tests\test_jobs.py ...     [100%]
```

If async tests were skipped or errored earlier, we fixed it by:

* Installing `pytest-asyncio`
* Using proper `@pytest.mark.asyncio`
* Avoiding issues with `None` as exit code in `JobStatus`

---

## Example Commands to Try

```bash
# Submit a job
curl -X POST http://localhost:8000/jobs -H "Content-Type: application/json" -d "{\"command\": \"echo Hello\"}"

# List all jobs
curl http://localhost:8000/jobs

# Check job status by ID
curl http://localhost:8000/jobs/<job_id>
```

---

## Notes

* If you’re on **Windows**, use `cmd /c echo Hello` instead of just `echo Hello` when submitting jobs.
* We're using `threading.Thread` instead of asyncio subprocess because it was throwing `NotImplementedError` on Windows.

---

## To-Do (Optional Ideas)

* Switch to a real job queue like Celery or RQ
* Store jobs in Redis or a database
* Add JWT-based authentication
* Add log file per job
* Dockerize the app

---

## Credits

Built with ❤️ for learning FastAPI async jobs, testing, and backend architecture.
Feel free to fork and improve!

---

##  Optional: Simple Web UI (Frontend)

This project also comes with a basic UI built using plain HTML, CSS, and JavaScript to help visualize the job system in action.

### Folder structure:

```
frontend/
├── index.html     # Main UI page
├── styles.css     # Basic styling for the form and job list
└── app.js         # Logic to talk to FastAPI backend
```

### How to run it:

Make sure your backend is running on `http://localhost:8000`, then:

```bash
cd frontend
python -m http.server 8080
```

Visit it in your browser:
 [http://localhost:8080](http://localhost:8080)

---

### UI Features:

* Submit shell commands via input field
* View job list with status (`running`, `completed`, etc.)
* Auto-refresh job list every 5 seconds
* Cancel running jobs with a button
* Output display for completed jobs
* Color-coded status display (green = success, red = failed, etc.)

---

This UI is intentionally kept simple. It's ideal for beginners who want to learn how frontend talks to backend via APIs.
You can later rebuild this in React/Vue or add Tailwind/Boo
