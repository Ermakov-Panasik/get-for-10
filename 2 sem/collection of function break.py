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
place = str('C:\\Users\\Admin\\Documents\\py\\sputnik')  #'C:\\Users\\hp\\Desktop\\sputnik'

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
    with open(place + '\\' + name, 'r') as file:
        lines = file.readlines()
    return [lines[58], lines[59]] #возврат 2 строк нужного tle

def CoordToDec(lon, lat, r):
    lat = math.radians(lat)
    lon = math.radians(lon)
    x = r * math.cos(lat) * math.cos(lon)
    y = r * math.sin(lon) * math.cos(lat)
    z = r * math.sin(lat)
    return (x,y,z)


# функция возвращает список географических координат (долгота, широта, высота над поверхностью) в виде двумерного массива
# подразумевается, что наблюдение начинается в 00:00 дня track_day и длится dur минут,
# точки рассчитываются раз в step минут
# lon(-180, 180), lat(-90,90), r - над поверхностью!
# чтобы получить чисто сферические координаты - r+6370 км

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

        dec_coord = CoordToDec(lon, lat, alt + 6370)

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

#Функция, сохраняющая данные data в файл под именем name
def save_file_as (data, name):
    np.savetxt(place + '/' + name + ".txt", data, fmt = '%3.0d')

# функция возвращает расстояние между 2 точками в трёхмерном декартовом пространстве
def distance (coord1, coord2):
    return math.sqrt((float(coord1[0])-float(coord2[0])) ** 2 + (float(coord1[1])-float(coord2[1])) ** 2 + (float(coord1[2])-float(coord2[2])) ** 2)

 #функция принимает координаты статичной точки и путь до файла с координатами движущейся
def find_angle (lk_coord, traectory):
    with open(traectory, 'r') as file:
        lines = file.readlines()
        experiment_time = []
        angles = []
        for i in range(0, lines.size(), 1):
            data = (lines[i]).split()
            position = [data[0], data[1], data[2]]
            R1 = distance([0, 0, 0], lk_coord)
            R2 = distance([0, 0, 0], position)
            R3 = distance(lk_coord, position)
            if math.degrees(math.acos((R1 ** 2 + R3 ** 2 - R2 ** 2) / (2 * R1 * R3))) - 90 > 10:
                experiment_time.append(i)
                angles.append(math.degrees(math.acos((R1 ** 2 + R3 ** 2 - R2 ** 2) / (2 * R1 * R3))) - 90)
        # конвертировать experiment_time в формат ответа
        answer = np.arange(7 * len(experiment_time)).reshape(len(experiment_time), 7) #двумерный массив на 7 солбцов и нужное количество строк
        x0 = lk_coord[0] # для удобства вводим переменные - кординаты ЛК
        y0 = lk_coord[1] # так же это координаты вектора нормали к (а)
        z0 = lk_coord[2]
        xn = 0  # направление на север в касательной к шару плоскости (а), проходящей через лк
        yn = 0
        zn = (x0 ** 2 + y0 ** 2 + z0 ** 2) / z0

        for i in range(0, len(experiment_time), 1):
            data = (lines[experiment_time[i]]).split()
            answer[i] [1] = int(angles [i])
            answer[i] [2] = int(data [3])
            answer[i] [3] = int(data [4])
            answer[i] [4] = int(data [5])
            answer[i] [5] = int(data [6])
            answer[i] [6] = int(data [7])

            #расчёт азимута
            x1 = float(data[0]) # координаты спутника в данный момент
            y1 = float(data[1])
            z1 = float(data[2])
            k = float(1 - (x0*x1 + y0*y1 + z0*z1) / (x0 ** 2 + y0 ** 2 + z0 ** 2)) # коэффициент, для определения точки проекции спутника на плоскость (а)

            x2 = x1 + k*x0 # координаты проекции спутника на (а)
            y2 = y1 + k*y0
            z2 = z1 + k*z0

            R1 = distance([x2, y2, z2], lk_coord)
            R2 = distance([xn, yn, zn], lk_coord)
            R3 = distance([xn, yn, zn], [x2, y2, z2])
            fi = int(math.degrees(math.acos((R1 ** 2 + R1 ** 2 - R3 ** 2) / (2 * R1 * R2)))) # угол между направлением на север и спутником

            # найдём из фи азимут
            xp = float(-y0*z0 - y0*(x0 ** 2 + y0 ** 2)/z0) # координаты вектора (вектор р), перпендикулярного вектоу направления на север
            yp = float(x0*(x0 ** 2 + y0 ** 2)/z0 + x0*z0)

            R1 = distance([x0+xp, y0+yp, z0], lk_coord)
            R2 = distance([x2, y2, z2], lk_coord)
            R3 = distance([x0+xp, y0+yp, z0], [x2, y2, z2])
            fi2 = math.degrees(math.acos((R1 ** 2 + R1 ** 2 - R3 ** 2) / (2 * R1 * R2))) # угол между направлением на спутник и вектором р
            if fi2 > 90: # определяем, нужен ли пересчёт угла (fi от 0 до 180, азимут от 0 до 360)
                fi = int(360 - fi)
            answer[i] [0] = int(fi)
        print(answer)
    save_file_as (answer, "answer") #файл с данными в фомате: азимут, угол наклона, час, минута, д, м, г

try:
    tle = read_txt()
    print("Введите дату начала наблюдения и продолжительность в фомате: дд мм гггг (время в часах)")
    enter = str(input())
    enter_list = enter.split()
    length = int(enter_list[3]) * 60
    geo_coord = create_orbital_track_shapefile_for_day(date(int(enter_list[2]),int(enter_list[1]),int(enter_list[0])), 1, length, tle)
    save_file_as (geo_coord, "coord")
    lon_lk = 37.51814961433411  #координаты взяты из https://www.mapsdirections.info/ru/GPS-координаты-Google-Картах.html
    lat_lk = 55.93018181969348
    H_lk = 0.198 + 6370
    lk_coord = CoordToDec(lon_lk, lat_lk, H_lk)
    find_angle (lk_coord, place + "\\coord.txt")

except:
    print("something don't work")