do ->
  timeOfDayAPI = '/api/v1'
  timeFormat = 'h:mm:ss a'
  
  $.getJSON(timeOfDayAPI).done (data) ->
    dawn = data.times_of_day.dawn
    dusk = data.times_of_day.dusk
    noon = data.times_of_day.noon
    sunrise = data.times_of_day.sunrise
    sunset = data.times_of_day.sunset
    
    $('#js-dawn').append(moment(dawn).format(timeFormat))
    $('#js-dusk').append(moment(dusk).format(timeFormat))
    $('#js-noon').append(moment(noon).format(timeFormat))
    $('#js-sunrise').append(moment(sunrise).format(timeFormat))
    $('#js-sunset').append(moment(sunset).format(timeFormat))
    
    if data.is_night
      $('#js-time-of-day').append('Night')
    
    if data.is_day
      $('#js-time-of-day').append('Day')
    
    if data.is_astronomical_twilight
      $('#js-time-of-day').append('Astronomical Twilight')
    
    if data.is_civil_twlight
      $('#js-time-of-day').append('Civil Twilight')
    
    if data.is_nautical_twlight
      $('#js-time-of-day').append('Nautical Twilight')