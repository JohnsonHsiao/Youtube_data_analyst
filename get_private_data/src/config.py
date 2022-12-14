import os


# path
AUTH_DIR ='/Users/johnsonhsiao/api-data-download/get_private_data/auths'
CHANNEL_ID_MAPPING = os.path.join('..', 'channel_id.yml')
CLIENT_SECRETS = os.path.join('..', 'key', 'client_secret.json')

# youtube api config
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
REDIRECT_URI = None
SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly',
          'https://www.googleapis.com/auth/youtube.force-ssl']

# server config
IP = '127.0.0.1'
PORT = 8000
