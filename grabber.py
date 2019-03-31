from logging import getLogger
from datetime import datetime

from youtube import API, YouTubeException
from sqlalchemy.orm import sessionmaker

from database import engine, Video, Views


class Grabber:

    def __init__(self, api_key, channels):
        Session = sessionmaker(bind=engine)

        self.logger = getLogger('youtuber.grabber')
        self.api = API(api_key=api_key, client_id='', client_secret='')
        self.channels = channels
        self.session = Session()

    def _get(self, resource, part, **kwargs):
        try:
            result = self.api.get(resource, part=part, **kwargs)
            if result['pageInfo']['totalResults'] == 0:
                self.logger.error('Resource "{}" is empty for "{}"'.format(resource, kwargs))
                exit(1)

            else:
                return result['items'], result.get('nextPageToken', None)

        except YouTubeException as e:
            self.logger.error(e.error_type)
            return [], None

    def run(self):
        for name in self.channels:
            channels, _ = self._get('channels', 'id', forUsername=name)
            channel_id = channels[0]['id']
            playlists, _ = self._get('playlists', part='id', channelId=channel_id, maxResults=50)
            playlist_ids = [item['id'] for item in playlists]

            for pl_id in playlist_ids:
                page_token = None
                while True:
                    pl_items, page_token = self._get('playlistItems', part='snippet,contentDetails', playlistId=pl_id, maxResults=50, pageToken=page_token)

                    if not page_token:
                        break

                    for item in pl_items:
                        video_id = item['contentDetails']['videoId']
                        video_published_at = item['contentDetails'].get('videoPublishedAt', None)
                        if not video_published_at:
                            continue # deleted video

                        published_at = datetime.strptime(video_published_at, '%Y-%m-%dT%H:%M:%S.%fZ')
                        title = item['snippet']['title']

                        video = self.session.query(Video).get(video_id)
                        if not video:
                            self.session.add(Video(video_id=video_id, channel=name, title=title, published_at=published_at))
                            self.session.commit()

                        video_stat = self._get('videos', part='statistics', id=video_id)[0][0]
                        count = int(video_stat['statistics']['viewCount'])

                        views = Views(video_id, count)
                        self.session.add(views)
                        self.session.commit()

