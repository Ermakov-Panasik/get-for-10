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

def find_impulse(data, first_it):
    id = first_it
    for i in range(first_it, len(data)-91, 1):
        counter = 0
        for j in range (0, 84, 14):
            if abs(data[i+j] - 1800) > 1600 or abs(data[i+j+7]-data[i+j]) > 21500 or abs(data[i+j+7]-data[i+j]) < 3000: 
                counter = counter+1
        if counter <= 2:
            id = i
            break 
    return id


place = 'C:\\Users\\hp\\sputnik' #'C:\\Users\\hp\\sputnik''C:\\Users\\Admin\\Documents\\py\\wav'

save_file = open(place + '\\' + "wav_read.txt", "a")

fs, data = wav.read('C:\\Users\\hp\\sputnik\\signal.wav')
print(fs)
print(len(data))
def save_file_as (data, name):
    np.savetxt(place + '\\' + name + ".txt", data, fmt = '%3.0d')

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

save_file_as(data_am, "data_with_exception") # только для тестирования
max_value = max(data_am) # избавление от выбросов
exception = []
for i in range(0, len(data_am), 1):
    if (data_am[i] >= 0.9*max_value):
        exception.append(i)
if (len(exception) <= 0.00001*len(data_am)):
    print("we have any exceptions")
    for i in range(0, len(exception), 1):
        data_am[exception[i]] = 0
    max_value = max(data_am)
    for i in range(0, len(exception), 1):
        data_am[exception[i]] = max_value

print(max_value)
save_file_as(data_am, "data_without_exception") # только для тестирования

new_data = np.zeros((len(data_am), 1))
elem = int(0)
it = find_impulse(data_am, 0)
while it <= len(data_am) - int(fs*0.5):
    for j in range(it, it + int(fs*0.5), 1):
        new_data[elem] = data_am[j]
        elem += 1
    k = it + int(fs*0.5) - 50
    it = find_impulse(data_am, k)

save_file_as(new_data, "new_data")

w = int(0.5*fs) #длина одной линии = ширина кадра
h = data_am.shape[0]//w #высота кадра
image = Image.new('RGB', (w, h))

it = find_impulse(data_am, 0)
print(it)

px, py = 0, 0
for p in range(new_data.shape[0]):
    light = int(new_data[p]/max_value * 255)
    if light < 0: light = 0
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