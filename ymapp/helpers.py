# -*- coding: utf-8 -*-

import os
from config import project_root


def css_js_update_time(for_public=False):
    """Возвращает словарь с временем обновлений статики."""

    static = {
        'css/custom.css': 0,
    }

    for path, time in static.items():
        static[path] = os.path.getmtime(os.path.join(project_root, 'ymapp/static', path))

    return static
