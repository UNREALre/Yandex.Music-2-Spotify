import os
import confuse

project_root = os.path.dirname(os.path.abspath(__file__))
os.environ['YMUSIC2SPOTIFYDIR'] = project_root
appConfig = confuse.Configuration('YMUSIC2SPOTIFY')


class Config:
    SECRET_KEY = appConfig['app']['secret'].get() or 'simple-secret'
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = 'sessions'
