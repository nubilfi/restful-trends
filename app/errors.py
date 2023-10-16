from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.logger import logger

async def custom_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        logger.error(f"Application error: {str(exc.detail)}")

        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    logger.error("Internal server error")

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

def remove_job_safely(scheduler: AsyncIOScheduler, job_id: str):
    try:
        scheduler.remove_job(job_id)

        return {"scheduled": False, "job_id": job_id}
    except JobLookupError:
        logger.error(f"Removing job error: Job with ID {str(job_id)} not found.")
        raise HTTPException(status_code=404, detail=f"Job with ID '{job_id}' not found.")