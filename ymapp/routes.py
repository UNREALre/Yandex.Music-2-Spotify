# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, flash, request, session, url_for
from yandex_music.client import Client
from yandex_music.exceptions import BadRequest
from ymapp.helpers import css_js_update_time, init_client
from ymapp.forms import AuthForm
from ymapp.classes import SpotifyManager
from ymapp.classes.SpotifyManager import auth_manager

blueprint = Blueprint('public', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    progress = 0
    # Проверим, не пришел ли код авторизации от Spotify
    if request.args.get('code'):
        session['token_info'] = auth_manager.get_access_token(request.args['code'])
        return redirect(url_for('public.index'))

    spotify_manager = SpotifyManager()
    if not spotify_manager.auth():
        if session.get('token_info'):
            session['token_info'] = auth_manager.refresh_access_token(session.get('token_info')['refresh_token'])
            return redirect(url_for('public.index'))

        auth_url = auth_manager.get_authorize_url()
        progress = 0
    else:
        auth_url = None
        progress = 35

    times = css_js_update_time()
    form = AuthForm()
    playlists = None

    if session.get('yandex_token') and not form.validate_on_submit():
        client = init_client(token=session.get('yandex_token'))
        if client:
            playlists = client.users_playlists_list()
            progress = 70

    if form.validate_on_submit():
        client = init_client(login=form.login.data, password=form.password.data)
        session['yandex_token'] = client.token
        playlists = client.users_playlists_list()
        progress = 70

    return render_template('index.html',
                           progress=progress,
                           spotify_data=spotify_manager.user_data,
                           spotify_auth_url=auth_url,
                           lists=playlists,
                           form=form,
                           times=times)


@blueprint.route('/import-pl', methods=['POST'])
def import_pl():
    spotify_manager = SpotifyManager()
    spotify_manager.auth()

    client = Client.from_token(session.get('yandex_token'))
    ids = request.form.getlist('for_import[]')
    if ids:
        import_data = []
        for id in ids:
            try:
                playlist = client.users_playlists(kind=id)
            except BadRequest:
                flash("Не удалось выполнить запрос в Яндекс.Музыке")
            else:
                track_ids = [track['id'] for track in playlist[0].tracks]
                if track_ids:
                    tracks = client.tracks(track_ids)
                    import_data.append({
                        "name": playlist[0].title,
                        "description": "Yandex.Music",
                        "tracks": tracks
                    })

        result = spotify_manager.import_playlists(import_data)
    else:
        flash("Не заданы ID плейлистов для импорта!")

    times = css_js_update_time()

    return render_template('index.html',
                           result=result,
                           progress=100,
                           spotify_data=spotify_manager.user_data,
                           times=times)
