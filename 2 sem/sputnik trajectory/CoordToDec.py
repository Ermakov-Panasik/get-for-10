import math

def CoordToDec(lon, lat, r):
    lat = math.radians(lat)
    lon = math.radians(lon)
    x = r * math.cos(lat) * math.cos(lon)
    y = r * math.sin(lon) * math.cos(lat)
    z = r * math.sin(lat)
    return (x,y,z)