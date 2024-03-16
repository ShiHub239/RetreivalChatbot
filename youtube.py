import os
from dotenv import load_dotenv
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


keyword = "toronto"

load_dotenv()
DEV_KEY = os.environ.get("API_KEY")
api_service_name = "youtube"
api_version = "v3"

def construct_url(id):
    return f"https://www.youtube.com/watch?v={id}"


def youtube_search(keyword, limit):
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
    

    # channels = []
    # playlists = []

    # # Add each result to the appropriate list, and then display the lists of
    # # matching videos, channels, and playlists.
    # for search_result in response.get('items', []):
    #     if search_result['id']['kind'] == 'youtube#video':
    #         videos.append('%s (%s)' % (search_result['snippet']['title'],
    #                                 search_result['id']['videoId']))
    #     elif search_result['id']['kind'] == 'youtube#channel':
    #         channels.append('%s (%s)' % (search_result['snippet']['title'],
    #                                 search_result['id']['channelId']))
    #     elif search_result['id']['kind'] == 'youtube#playlist':
    #         playlists.append('%s (%s)' % (search_result['snippet']['title'],
    #                                     search_result['id']['playlistId']))

    # print('Videos:\n', '\n'.join(videos), '\n')
    # print('Channels:\n', '\n'.join(channels), '\n')
    # print('Playlists:\n', '\n'.join(playlists), '\n')



# print(youtube_search("toronto", 25)[0])