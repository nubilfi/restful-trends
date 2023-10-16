# from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Schedule = AsyncIOScheduler()
# Schedule.start()

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from app.settings import settings

# Create a Redis job store
jobstore = RedisJobStore(host=settings.scheduler_redis_host, port=settings.scheduler_redis_port, db=settings.scheduler_redis_db)

# Create the scheduler with the job store
Schedule = AsyncIOScheduler(jobstores={'default': jobstore})
Schedule.start()