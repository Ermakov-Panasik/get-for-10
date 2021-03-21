import wave
import numpy as np
import shutil
import os

#путь до папки, куда будут сохраняться файлы
place = str('C:\\Users\\Admin\\Documents\\py\\wav')

def read_wav ():
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

    name = ("wav_read.txt") # имя файла с данными
    try:
        with wave.open('C:\\Users\\Admin\\Documents\\py\\signal.wav') as file:
            data = file.readframes(file.getnframes())
            data_as_np_int16 = np.frombuffer(data, dtype=np.int16)
            data_as_np_float32 = data_as_np_int16.astype(np.float32)
            data_normalised = data_as_np_float32 / (2 ** 15)
            save_file = open(place + '\\' + name, "a")
            for i in range(0, len(data_as_np_float32), 1):
                save_file.write(str(data_as_np_float32[i]))
                save_file.write('\n')
        print("file was created")
    except:
        print("file wasn't created")

try:
    read_wav()
except:
    print("something don't work")