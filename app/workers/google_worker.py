import asyncio
import json
import os
import aiofiles
from google_trends import daily_trends
from datetime import datetime
from app.logger import logger

async def google_trend_worker():
    await asyncio.sleep(5)

    logger.info("Google trend worker executed")

    # Define the directory and file paths
    directory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'trends_data')
    file_path = os.path.join(directory_path, 'google_trend_data.json')

    # Ensure the directory exists, and create it if not
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Ensure the file exists, and create it if not
    if not os.path.exists(file_path):
        async with aiofiles.open(file_path, mode='w') as file:
            await file.write(json.dumps({}))

    # Retrieve daily trends data from Google Trends
    try:
        today_trends = daily_trends(country='ID')

        # Create a dictionary with a "results" key
        results_dict = {
            "results": today_trends,
            "generated_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Convert the data to JSON format with the "results" key
        trends_json = json.dumps(results_dict, indent=2)

        # Save the JSON data to the file
        async with aiofiles.open(file_path, 'w') as file:
            await file.write(trends_json)

        logger.info(f"Google Trends data saved to {file_path}")
    except Exception as e:
        logger.error(f"Error retrieving or saving Google Trends data: {str(e)}")
