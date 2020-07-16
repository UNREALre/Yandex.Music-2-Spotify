# -*- coding: utf-8 -*-

import os
from config import project_root
from yandex_music.client import Client
from yandex_music.exceptions import Captcha


def css_js_update_time(for_public=False):
    """Возвращает словарь с временем обновлений статики."""

    static = {
        'css/custom.css': 0,
    }

    for path, time in static.items():
        static[path] = os.path.getmtime(os.path.join(project_root, 'ymapp/static', path))

    return static


def init_client(login=None, password=None, token=None, captcha_answer=None, captcha_key=None):
    client = captcha = None
    if token:
        try:
            client = Client.from_token(token)
        except BaseException as ex:
            client = None

    if login and password:

        try:
            print("{} - {} - {} - {}".format(login, password, captcha_answer, captcha_key))
            client = Client.from_credentials(login, password, captcha_answer, captcha_key)
        except Captcha as e:
            captcha_key = e.captcha.x_captcha_key
            e.captcha.download('ymapp/static/captchas/{}_captcha.png'.format(captcha_key))
            captcha = {
                'file': '/static/captchas/{}_captcha.png'.format(captcha_key),
                'cp_key': captcha_key
            }

    return client, captcha
