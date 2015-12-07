from flask import jsonify, render_template, Blueprint

from astral import Astral

views_blueprint = Blueprint('views', __name__, template_folder='templates')


@views_blueprint.route('/')
def index():
    return render_template('index.html')


@views_blueprint.route('/api/v1')
def api_v1():
    astral = Astral()
    astral.solar_depression = 'civil'

    city = astral['Toronto']

    return jsonify(city.sun())
