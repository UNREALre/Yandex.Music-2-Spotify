import sys
from urllib.parse import urlencode
from flask import redirect, request, jsonify
from config import appConfig
from requests import post


class YandexAuth:
    def __init__(self):
        self.base_url = 'https://oauth.yandex.ru/'
        self.client_id = appConfig['yandex']['client_id'].get()
        self.client_secret = appConfig['yandex']['client_secret'].get()

    def get_token(self):
        if request.args.get('code', False):
            # Если скрипт был вызван с указанием параметра "code" в URL,
            # то выполняется запрос на получение токена
            data = {
                'grant_type': 'authorization_code',
                'code': request.args.get('code'),
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            data = urlencode(data)
            # Токен необходимо сохранить для использования в запросах к API Директа
            return jsonify(post(self.base_url + "token", data).json())
        else:
            # Если скрипт был вызван без указания параметра "code",
            # то пользователь перенаправляется на страницу запроса доступа
            return redirect(
                self.base_url + "authorize?response_type=code&client_id={}".format(self.client_id))
