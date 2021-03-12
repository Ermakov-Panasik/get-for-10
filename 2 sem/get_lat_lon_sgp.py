from datetime import datetime, date, timedelta
import spacetrack.operators as op
from spacetrack import SpaceTrackClient
from pyorbital.orbital import Orbital
import numpy as np
import pathlib

# функция возвращает список географических координат (долгота, широта, высота над поверхностью) в виде двумерного массива
# стоит еще добавить возвращение времени в utc для каждой точки
# подразумевается, что наблюдение начинается в 00:00 дня track_day и длится dur минут,
# точки рассчитываются раз в step минут

# lon(-180, 180), lat(-90,90), r - над поверхностью!
# чтобы получить чисто сферические координаты - r+6400 км

def create_orbital_track_shapefile_for_day (track_day, step, dur):
    # получаем TLE для NOAA-19
    tle_1 = '1 33591U 09005A   21067.53688389  .00000027  00000-0  40065-4 0  9999'
    tle_2 = '2 33591  99.1917  85.7021 0014730  58.0337 302.2263 14.12454575622414'
 
     # Создаём экземляр класса Orbital
    orb = Orbital("N", line1=tle_1, line2=tle_2)

    i = 0
    minutes = 0

    coord = np.arange(3*dur).reshape(dur, 3)

    while minutes < dur:
        # Расчитаем час, минуту, секунду (для текущего шага)
        utc_hour = int(minutes // 60)
        utc_minutes = int((minutes - (utc_hour*60)) // 1)
        utc_seconds = int(round((minutes - (utc_hour*60) - utc_minutes)*60))
        utc_string = str(utc_hour) + '-' + str(utc_minutes) + '-' + str(utc_seconds)
        utc_time = datetime(track_day.year,track_day.month,track_day.day,utc_hour,utc_minutes,utc_seconds)
 
        # Считаем положение спутника
        lon, lat, alt = orb.get_lonlatalt(utc_time)

        coord[i] [0] = lon
        coord[i] [1] = lat
        coord[i] [2] = alt #или alt + 6400

        i += 1
        minutes += step

    return coord


geo_coord = create_orbital_track_shapefile_for_day(date(2021,3,10), 1, 20)
print (geo_coord)

# записать массив в файл - пока не получается
# open( path + '/geo_coord.txt', 'wb').write(create_orbital_track_shapefile_for_day(date(2021,3,13), 1, 20))