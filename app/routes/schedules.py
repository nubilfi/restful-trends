from fastapi import APIRouter, Depends
from app.scheduler import Schedule
from app.workers import google_worker, tiktok_worker, twitter_worker, youtube_worker, google_worker_ai
from app.errors import remove_job_safely
from app.utils import get_authenticated

router = APIRouter(
    prefix="/v1",
    tags=["schedules"],
)

@router.get("/schedules/show_schedules/")
async def get_scheduled_syncs():
    """
    View All Scheduled Jobs. This schedule is used to retrieve Trends data based on the latest trend.
    """
    schedules = []
    for job in Schedule.get_jobs():
        schedules.append({"Name": str(job.id), "Run Frequency": str(job.trigger), "Next Run": str(job.next_run_time)})

    return schedules

# Google Trends Actions
@router.post("/schedules/google_trend/")
async def add_google_trend_job_to_scheduler(time_in_minutes:int=30, _username: str = Depends(get_authenticated)):
    """
    Add A Scheduled Job for Google trend. By default it'll run for every _30 minutes_ to generate the latest trend,
    but you can change it on its parameter. Remember, the parameter value is in `minutes` time unit.

    After you set the schedule, it'll run again automatically to retrieve or generate the latest trend.
    """
    google_trend_job = Schedule.add_job(google_worker.google_trend_worker, 'interval', minutes=time_in_minutes, id="schedule_google_trend")

    return {"scheduled": True, "job_id": google_trend_job.id}

@router.delete("/schedules/google_trend/")
async def remove_google_trend_job_from_scheduler(_username: str = Depends(get_authenticated)):
    """
    Delete Google Scheduled Job. You're fully responsible for this action, it'll remove the job from scheduler and you'll no longer retrieve the latest
    trends data.
    """
    job_status = remove_job_safely(Schedule, "schedule_google_trend")

    return job_status


@router.post("/schedules/google_trend_ai/")
async def add_google_trend_ai_job_to_scheduler(time_in_minutes:int=30, _username: str = Depends(get_authenticated)):
    """
    Add A Scheduled Job for Google trend with OpenAI involved. By default it'll run for every _30 minutes_ to generate the latest trend,
    but you can change it on its parameter. Remember, the parameter value is in `minutes` time unit.

    After you set the schedule, it'll run again automatically to retrieve or generate the latest trend.
    """
    google_trend_job = Schedule.add_job(google_worker_ai.google_trend_ai_worker, 'interval', minutes=time_in_minutes, id="schedule_google_trend_ai")

    return {"scheduled": True, "job_id": google_trend_job.id}

@router.delete("/schedules/google_trend_ai/")
async def remove_google_trend_ai_job_from_scheduler(_username: str = Depends(get_authenticated)):
    """
    Delete Google AI Scheduled Job. You're fully responsible for this action, it'll remove the job from scheduler and you'll no longer retrieve the latest
    trends data.
    """
    job_status = remove_job_safely(Schedule, "schedule_google_trend_ai")

    return job_status

# TikTok Trends Actions
@router.post("/schedules/tiktok_trend/")
async def add_tiktok_trend_job_to_scheduler(time_in_minutes:int=30, _username: str = Depends(get_authenticated)):
    """
    Add A Scheduled Job for TikTok trend. By default it'll run for every _30 minutes_ to generate the latest trend,
    but you can change it on its parameter. Remember, the parameter value is in `minutes` time unit.

    After you set the schedule, it'll run again automatically to retrieve or generate the latest trend.
    """
    tiktok_trend_job = Schedule.add_job(tiktok_worker.tiktok_trend_worker, 'interval', minutes=time_in_minutes, id="schedule_tiktok_trend")

    return {"scheduled": True, "job_id": tiktok_trend_job.id}

@router.delete("/schedules/tiktok_trend/")
async def remove_tiktok_trend_job_from_scheduler(_username: str = Depends(get_authenticated)):
    """
    Delete TikTok Scheduled Job. You're fully responsible for this action, it'll remove the job from scheduler and you'll no longer retrieve the latest
    trends data.
    """
    job_status = remove_job_safely(Schedule, "schedule_tiktok_trend")

    return job_status

# Twitter Trends Actions
@router.post("/schedules/twitter_trend/")
async def add_twitter_trend_job_to_scheduler(time_in_minutes:int=30, _username: str = Depends(get_authenticated)):
    """
    Add A Scheduled Job for Twitter trend. By default it'll run for every _30 minutes_ to generate the latest trend,
    but you can change it on its parameter. Remember, the parameter value is in `minutes` time unit.

    After you set the schedule, it'll run again automatically to retrieve or generate the latest trend.
    """
    twitter_trend_job = Schedule.add_job(twitter_worker.twitter_trend_worker, 'interval', minutes=time_in_minutes, id="schedule_twitter_trend")

    return {"scheduled": True, "job_id": twitter_trend_job.id}

@router.delete("/schedules/twitter_trend/")
async def remove_twitter_trend_job_from_scheduler(_username: str = Depends(get_authenticated)):
    """
    Delete Twitter Scheduled Job. You're fully responsible for this action, it'll remove the job from scheduler and you'll no longer retrieve the latest
    trends data.
    """
    job_status = remove_job_safely(Schedule, "schedule_twitter_trend")

    return job_status

# YouTube Trends Actions
@router.post("/schedules/youtube_trend/")
async def add_youtube_trend_job_to_scheduler(time_in_minutes:int=30, _username: str = Depends(get_authenticated)):
    """
    Add A Scheduled Job for YouTube trend. By default it'll run for every _30 minutes_ to generate the latest trend,
    but you can change it on its parameter. Remember, the parameter value is in `minutes` time unit.

    After you set the schedule, it'll run again automatically to retrieve or generate the latest trend.
    """
    youtube_trend_job = Schedule.add_job(youtube_worker.youtube_trend_worker, 'interval', minutes=time_in_minutes, id="schedule_youtube_trend")

    return {"scheduled": True, "job_id": youtube_trend_job.id}

@router.delete("/schedules/youtube_trend/")
async def remove_youtube_trend_job_from_scheduler(_username: str = Depends(get_authenticated)):
    """
    Delete YouTube Scheduled Job. You're fully responsible for this action, it'll remove the job from scheduler and you'll no longer retrieve the latest
    trends data.
    """
    job_status = remove_job_safely(Schedule, "schedule_youtube_trend")

    return job_status
