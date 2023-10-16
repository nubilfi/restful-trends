import json
import os
import asyncio
import secrets
import openai
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.logger import logger
from cachetools import TTLCache
from app.settings import settings

security = HTTPBasic()

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.error(f"Reading {file_path} data file is failed")
        # If the file doesn't exist or contains invalid JSON, return a dummy JSON
        data = {"results": []}

    return data

# Define a cache with a TTL (time to live) of 1800 seconds (manually set 30 minutes as default)
cache = TTLCache(maxsize=1, ttl=int(os.getenv('TTL_CACHE', 1800)))

async def get_cached_data_trends(file_path):
    if file_path not in cache:
        # If it's not cached, it reads the JSON data from the file
        # in a separate thread using asyncio.to_thread and caches it.
        data = await asyncio.to_thread(read_json_file, file_path)
        cache[file_path] = data

    return cache[file_path]

def get_authenticated(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"changeme"

    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )

    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"changeme"

    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )

    if not (is_correct_username and is_correct_password):
        logger.error(f"Authentication is failed: Incorrect email or password")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    pass

# Define a function to generate content using GPT-3.5-turbo
openai.api_key = settings.openai_api_key
async def generate_ai_content(keyword):
    logger.info("OpenAI executed")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Surprise me about {keyword}"}
            ],
            max_tokens=2500,  # Max 4096
            temperature=0
        )

        logger.info(f"Generating AI content for '{keyword}' success")
        return response
    except Exception as e:
        # Handle the exception, e.g., log the error or return a default value
        logger.error(f"Error generating AI content for '{keyword}': {str(e)}")
