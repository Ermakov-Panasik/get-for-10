import math
def CoordToDec(lon, lat, r):
    lat = (90-lat)*math.pi/180
    lon = lon*math.pi/180
    x = r * math.sin(lat) * math.cos(lon)
    y = r * math.sin(lon) * math.cos(lat)
    z = r * math.cos(lat)

    return (x,y,z)

print(CoordToDec(180, 0, 6400))
