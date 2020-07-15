import os
from flask import session, redirect, url_for, flash
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyException
from config import appConfig, project_root

scope = "playlist-modify-public"
auth_manager = SpotifyOAuth(scope=scope,
                            client_id=appConfig['spotify']['client_id'].get(),
                            client_secret=appConfig['spotify']['client_secret'].get(),
                            redirect_uri=appConfig['spotify']['redirect_uri'].get(),
                            cache_path=os.path.join(project_root, appConfig['spotify']['cache'].get()))


class SpotifyManager:
    def __init__(self):
        self.sp = None
        self.user_data = {}

    def auth(self):
        if not session.get('token_info'):
            return False

        self.sp = spotipy.Spotify(session.get('token_info')['access_token'])
        try:
            self.user_data['name'] = self.sp.me()['display_name']
            self.user_data['id'] = self.sp.me()['id']
        except SpotifyException as ex:
            return False

        return True

    def import_playlists(self, playlists):
        success_pl = []
        failed_pl = []
        for playlist in playlists:
            try:
                playlist['spotify_data'] = self.create_playlist(playlist['name'], description=playlist['description'])
            except SpotifyException as ex:
                flash(str(ex))
                failed_pl.append(playlist)
            else:
                track_ids = []
                for track in playlist['tracks']:
                    search_result = self.search("{} - {} - {}".format(track.artists[0].name if track.artists else "",
                                                                      track.albums[0].title if track.albums else "",
                                                                      track.title))

                    if search_result['tracks']['items']:
                        track_ids.append(search_result['tracks']['items'][0]['id'])

                try:
                    for i in range(len(track_ids) // 100 + 1):
                        self.add_tracks_to_playlist(track_ids[i*100:i*100+100], playlist['spotify_data']['id'])
                except BaseException as error:
                    failed_pl.append(playlist)
                    flash(str(error))
                else:
                    success_pl.append(playlist)

        return {
            'success': success_pl,
            'failed': failed_pl,
        }

    def create_playlist(self, name, description=None):
        return self.sp.user_playlist_create(self.user_data['id'], name, description=description)

    def search(self, query):
        return self.sp.search(query)

    def add_tracks_to_playlist(self, track_ids, playlist_id):
        self.sp.user_playlist_add_tracks(self.user_data['id'], playlist_id, track_ids)
