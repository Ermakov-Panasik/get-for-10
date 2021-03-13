import pathlib
import shutil
import os
import requests
import math
from datetime import datetime, date, timedelta
import spacetrack.operators as op
from spacetrack import SpaceTrackClient
from pyorbital.orbital import Orbital
import numpy as np
import pathlib

#путь до папки, куда будут сохраняться файлы
place = str('C:\\Users\\Admin\\Documents\\py\\sputnik')

def read_txt ():
    try:
        shutil.rmtree(place)
    except OSError:
        print ("Deletion of the directory %s failed" % place)
    else:
        print ("Successfully deleted the directory %s" % place)
    try:
        os.mkdir(place)
    except OSError:
        print ("Creation of the directory %s failed" % place)
    else:
        print ("Successfully created the directory %s" % place)
    try:
        os.mkdir(place)
    except OSError:
        print ("Creation of the directory %s failed" % place)
    else:
        print ("Successfully created the directory %s " % place)

    name = ("TLE.txt")
    data = requests.get("http://celestrak.com/NORAD/elements/noaa.txt", allow_redirects=True)
    open(place + '/' + name, 'wb').write(data.content)
    with open(place + '/' + name, 'r') as file:
        lines = file.readlines()
    return [lines[58], lines[59]] #вывод 2 строк нужного tle

def CoordToDec(lon, lat, r):
    lat = (90-lat)*math.pi/180
    lon = lon*math.pi/180
    x = r * math.sin(lat) * math.cos(lon)
    y = r * math.sin(lon) * math.cos(lat)
    z = r * math.cos(lat)
    return (x,y,z)


# функция возвращает список географических координат (долгота, широта, высота над поверхностью) в виде двумерного массива
# подразумевается, что наблюдение начинается в 00:00 дня track_day и длится dur минут,
# точки рассчитываются раз в step минут
# lon(-180, 180), lat(-90,90), r - над поверхностью!
# чтобы получить чисто сферические координаты - r+6400 км

def create_orbital_track_shapefile_for_day (track_day, step, dur, tle):
    # получаем TLE для NOAA-19
    tle_1 = str(tle[0])
    tle_2 = str(tle[1])
 
     # Создаём экземляр класса Orbital
    orb = Orbital("N", line1=tle_1, line2=tle_2)

    i = 0
    minutes = 0

    coord = np.arange(8*dur).reshape(dur, 8)

    while minutes < dur:
        # Расчитаем час, минуту, секунду (для текущего шага)
        utc_hour = int(minutes // 60)
        utc_minutes = int((minutes - (utc_hour*60)) // 1)
        utc_seconds = int(round((minutes - (utc_hour*60) - utc_minutes)*60))
        utc_string = str(utc_hour) + '-' + str(utc_minutes) + '-' + str(utc_seconds)
        utc_time = datetime(track_day.year,track_day.month,track_day.day,utc_hour,utc_minutes,utc_seconds)
 
        # Считаем положение спутника
        lon, lat, alt = orb.get_lonlatalt(utc_time)

        dec_coord = CoordToDec(lon, lat, alt+6400)

        coord[i] [0] = int(dec_coord[0])
        coord[i] [1] = int(dec_coord[1])
        coord[i] [2] = int(dec_coord[2])
        coord[i] [3] = int(utc_hour+3)
        coord[i] [4] = int(utc_minutes)
        coord[i] [5] = int(track_day.day)
        coord[i] [6] = int(track_day.month)
        coord[i] [7] = int(track_day.year)

        i += 1
        minutes += step

    return coord # возвращает координаты и время в формате: x, y, z, час, минута, д, м, гггг (время местное = Московское)

try:
    tle = read_txt()
    print("Введите дату начала наблюдения и продолжительность в фомате: дд мм гггг (время в часах)")
    enter = str(input())
    enter_list = enter.split()
    length = int(enter_list[3]) * 60
    geo_coord = create_orbital_track_shapefile_for_day(date(int(enter_list[2]),int(enter_list[1]),int(enter_list[0])), 1, length, tle)
    name = "coord.txt"
    np.savetxt(place + '/' + name, geo_coord, fmt = '%3.0d')
except:
    print("something don't work")