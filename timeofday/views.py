import datetime

from flask import jsonify, render_template, make_response, Blueprint

from astral import Astral
from icalendar import Calendar, Event

views_blueprint = Blueprint('views', __name__, template_folder='templates')


@views_blueprint.route('/')
def index():
    return render_template('index.html')


@views_blueprint.route('/ics')
def ics():
    astral = Astral()
    astral.solar_depression = 'civil'
    astral.depression = 6.0

    city = astral['Toronto']

    cal = Calendar()
    cal.add('prodid', '-//Time of Day//time-of-day.herokuapp.com//')
    cal.add('version', '2.0')

    today = datetime.date.today()

    for x in range(-7, 8):
        date = today + datetime.timedelta(days=x)

        sun = city.sun(date=date, local=True)

        for summary, time in sun.items():
            event = Event()
            event.add('summary', summary.capitalize())
            event.add('dtstart', time)
            event.add('dtend', time)
            event.add('dtstamp', time)

            cal.add_component(event)

    resp = make_response(cal.to_ical())

    resp.headers['Content-Disposition'] = 'attachment; filename=time-of-day.ics'
    resp.headers['Content-Type'] = 'text/calendar'

    return resp


@views_blueprint.route('/api/v1')
def api_v1():
    astral = Astral()
    astral.solar_depression = 'civil'
    astral.depression = 6.0

    city = astral['Toronto']

    response = {
        'is_day': False,
        'is_night': False,
        'is_civil_twlight': False,
        'is_nautical_twlight': False,
        'is_astronomical_twilight': False,
        'is_blue_hour': False,
        'solar_zenith_angle': city.solar_zenith(),
        'solar_elevation_angle': city.solar_elevation(),
        'solar_azimuth_angle': city.solar_azimuth(),
        'times_of_day': city.sun()
    }

    current_datetime = datetime.datetime.now(city.tz)

    if city.sunrise() < current_datetime < city.sunset():
        response['is_day'] = True
    else:
        response['is_night'] = True

    if -6 <= city.solar_zenith() <= 0:
        response['is_civil_twlight'] = True
        response['is_day'] = False
        response['is_night'] = False
    elif -12 <= city.solar_zenith() <= -6:
        response['is_nautical_twlight'] = True
        response['is_day'] = False
        response['is_night'] = False
    elif -18 <= city.solar_zenith() <= -12:
        response['is_astronomical_twilight'] = True
        response['is_day'] = False
        response['is_night'] = False

    if -6 <= city.solar_zenith() <= -4:
        response['is_blue_hour'] = True
    elif -4 <= city.solar_zenith() <= 6:
        response['is_golden_hour'] = True

    if 0 <= city.moon_phase() < 7:
        response['moon_phase'] = 'new-moon'
    elif 7 <= city.moon_phase() < 14:
        response['moon_phase'] = 'first-quarter'
    elif 14 <= city.moon_phase() < 21:
        response['moon_phase'] = 'full-moon'
    elif 21 <= city.moon_phase():
        response['moon_phase'] = 'last-quarter'

    return jsonify(response)
