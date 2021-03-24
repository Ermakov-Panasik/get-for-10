import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np
import shutil
import os
import matplotlib.pyplot as plt
from PIL import Image

# преобразование Гилберта
def hilbert(data):
    analytical_signal = signal.hilbert(data)
    amplitude_envelope = np.abs(analytical_signal)
    return amplitude_envelope

place = 'C:\\Users\\hp\\sputnik' #'C:\\Users\\Admin\\Documents\\py\\wav'

save_file = open(place + '\\' + "wav_read.txt", "a")

fs, data = wav.read(place + '\\' +'signal.wav')
print(fs)
print(len(data))

# # визуализация сигнала и получение матрицы

# n = int(len(data) / (fs/2)) + 1
# m = int(fs/2)

# j = 0
# p = 0
# s = 0
# A = [0] * n
# for i in range(n):
#     A[i] = [0] * m

# for i in range(0, len(data), 1):
#     A[s][p] = data[i]
#     save_file.write(str(data[i]) + " ")
#     j += 1
#     p += 1
#     if j == int(fs/2):
#         save_file.write('\n')
#         s += 1
#         p = 0
#     if j == fs-1:
#         save_file.write('\n')
#         j = 0
#         i += 1
#         s += 1
#         p = 0

# data_crop = A[500]
# plt.figure(figsize=(12,4))
# plt.plot(data_crop)
# plt.xlabel("Samples")
# plt.ylabel("Amplitude")
# plt.title("Signal")
# plt.show()

data_am = hilbert(data) #раскрытие амплитудной модуляции с помощью преобразования Гилберта


# # Визуализация промодулированного сигнала
# data_am_crop = data_am[200*fs:201*fs]
# data_crop = data[200*fs:201*fs]

# plt.figure(figsize=(12,4))
# plt.plot(data_crop)
# plt.plot(data_am_crop)
# plt.xlabel("Samples")
# plt.ylabel("Amplitude")
# plt.title("Signal")
# plt.show()

w = int(0.5*fs) #длина одной линии = ширина кадра
h = data_am.shape[0]//w #высота кадра
image = Image.new('RGB', (w, h))

px, py = 0, 0
for p in range(data_am.shape[0]):
    lum = int(data_am[p]//32 - 32)
    if lum < 0: lum = 0
    if lum > 255: lum = 255
    image.putpixel((px, py), (0, lum, 0))
    px += 1
    if px >= w:
        if (py % 50) == 0:
            print(f"Line saved {py} of {h}")
        px = 0
        py += 1
        if py >= h:
            break
image = image.resize((w, 4*h))
plt.imshow(image)
plt.show()