import re
from flask import Flask, session
from flask_session import Session
from config import Config
from jinja2 import Markup, evalcontextfilter

app = Flask(__name__)
app.config.from_object(Config)

Session(app)


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    """Converts newlines in text to HTML-tags"""

    value = re.sub(r'\r\n|\r|\n', '\n', value) # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = [u'<p>%s</p>' % p.replace('\n', '<br />') for p in paras]
    paras = u'\n\n'.join(paras)
    return Markup(paras)


from ymapp.routes import blueprint as blueprint_public
app.register_blueprint(blueprint_public, url_prefix='/')
