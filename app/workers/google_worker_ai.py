import asyncio
import json
import os
import aiofiles
from google_trends import daily_trends
from datetime import datetime
from app.logger import logger
from app.utils import generate_ai_content

async def fetch_trends_and_generate_content():
    try:
        today_trends = await asyncio.to_thread(daily_trends, country='ID')

        formatted_trends = [{"keyword": keyword, "suggested_ai_article": ""} for keyword in today_trends]

        # Create a list of tasks to generate AI content for each keyword
        content_generation_tasks = [generate_ai_content(trend["keyword"]) for trend in formatted_trends]

        # Wait for all content generation tasks to complete
        suggested_contents = await asyncio.gather(*content_generation_tasks)

        # Assign the generated content to the corresponding trends
        for i, trend in enumerate(formatted_trends):
            trend["suggested_ai_article"] = suggested_contents[i]["choices"][0]["message"]["content"]

        results_dict = {
            "results": formatted_trends,
            "generated_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return results_dict

    except Exception as e:
        logger.error(f"Error retrieving or saving Google Trends data: {str(e)}")
        return None

async def google_trend_ai_worker():
    await asyncio.sleep(5)

    logger.info("Google trend AI worker executed")

    # Define the directory and file paths
    directory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'trends_data')
    file_path = os.path.join(directory_path, 'google_trend_ai_data.json')

    # Ensure the directory exists, and create it if not
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Ensure the file exists, and create it if not
    if not os.path.exists(file_path):
        async with aiofiles.open(file_path, mode='w') as file:
            await file.write(json.dumps({}))

    try:
        results_dict = await fetch_trends_and_generate_content()

        if results_dict is not None:
            trends_json = json.dumps(results_dict, indent=2)

            # Asynchronously write the JSON data to the file
            async with aiofiles.open(file_path, 'w') as file:
                await file.write(trends_json)

            logger.info(f"Google Trends AI data saved to {file_path}")
    except Exception as e:
        logger.error(f"Error retrieving or saving Google Trends AI data: {str(e)}")