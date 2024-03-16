import os
from dotenv import load_dotenv
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain.agents import tool


keyword = "toronto"

load_dotenv()
DEV_KEY = os.environ.get("API_KEY")
api_service_name = "youtube"
api_version = "v3"

def construct_url(id):
    return f"https://www.youtube.com/watch?v={id}"

@tool
def youtube_search(keyword: str, limit: int = 10) -> list[dict]:
    """ Search on YouTube for videos, and return the titles and URLs for each of them. 
        Find as many videos as possible.


        Args:
            keyword: Term we want to search for
            limit: Maximum amount of videos to search for
    """

    youtube = build(api_service_name, api_version, developerKey=DEV_KEY)

    response = youtube.search().list(
        q=keyword,
        part='id, snippet',
        maxResults=limit
    ).execute()

    video_list = []
    for video in response.get('items', []):
        if video['id']['kind'] == 'youtube#video':
            title = video['snippet']['title']
            url = construct_url(video['id']['videoId'])
            video_list.append({
                'title': title,
                'url': url
            })

    return video_list
    