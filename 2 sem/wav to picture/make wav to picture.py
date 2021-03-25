import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np
import shutil
import os
import matplotlib.pyplot as plt
from PIL import Image
import array

# преобразование Гилберта
def hilbert(data):
    analytical_signal = signal.hilbert(data)
    amplitude_envelope = np.abs(analytical_signal)
    return amplitude_envelope

place = 'C:\\Users\\Admin\\Documents\\py\\wav' #'C:\\Users\\hp\\sputnik'

save_file = open(place + '\\' + "wav_read.txt", "a")

fs, data = wav.read('C:\\Users\\Admin\\Documents\\py\\signal.wav')
print(fs)
print(len(data))
if fs%2 > 0:
    fs += 2
# def save_file_as (data, name):
#     np.savetxt(place + '\\' + name + ".txt", data, fmt = '%3.0d')

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

# избавимся от сдвига в начале
# max_value = max(data_am)
# for i in range(0, len(data_am), 1):
#     if data_am[i] >= 0.75 * max_value:
#         count = int(0)
#         change = int(0)
#         for j in range(i, i+50, 1):
#             if data_am[j] >= 0.75 * max_value:
#                 count += 1
#         if count >= 10:
#             it = i
#             change = 1
#             i = len(data_am)
# for i in range(0, len(data_am) - 2000, 1):
#     data_am[i] = data_am[i+2000]

# # избавимся от шумов
# save_file_as(data_am, "data_after_hilbert")
# max_value = max(data_am)
# print(max_value)
# data_am_without_noise = []
# size_data = []
# new_str = []
# it1 = int(0)
# it2 = int(0)
# count = int(0)
# change = bool(0)
# for i in range(0, len(data_am), 1):
#     if data_am[i] >= 0.8 * max_value:
#         count = 0
#         change = 0
#         for j in range(i, i+50, 1):
#             if data_am[j] >= 0.75 * max_value:
#                 count += 1
#         if count >= 20:
#             if it1 == 0:
#                 it2 = i
#                 it1 = 1
#             else:
#                 it1 = it2-110
#                 it2 = i+100
#             i = i+100
#             change = 1
    
#     if change == 1:
#         sum = int(0)
#         for j in range(it1, it2, 1):
#             new_str.append(data_am[j])
#             sum += data_am[j]
#         if sum / (it2-it1) >= 0.7 * max_value:
#             new_str.clear()
#         else:
#             data_am_without_noise.append(new_str)
#             size_data.append(it2-it1)
#             new_str.clear()

# max_size = max(size_data)
# for i in range(0, len(data_am_without_noise), 1):
#     for j in range(size_data[i], max_size, 1):
#         data_am_without_noise[i].append(int(max_value))

# data_am.clear()
# for i in range(0, len(data_am_without_noise), 1):
#     data_am.append(data_am_without_noise[i])
# fs = max_size

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

max_value = max(data_am)
w = int(0.5*fs) #длина одной линии = ширина кадра
h = data_am.shape[0]//w #высота кадра
image = Image.new('RGB', (w, h))

px, py = 0, 0
for p in range(data_am.shape[0]):
    light = int(data_am[p]/max_value * 255)
    if light < 0: light = 0
    if light > 255: light = 255
    image.putpixel((px, py), (light, light, light))
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