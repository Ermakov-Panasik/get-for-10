import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np
import shutil
import os
import matplotlib.pyplot as plt

place = 'C:\\Users\\hp\\sputnik' #'C:\\Users\\Admin\\Documents\\py\\wav'

save_file = open(place + '\\' + "wav_read.txt", "a")

fs, data = wav.read(place + '\\' +'signal.wav')
print(fs)
print(len(data))

n = int(len(data) / (fs/2)) + 1
m = int(fs/2)

j = 0
p = 0
s = 0
A = [0] * n
for i in range(n):
    A[i] = [0] * m

for i in range(0, len(data), 1):
    A[s][p] = data[i]
    save_file.write(str(data[i]) + " ")
    j += 1
    p += 1
    if j == int(fs/2):
        save_file.write('\n')
        s += 1
        p = 0
    if j == fs-1:
        save_file.write('\n')
        j = 0
        i += 1
        s += 1
        p = 0

#график сигнала на 500 секунде
data_crop = A[500]
plt.figure(figsize=(12,4))
plt.plot(data_crop)
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.title("Signal")
plt.show()
