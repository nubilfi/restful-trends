import asyncio
import json
import os
import requests
import aiofiles
from datetime import datetime
from app.logger import logger
from bs4 import BeautifulSoup

async def youtube_trend_worker():
    await asyncio.sleep(5)

    logger.info("Youtube trend worker executed")

    # Define the directory and file paths
    directory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'trends_data')
    file_path = os.path.join(directory_path, 'youtube_scraped_trend_data.json')

    # Ensure the directory exists, and create it if not
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Ensure the file exists, and create it if not
    if not os.path.exists(file_path):
        async with aiofiles.open(file_path, mode='w') as file:
            await file.write(json.dumps({}))

    # Retrieve daily trends data from Youtube Trends
    try:
        url = "https://www.youtube.com/feed/trending"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP error
        content = response.text

        soup = BeautifulSoup(content, "html.parser")
        scripts = soup.find_all("script")

        # Find the script containing "var ytInitialData = "
        target_script = None
        for script in scripts:
            if "var ytInitialData = " in script.text:
                target_script = script
                break

        if target_script:
            data = target_script.text.replace("var ytInitialData = ", "")
            data = data.rstrip(";")
            data = json.loads(data)

            # Convert the data to JSON format with the "results" key
            results_dict = {
                "results": data,
                "scraped_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            trends_json = json.dumps(results_dict, indent=2)

            # Save the JSON data to the file
            async with aiofiles.open(file_path, 'w') as file:
                await file.write(trends_json)

            logger.info(f"Scraped Youtube Trends data saved to {file_path}")
        else:
            logger.error(f"YouTube Scraping failed: Script containing 'var ytInitialData' not found on the page.")


        await asyncio.sleep(5)
        await youtube_compose_scraped_trend_data_worker()
    except Exception as e:
        logger.error(f"YouTube Scraping failed: Error retrieving or saving Scraped Youtube Trends data: {str(e)}")


async def youtube_compose_scraped_trend_data_worker():
    """"
    Compose our scraped data to be used as daily youtube trend endpoint output.
    """
    await asyncio.sleep(5)

    logger.info("Compose Youtube scraped trend data worker executed")

    # Define the directory and file paths
    directory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'trends_data')
    file_path = os.path.join(directory_path, 'youtube_trend_data.json')

    # Ensure the directory exists, and create it if not
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Ensure the file exists, and create it if not
    if not os.path.exists(file_path):
        async with aiofiles.open(file_path, mode='w') as file:
            await file.write(json.dumps({}))

    # Our source file path
    source_file_path = os.path.join(directory_path, 'youtube_scraped_trend_data.json')

    try:
        # Asynchronously read the source file
        async with aiofiles.open(source_file_path, 'r') as file:
            file_contents = await file.read()
            file_contents_dict = json.loads(file_contents)

            # The Tabbed trend is available on: file_contents.results.contents.twoColumnBrowseResultsRenderer.tabs
            nested_value = file_contents_dict.get("results", {}).get("contents", {}).get("twoColumnBrowseResultsRenderer", {}).get("tabs", {})

            modify_results = []
            modified_contents = []
            for item in nested_value:
                tab_renderer = item["tabRenderer"]

                if tab_renderer.get("content", ""):
                    section_list_renderer = tab_renderer.get("content", "").get("sectionListRenderer")

                    if section_list_renderer.get("contents"):
                        contents = section_list_renderer["contents"]

                        for content_item in contents:
                            item_section_renderer = content_item.get("itemSectionRenderer", {})

                            if item_section_renderer.get("contents"):
                                shelf_renderer = item_section_renderer["contents"][0].get("shelfRenderer", {})
                                expanded_shelf_contents_renderer = shelf_renderer.get("content", {}).get("expandedShelfContentsRenderer", {})

                                if expanded_shelf_contents_renderer.get("items"):
                                    video_renderer = expanded_shelf_contents_renderer["items"][0].get("videoRenderer", {})
                                    thumbnail_url = video_renderer.get("thumbnail", {}).get("thumbnails", [])[0].get("url", "")
                                    title_text = video_renderer.get("title", {}).get("runs", [])[0].get("text", "")
                                    web_command_url = video_renderer.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", "")

                                    main_content = {
                                        "thumbnails_url": thumbnail_url,
                                        "title_text": title_text,
                                        "video_url": web_command_url.replace("/watch?v=", "https://www.youtube.com/embed/")
                                    }
                                    modified_contents.append(main_content)

                extracted_item = {
                    "tabTitle": tab_renderer.get("title", ""),
                    "isTabActive": tab_renderer.get("selected", ""),
                    "content": modified_contents
                }

                modify_results.append(extracted_item)

            # Create a dictionary with a "results" key
            results_dict = {
                # "results": nested_value,
                "results": modify_results,
                "generated_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Convert the data to JSON format with the "results" key
            trends_json = json.dumps(results_dict, indent=2)

            # Asynchronously write the JSON data to the file
            async with aiofiles.open(file_path, 'w') as file:
                await file.write(trends_json)

            logger.info(f"Youtube Trends data saved to {file_path}")
    except FileNotFoundError:
        # Handle the case where the file does not exist
        logger.error(f"YouTube Compose failed: The file '{source_file_path}' does not exist.")

    except Exception as e:
        # Handle any other exceptions that might occur during file reading
        logger.error(f"YouTube Compose failed: An error occurred while reading '{source_file_path}': {str(e)}")