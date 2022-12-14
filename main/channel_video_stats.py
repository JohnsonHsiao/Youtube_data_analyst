from googleapiclient.discovery import build
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def get_channel_stats(youtube_builder, channel_pool):

    requests = youtube_builder.channels().list(
        part = 'snippet, contentDetails, statistics',
        id = ','.join(channel_pool)
    )
    response = requests.execute()
    all_channel_data = []
    all_playlist_id_data = []
    all_description_data = []
    for i in range(len(response['items'])):
        # channel_data
        channel_data = dict(
            channel_name = response['items'][i]['snippet']['title'],
            subscribers = response['items'][i]['statistics']['subscriberCount'],
            view_count = response['items'][i]['statistics']['viewCount'],
            video_count = response['items'][i]['statistics']['videoCount'],
            playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
            etag =  response['items'][i]['etag'],
            publish_date = response['items'][i]['snippet']['publishedAt'],)
        
        # playlist_id_data
        playlist_id_data = dict(
            channel_name = response['items'][i]['snippet']['title'],
            playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        
        # description_data
        description_data = dict(
            channel_name = response['items'][i]['snippet']['title'],              
            description = response['items'][i]['snippet']['description'])

        all_channel_data.append(channel_data)
        all_channel_data = pd.DataFrame(all_channel_data)
        all_channel_data['subscribers'] = pd.to_numeric(all_channel_data['subscribers'])
        all_channel_data['view_count'] = pd.to_numeric(all_channel_data['view_count'])
        all_channel_data['publish_date'] = pd.to_datetime(all_channel_data['publish_date'])# maybe just need yy-mm-dd
        all_playlist_id_data.append(playlist_id_data)
        all_playlist_id_data = pd.DataFrame(all_playlist_id_data)
        all_description_data.append(description_data)
        all_description_data = pd.DataFrame(all_description_data)
        
    return all_channel_data, all_description_data, all_playlist_id_data

def get_video_ids(youtube, playlist_id):

    requests = youtube.playlistItems().list(
        part = "contentDetails", 
        playlistId = playlist_id,
        maxResults = 50
    )
    response = requests.execute()
    video_ids = []
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
    next_page_token = response.get('nextPageToken')
    more_pages = True

    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            requests = youtube.playlistItems().list(
                    part = "contentDetails", 
                    playlistId = playlist_id,
                    maxResults = 50,
                    pageToken = next_page_token
                )
            response = requests.execute()
            
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            next_page_token = response.get('nextPageToken')

    return video_ids

def get_video_details_in_json(youtube, video_ids):

    requests = youtube.videos().list(
        part = 'snippet, statistics',
        id =  ','.join(video_ids[:50])
    )
    response = requests.execute()

    return response

def get_video_details_list(youtube, video_ids):

    all_video_stats_list = []
    for i in range(0, len(video_ids), 50):
        requests = youtube.videos().list(
            part = 'snippet, contentDetails, status, statistics', 
            id = ','.join(video_ids[i:i+50])
        )
        response = requests.execute()
        for video in response['items']:
            # breakpoint()
            video_stats = dict(
                title = video['snippet']['title'],
                category = video['snippet'].get('categoryID'),  
                published_date = video['snippet']['publishedAt'],
                channel_id = video['snippet']['channelId'],
                video_view_count = video['statistics'].get('viewCount'),
                video_like_count = video['statistics'].get('likeCount'),
                #video_favorite_count = video['statistics'].get('favoriteCount'),
                #banned from api document
                video_comment_count = video['statistics'].get('commentCount'),
                duration = video['contentDetails'].get('duration'),
                dimension = video['contentDetails'].get('dimension'),
                definition = video['contentDetails'].get('definition'),
                regionrestiction = video['contentDetails'].get('regionRestriction'),
                caption = video['contentDetails'].get('caption'),
                licensedContent = video['contentDetails'].get('licensedContent'),
                region_content_rating = video['contentDetails'].get('contentRating'),
                projection_style = video['contentDetails'].get('projection'), 
                custom_thumbnail_type = video['contentDetails'].get('hasCustomThumbnail'),
                upload_status = video['status'].get('uploadStatus'),  
                embeddable_link = video['status'].get('embeddable'),
                madeforkids = video['status'].get('madeForKids'),
            )
            all_video_stats_list.append(video_stats)
    return all_video_stats_list

