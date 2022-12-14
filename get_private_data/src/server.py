import json
import os
from pdb import set_trace as bp  # noqa

import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow
from flask_socketio import SocketIO
from googleapiclient.discovery import build

from config import CLIENT_SECRETS
from config import IP
from config import PORT
from config import REDIRECT_URI
from config import SCOPES


app = flask.Flask(__name__)
app.secret_key = os.urandom(42)
socketio = SocketIO(app)


@socketio.on('disconnect')
def disconnect():
    flask.session.clear()


@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')


@app.route('/query')
def query():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load the credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    # get channel ids
    client = build('youtube', 'v3', credentials=credentials)
    channel_ids = channel_ids_by_username(client, part='id', mine=True)

    # get channel data
    client = build('youtubeAnalytics', 'v2', credentials=credentials)
    data, cols = get_data(client, channel_id=channel_ids[0])  # TODO: get multiple
    return flask.render_template('record.html', records=data, colnames=cols)


@app.route('/download_auth')
def download_auth_pkl():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')
    return flask.Response(
            json.dumps(flask.session['credentials']),
            mimetype='json',
            headers={'Content-disposition': 'attachment; filename=test.json'})


@app.route('/authorize')
def authorize():
    flask.session.clear()
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS, scopes=SCOPES, redirect_uri=REDIRECT_URI)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        # This parameter enables offline access which gives your application
        # both an access and refresh token.
        access_type='offline',
        # This parameter enables incremental auth.
        include_granted_scopes='true')

    # Store the state in the session so that the callback can verify that
    # the authorization server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verify the authorization server response.
    state = flask.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS, scopes=SCOPES, state=state, redirect_uri=REDIRECT_URI)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials in the session.
    # ACTION ITEM for developers:
    #     Store user's access and refresh tokens in your data store if
    #     incorporating this code into your real app.
    credentials = flow.credentials
    flask.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    return flask.redirect(flask.url_for('index'))


def channel_ids_by_username(client, **kwargs):
    response = client.channels().list(
      **kwargs
    ).execute()

    return [v['id'] for v in response['items']]


def get_data(client, **kwargs):
    result = client.reports().query(
        ids=f'channel=={kwargs["channel_id"]}',
        startDate='2021-10-31',
        endDate='2021-12-31',
        metrics='estimatedMinutesWatched,views,likes,subscribersGained',
        dimensions='day',
        sort='day').execute()

    col = [v['name'] for v in result['columnHeaders']]
    return result['rows'], col


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(IP, PORT, debug=True)
