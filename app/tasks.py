import subprocess
from app.store import jobs, processes

def run_job(job_id: str, command: str):
    jobs[job_id] = {"status": "running", "output": "", "exit_code": None}
    try:
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        processes[job_id] = proc  # Track the process

        stdout, stderr = proc.communicate()

        output = stdout + stderr
        exit_code = proc.returncode
        status = "completed" if exit_code == 0 else "failed"
    except Exception as e:
        output = str(e)
        exit_code = -1
        status = "failed"
    finally:
        jobs[job_id] = {"status": status, "output": output, "exit_code": exit_code}
        processes.pop(job_id, None)  # Clean up after job finishes
