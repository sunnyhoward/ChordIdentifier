# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 20:28:05 2020

@author: Sally
"""
import numpy as np
import struct
import matplotlib.pyplot as plt
import wave

a=0
option = input('Is the audio a single note (s) or a chord? (c) ')
while a==0:
    if option != 's' and option != 'c':
        print("that is not a correct answer, please enter 's' or 'c'.")
        option = input('Is the audio a single note (s) or a chord? (c) ')
    else:
        a=1

sound_file = wave.open('d string.wav', 'r')
file_length = sound_file.getnframes()   #Decode Audio File
samplerate = sound_file.getframerate()

       
sound = np.zeros(file_length)
for i in range(file_length):
    data = sound_file.readframes(1)
    data = struct.unpack("h", data)
    sound[i] = int(data[0])
    
sound = np.square(sound)

plt.plot(np.arange(file_length),sound)

plt.plot(np.arange(file_length)[4000:20000],sound[4000:20000])

chord1 = sound#[4000:20000]

fourier = np.fft.fft(chord1)
freq = np.fft.fftfreq(len(chord1),1/samplerate)

plt.plot(freq,fourier.real,freq,fourier.imag)
plt.plot(freq[1:4000],fourier.real[1:4000])
#plt.plot(freq[1:4000],fourier.imag[1:4000])


sortorder = np.argsort(np.absolute(fourier)**2)

bestfreqs = freq[sortorder[-10:]]

if option=='s':
    freqofnote = bestfreqs[0]
    print('the frequency of the note is ' + str(freqofnote))
