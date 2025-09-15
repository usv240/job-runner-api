from fastapi import APIRouter
from app.models import JobRequest, JobStatus
from app.tasks import run_job
from app.utils import generate_job_id
from app.store import jobs, processes  # ✅ Import here
import uuid
import threading

router = APIRouter()

@router.post("/jobs")
def submit_job(request: JobRequest):
    job_id = uuid.uuid4().hex
    thread = threading.Thread(target=run_job, args=(job_id, request.command))
    thread.start()
    return {"job_id": job_id, "status": "queued", "output": "", "exit_code": None}

@router.get("/jobs/{job_id}", response_model=JobStatus)
def get_job(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return {"job_id": job_id, "status": "not_found", "output": "", "exit_code": -1}
    return {"job_id": job_id, **job}

@router.get("/jobs")
def list_jobs():
    return [{"job_id": jid, "status": data["status"]} for jid, data in jobs.items()]

@router.post("/jobs/{job_id}/cancel")
def cancel_job(job_id: str):
    process = processes.get(job_id)
    if process and process.poll() is None:
        process.terminate()
        jobs[job_id]["status"] = "cancelled"
        return {"message": f"Job {job_id} cancelled"}
    return {"message": f"Job {job_id} not running or already finished"}
