import os
from urllib import response
import csv
from datetime import datetime as dt
from dotenv import load_dotenv
from googleapiclient.discovery import build


# config and bar path
import configparser
config = configparser.ConfigParser()
config.read("/Users/chouwilliam/OrbitNext/api-data-download/key/confidential.ini")
API_KEY = config['PUBLIC_API_KEY']['API_KEY']

youtube = build('youtube', 'v3', developerKey=API_KEY)

comments = []
today = dt.today().strftime('%d-%m-%Y')

def process_comments(response_items, csv_output=False):

    for res in response_items:

        # loop through the replies
        if 'replies' in res.keys():
            for reply in res['replies']['comments']:
                comment = reply['snippet']
                comment['commentId'] = reply['id']
                comments.append(comment)
        else:
            comment = {}
            comment['snippet'] = res['snippet']['topLevelComment']['snippet']
            comment['snippet']['parentId'] = None
            comment['snippet']['commentId'] = res['snippet']['topLevelComment']['id']

            comments.append(comment['snippet'])

    if csv_output:
         make_csv(comments)
    
    print(f'Finished processing {len(comments)} comments.')
    return comments


def make_csv(comments, channelID=None):
    header = comments[0].keys()

    if channelID:
        filename = f'comments_{channelID}_{today}.csv'
    else:
        filename = f'comments_{today}.csv'

    with open(filename, 'w', encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(comments)


def search_result(query):

    """
    Refer to the documentation: https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.search.html
    """

    request = build("youtube", "v3", developerKey=API_KEY).search().list(
        part="snippet",
        q = query,
        maxResults=10
    )

    return request.execute()


def channel_stats(channel_ID):
    """
    Refer to the documentation: https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.channels.html
    """
    query =  build("youtube", "v3", developerKey=API_KEY)
    request = query.channels().list(
        part= "statistics",
        id = channel_ID
    )
    return request.execute()

def comment_threads(channelID, to_csv=False):
    
    comments_list = []
    
    request = youtube.commentThreads().list(
        part='id,replies,snippet',
        videoId=channelID,
    )
    response = request.execute()
    comments_list.extend(process_comments(response['items']))

    # if there is nextPageToken, then keep calling the API
    while response.get('nextPageToken', None):
        request = youtube.commentThreads().list(
            part='id,replies,snippet',
            videoId=channelID,
            pageToken=response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))
    
    print(f"Finished fetching comments for {channelID}. {len(comments_list)} comments found.")
    
    if to_csv:
        make_csv(comments_list, channelID)
    
    return comments_list


def get_video_ids(channelId):
    """
    Reference : https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.search.html
    """
    videoIds = []
 
    request = youtube.search().list(
        part="snippet",
        channelId=channelId,
        type="video",
        maxResults=50,
        order="date"
    )

    response = request.execute()
    responseItems = response['items']

    videoIds.extend([item['id']['videoId'] for item in responseItems if item['id'].get('videoId', None) != None])

    # if there is nextPageToken, then keep calling the API
    while response.get('nextPageToken', None):
        request = youtube.search().list(
            part="snippet",
            channelId=channelId,
        )
        response = request.execute()
        responseItems = response['items']

        videoIds.extend([item['id']['videoId'] for item in responseItems if item['id'].get('videoId', None) != None])
    
    print(f"Finished fetching videoIds for {channelId}. {len(videoIds)} videos found.")

    return videoIds

