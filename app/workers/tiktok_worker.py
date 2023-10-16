import asyncio
import os
import json
import logging
import aiohttp
import aiofiles
from datetime import datetime
from app.logger import logger

# Initialize logger
log = logging.getLogger(__name__)

# Define headers and params
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'
}
params_feed = {
    'version_name': '26.1.3',
    'version_code': '260103',
    'build_number': '26.1.3',
    'manifest_version_code': '260103',
    'update_version_code': '260103',
    'ts': '1684811896',
    'device_brand': 'Google',
    'device_type': 'Pixel 7',
    'device_platform': 'android',
    'resolution': '1080*2400',
    'dpi': '680',
    'os_version': '10',
    'os_api': '29',
    'carrier_region': 'ID',  # Use ID for Indonesia
    'sys_region': 'ID',      # Use ID for Indonesia
    'region': 'ID',          # Use ID for Indonesia
    'app_name': 'trill',
    'app_language': 'en',
    'language': 'en',
    'timezone_name': 'Asia/Jakarta',  # Use Jakarta timezone for Indonesia
    'timezone_offset': '25200',       # Use Jakarta timezone offset (UTC+7) for Indonesia
    'channel': 'googleplay',
    'ac': 'wifi',
    'mcc_mnc': '510',        # Use MCC_MNC for an Indonesian carrier
    'is_my_cn': '0',
    'aid': '1180',
    'ssmix': 'a'
}

# Example list of URLs and filenames
urls_data = [
    {"url": "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/", "filename": "tiktok_feed_raw_data.json", "params": params_feed},
    {"url": "https://www.tiktok.com/node/share/discover", "filename": "tiktok_discover_raw_data.json", "params": {}},
    {"url": "https://tikfinity.zerody.one/api/getLiveChannels", "filename": "tiktok_live_channels_raw_data.json", "params": {}},
    # Add more URLs and filenames as needed
]

async def fetch_and_save_data(url_opts):
    try:
        url = url_opts["url"]
        params = url_opts["params"]
        filename = url_opts["filename"]

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                tiktok_data = await response.json()

        # Define the directory and file paths
        directory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'trends_data')
        file_path = os.path.join(directory_path, filename)

        # Ensure the directory exists, and create it if not
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        # Create a dictionary with a "results" key
        results_dict = {
            "results": tiktok_data,
            "generated_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Convert the data to JSON format with the "results" key
        trends_json = json.dumps(results_dict, indent=2)

        # Save the JSON data to the file
        async with aiofiles.open(file_path, 'w') as file:
            await file.write(trends_json)

        logger.info(f"TikTok Trends raw data saved to {file_path}")
    except Exception as e:
        logger.error(f"Error retrieving or saving TikTok Trends raw data for {url_opts['url']}: {str(e)}")

async def tiktok_trend_worker():
    await asyncio.sleep(5)

    logger.info("TikTok trend worker executed")

    # Create tasks for fetching and saving data concurrently
    tasks = [fetch_and_save_data(url_info) for url_info in urls_data]
    await asyncio.gather(*tasks)

    await asyncio.sleep(5)
    await compose_tiktok_feed_trend_worker()
    await compose_tiktok_discover_trend_worker()
    await compose_tiktok_live_trend_worker()

async def compose_tiktok_feed_trend_worker():
    """
    Compose TikTok feed trends raw data.
    """
    await asyncio.sleep(5)

    logger.info("Compose TikTok feed trend worker executed")

    # Define the directory and file paths
    directory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'trends_data')
    file_path = os.path.join(directory_path, 'tiktok_feed_data.json')
    source_file_path = os.path.join(directory_path, 'tiktok_feed_raw_data.json')

    try:
        # Asynchronously read the source file
        async with aiofiles.open(source_file_path, 'r') as file:
            file_contents = await file.read()
            file_contents_dict = json.loads(file_contents)

            nested_value = file_contents_dict.get("results", {}).get("aweme_list", [])

            modify_results = []
            for item in nested_value:
                content_id = item["aweme_id"]
                feed_desc = item["desc"]
                feed_author_region = item["author"]["region"]
                feed_author_nickname = item["author"]["nickname"]
                feed_author_avatar_url = item["author"]["avatar_thumb"]["url_list"][0]

                feed_music_id = item["music"]["id"]
                feed_music_desc = item["music"]["title"]
                feed_music_author = item["music"]["author"]
                feed_music_url = item["music"].get("play_url", {}).get("url_list", [])[0]
                feed_author_music_url = item["music"].get("play_url", {}).get("url_list", [])[0]

                feed_video_url = item["video"]["play_addr"]["url_list"][0]
                feed_video_views_count = item.get("playlist_info", {}).get("name", "")
                feed_keywords = item.get("suggest_words", {}).get("suggest_words", [])[0]["words"][0]["word"] if item.get("suggest_words", {}).get("suggest_words", []) else ""

                main_content = {
                    "content_id": content_id,
                    "feed_desc": feed_desc,
                    "feed_author_region": feed_author_region,
                    "feed_author_nickname": feed_author_nickname,
                    "feed_author_avatar_url": feed_author_avatar_url,
                    "feed_music_id": feed_music_id,
                    "feed_music_desc": feed_music_desc,
                    "feed_music_author": feed_music_author,
                    "feed_music_url": feed_music_url,
                    "feed_author_music_url": feed_author_music_url,
                    "feed_video_url": feed_video_url,
                    "feed_video_views_count": feed_video_views_count,
                    "feed_keywords": feed_keywords,
                }

                modify_results.append(main_content)

            # Create a dictionary with a "results" key
            results_dict = {
                "results": modify_results,
                "generated_time": file_contents_dict.get("generated_time", "")
            }

            # Convert the data to JSON format with the "results" key
            trends_json = json.dumps(results_dict, indent=2)

            # Asynchronously write the JSON data to the file
            async with aiofiles.open(file_path, 'w') as file:
                await file.write(trends_json)

            logger.info(f"TikTok Feed Trends data saved to {file_path}")
    except FileNotFoundError:
        # Handle the case where the file does not exist
        logger.error(f"TikTok Feed Compose failed: The file '{source_file_path}' does not exist.")

    except Exception as e:
        # Handle any other exceptions that might occur during file reading
        logger.error(f"TikTok Feed Compose failed: An error occurred while reading '{source_file_path}': {str(e)}")

async def compose_tiktok_discover_trend_worker():
    """
    Compose TikTok discover trends raw data.
    """
    await asyncio.sleep(5)

    logger.info("Compose TikTok feed discover worker executed")

    # Define the directory and file paths
    directory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'trends_data')
    file_path = os.path.join(directory_path, 'tiktok_discover_data.json')
    source_file_path = os.path.join(directory_path, 'tiktok_discover_raw_data.json')

    try:
        # Asynchronously read the source file
        async with aiofiles.open(source_file_path, 'r') as file:
            file_contents = await file.read()
            file_contents_dict = json.loads(file_contents)

            nested_value = file_contents_dict.get("results", {}).get("body", [])

            modify_results = []
            for item in nested_value:
                exploreList = item.get("exploreList", [])

                for list in exploreList:
                    content_id = list.get("cardItem", {}).get("id", "")
                    discover_list_title = list.get("cardItem", {}).get("title", "")
                    discover_list_subtitle = list.get("cardItem", {}).get("subTitle", "")
                    discover_list_description = list.get("cardItem", {}).get("description", "")
                    discover_list_url = "https://tiktok.com" + list.get("cardItem", {}).get("link", "")

                    main_content = {
                        "content_id": content_id,
                        "discover_list_title": discover_list_title,
                        "discover_list_subtitle": discover_list_subtitle,
                        "discover_list_description": discover_list_description,
                        "discover_list_url": discover_list_url,
                    }

                    modify_results.append(main_content)

            # Create a dictionary with a "results" key
            results_dict = {
                "results": modify_results,
                "generated_time": file_contents_dict.get("generated_time", "")
            }

            # Convert the data to JSON format with the "results" key
            trends_json = json.dumps(results_dict, indent=2)

            # Asynchronously write the JSON data to the file
            async with aiofiles.open(file_path, 'w') as file:
                await file.write(trends_json)

            logger.info(f"TikTok Discover Trends data saved to {file_path}")
    except FileNotFoundError:
        # Handle the case where the file does not exist
        logger.error(f"TikTok Discover Compose failed: The file '{source_file_path}' does not exist.")

    except Exception as e:
        # Handle any other exceptions that might occur during file reading
        logger.error(f"TikTok Discover Compose failed: An error occurred while reading '{source_file_path}': {str(e)}")

async def compose_tiktok_live_trend_worker():
    """
    Compose TikTok live trends raw data.
    """
    await asyncio.sleep(5)

    logger.info("Compose TikTok live trend worker executed")

    # Define the directory and file paths
    directory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'trends_data')
    file_path = os.path.join(directory_path, 'tiktok_live_channels_data.json')
    source_file_path = os.path.join(directory_path, 'tiktok_live_channels_raw_data.json')

    try:
        # Asynchronously read the source file
        async with aiofiles.open(source_file_path, 'r') as file:
            file_contents = await file.read()
            file_contents_dict = json.loads(file_contents)

            nested_value = file_contents_dict.get("results", {}).get("liveChannels", [])

            modify_results = []
            for item in nested_value:
                content_id = str(item.get("channelId", ""))
                live_user_id = item.get("ownerUserId", "")
                live_user_nickname = "https://tiktok.com/@" + item.get("channelName", "")
                live_user_country = item.get("countryCode", "")
                live_user_views_count = item.get("viewerCount", 0)

                main_content = {
                    "content_id": content_id,
                    "live_user_id": live_user_id,
                    "live_user_nickname": live_user_nickname,
                    "live_user_country": live_user_country,
                    "live_user_views_count": live_user_views_count,
                }

                modify_results.append(main_content)

            # Create a dictionary with a "results" key
            results_dict = {
                "results": modify_results,
                "generated_time": file_contents_dict.get("generated_time", "")
            }

            # Convert the data to JSON format with the "results" key
            trends_json = json.dumps(results_dict, indent=2)

            # Asynchronously write the JSON data to the file
            async with aiofiles.open(file_path, 'w') as file:
                await file.write(trends_json)

            logger.info(f"TikTok Live Trends data saved to {file_path}")
    except FileNotFoundError:
        # Handle the case where the file does not exist
        logger.error(f"TikTok Live Compose failed: The file '{source_file_path}' does not exist.")

    except Exception as e:
        # Handle any other exceptions that might occur during file reading
        logger.error(f"TikTok Live Compose failed: An error occurred while reading '{source_file_path}': {str(e)}")
