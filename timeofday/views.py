import datetime

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

    response = {
        'is_day': False,
        'is_night': False,
        'is_civil_twlight': False,
        'is_nautical_twlight': False,
        'is_astronomical_twilight': False,
        'times-of-day': city.sun()
    }

    if 0 <= city.solar_zenith() <= -6:
        response['is_civil_twlight'] = True
    elif -6 <= city.solar_zenith() <= -12:
        response['is_nautical_twlight'] = True
    elif -12 <= city.solar_zenith() <= -18:
        response['is_astronomical_twilight'] = True

    if city.sunrise() < datetime.datetime.now(city.tz) < city.sunset():
        response['is_day'] = True
    else:
        response['is_night'] = True

    if 0 <= city.moon_phase() < 7:
        response['moon_phase'] = 'new-moon'
    elif 7 <= city.moon_phase() < 14:
        response['moon_phase'] = 'first-quarter'
    elif 14 <= city.moon_phase() < 21:
        response['moon_phase'] = 'full-moon'
    elif 21 <= city.moon_phase():
        response['moon_phase'] = 'last-quarter'

    return jsonify(response)
