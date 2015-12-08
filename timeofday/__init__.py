import os

from flask import Flask

from flask.ext.assets import Environment, Bundle

from webassets.filter import get_filter

from .views import views_blueprint
from .utils import CustomJSONEncoder

app = Flask(__name__, instance_relative_config=True)
assets = Environment(app)

app.json_encoder = CustomJSONEncoder

app.register_blueprint(views_blueprint)

bower_dir = os.path.join(os.path.dirname(__file__), '../bower_components')

assets.load_path = [
    bower_dir,
    os.path.join(os.path.dirname(__file__), 'static')
]

assets.register(
    'js_all',
    Bundle(
        'jquery/dist/jquery.min.js',
        Bundle(
            'javascript/script.coffee',
            filters=['coffeescript']
        ),
        output='packed.js'
    )
)

scss = get_filter('scss', as_output=True, load_paths=[
    os.path.join(bower_dir, 'bourbon/app/assets/stylesheets/'),
    os.path.join(bower_dir, 'neat/app/assets/stylesheets/'),
    os.path.join(bower_dir, 'modular-scale/stylesheets/'),
    os.path.join(bower_dir, 'old-fashioned/scss'),
    os.path.join(os.path.dirname(__file__), 'static/stylesheets')
])

assets.register(
    'css_all',
    Bundle(
        'stylesheets/style.scss',
        filters=[scss],
        output='packed.css'
    )
)
