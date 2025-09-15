from pydantic import BaseModel
from typing import Optional

class JobRequest(BaseModel):
    command: str

class JobStatus(BaseModel):
    job_id: str
    status: str
    output: str = ""
    exit_code: Optional[int]
