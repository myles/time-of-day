from flask import Flask

from flask.ext.assets import Environment, Bundle

from .views import views_blueprint
from .utils import CustomJSONEncoder

app = Flask(__name__, instance_relative_config=True)
assets = Environment(app)

app.json_encoder = CustomJSONEncoder

app.register_blueprint(views_blueprint)
