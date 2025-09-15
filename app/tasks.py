# app/tasks.py

import subprocess
from app.store import jobs

def run_job(job_id: str, command: str):
    jobs[job_id] = {
        "status": "running",
        "output": "",
        "exit_code": None,
    }

    try:
        print(f"[DEBUG] Running command: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        jobs[job_id]["status"] = "completed" if result.returncode == 0 else "failed"
        jobs[job_id]["output"] = result.stdout.strip()
        jobs[job_id]["exit_code"] = result.returncode

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["output"] = str(e)
        jobs[job_id]["exit_code"] = -1
        print(f"[ERROR] Job {job_id} failed with exception: {e}")
