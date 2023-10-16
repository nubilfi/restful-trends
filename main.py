from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares import RedisRateLimiterMiddleware, redis_client
from app.routes import ping, google_daily, schedules, tiktok_daily, twitter_daily, youtube_daily
from app.errors import custom_exception_handler
from app.cors import cors_config
from os import getenv

import sentry_sdk

sentry_sdk.init(
    # Account: setup yours (https://sentry.io)
    dsn=getenv('SENTRY_DSN', ''),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = FastAPI(
    title="RESTful Trends App",
    description="an API to get Trends data from Google, TikTok, YouTube and Twitter",
    summary="Follow the trends.",
    version="0.0.1",
    contact={
        "name": "admin",
        "email": "admin@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/nubilfi/restful-trends/blob/main/LICENSE",
    },
)

app.add_middleware(
    RedisRateLimiterMiddleware,
    redis_client=redis_client,
    limit=20,
    window=30
)

# Add the error handler middleware
app.add_exception_handler(Exception, custom_exception_handler)
# Get the CORS middleware based on the mode
get_cors_config = cors_config()
app.add_middleware(CORSMiddleware, **get_cors_config)

app.include_router(ping.router)
app.include_router(google_daily.router)
app.include_router(tiktok_daily.router)
app.include_router(twitter_daily.router)
app.include_router(youtube_daily.router)
app.include_router(schedules.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=getenv('APP_HOST', '0.0.0.0'), port=int(getenv('APP_PORT', 0)))
