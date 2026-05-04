import uuid
import logging

jobs = {}

def create_job():
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "pending",
        "result": None
    }
    logging.info(f"Job created: {job_id}")
    return job_id

def update_job(job_id, result):
    if job_id in jobs:
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = result
        logging.info(f"Job completed: {job_id}")

def get_job(job_id):
    return jobs.get(job_id, None)