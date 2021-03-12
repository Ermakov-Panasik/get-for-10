import pathlib
import shutil
import os
import requests
#import datetime

place = str('C:\\Users\\Admin\\Documents\\py\\sputnik')
print("it is work!", place)

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

def read_txt (go):
    if go == True:
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
        words1 = lines[58].split()
        words2 = lines[59].split()
        return [words1[3], words2[2], words2[3], words2[4], words2[5], words2[6], words2[7]]
       
try:
    data = read_txt(True)
    print(data)

except  KeyboardInterrupt:
    print("something don't work")