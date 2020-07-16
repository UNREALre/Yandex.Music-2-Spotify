import os
folder = 'ymapp/static/captchas'
for filename in os.listdir(folder):
    path = os.path.join(folder, filename)
    os.unlink(path)
