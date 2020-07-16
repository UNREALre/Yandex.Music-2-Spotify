# -*- coding: utf-8 -*-

import os
from config import project_root
from yandex_music.client import Client, Captcha


def css_js_update_time(for_public=False):
    """Возвращает словарь с временем обновлений статики."""

    static = {
        'css/custom.css': 0,
    }

    for path, time in static.items():
        static[path] = os.path.getmtime(os.path.join(project_root, 'ymapp/static', path))

    return static


def init_client(login=None, password=None, token=None):
    client = captcha_key = captcha_answer = None

    if token:
        try:
            client = Client.from_token(token)
        except BaseException as ex:
            client = None

    if login and password:
        while not client:
            try:
                client = Client.from_credentials(login, password, captcha_answer, captcha_key)
            except Captcha as e:
                e.captcha.download('captcha.png')

                captcha_key = e.captcha.x_captcha_key
                captcha_answer = input('Число с картинки: ')

    return client
