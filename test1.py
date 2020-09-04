# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 20:28:05 2020

@author: Sally
"""
import numpy as np
import struct
import matplotlib.pyplot as plt
import wave
import pandas as pd
import tkinter.filedialog
from pychord import note_to_chord

#filename = tkinter.filedialog.askopenfilename()

filename = 'C:/Users/admin/Documents/sunnycode/chord detector/echord.wav'

df = pd.read_csv(r'C:/Users/admin/Documents/sunnycode/chord detector/notefreqs.csv')


def findnote(freqofnote,df):
    notefreqs = df['Freq'].to_numpy()
    notefreqindex = np.argmin(np.absolute(freqofnote-notefreqs))
    note = df['Note'].iloc[notefreqindex]
    octave = str(df['Octave'].iloc[notefreqindex])
    
    return note,octave



a=0
option = input('Is the audio a single note (s) or a chord? (c) ')
while a==0:
    if option != 's' and option != 'c':
        print("that is not a correct answer, please enter 's' or 'c'.")
        option = input('Is the audio a single note (s) or a chord? (c) ')
    else:
        a=1

sound_file = wave.open(filename, 'r')
file_length = sound_file.getnframes()   #Decode Audio File
samplerate = sound_file.getframerate()

       
sound = np.zeros(file_length)
for i in range(file_length):
    data = sound_file.readframes(1)
    data = struct.unpack("h", data)
    sound[i] = int(data[0])
    
sound = np.square(sound)

#plt.plot(np.arange(file_length),sound)

plt.plot(np.arange(file_length)[4000:20000],sound[4000:20000])

chord1 = sound#[4000:20000]

fourier = np.fft.fft(chord1)
freq = np.fft.fftfreq(len(chord1),1/samplerate)

fourier = fourier[freq>2]
freq = freq[freq>2]

#plt.plot(freq,fourier.real,freq,fourier.imag)

plt.figure()
plt.plot(freq[1:4000],fourier.real[1:4000])
#plt.plot(freq[1:4000],fourier.imag[1:4000])


sortorder = np.argsort(np.absolute(fourier)**2)

bestfreqs = freq[sortorder[-10:]]

if option=='s':
    freqofnote = bestfreqs[-1]
    note,octave = findnote(freqofnote,df)
    print('The frequency of the note is ' + str(np.round(freqofnote,2))+' Hz')
    print('The note is '+ note+octave)
    
elif option == 'c':
    freq1 = bestfreqs[-1]
    freq2 = bestfreqs[-2]
    freq3 = bestfreqs[-3]
    freq4 = bestfreqs[-4]
    note1,octave1 = findnote(freq1,df)
    note2,octave2 = findnote(freq2,df)
    note3,octave3 = findnote(freq3,df)
    note4,octave4 = findnote(freq4,df)
    
    freqs = [freq1,freq2,freq3,freq4]
    octaves = np.asarray([octave1,octave2,octave3,octave4])
    notes = np.asarray([note1,note2,note3,note4])
    
    
    sortfreq = np.argsort(freqs)
    
    sortednotes = list(notes[sortfreq])
    sortedoctaves = list(octaves[sortfreq])

    #now need to find the root note. start by finding lowest frequency. 
        
    finalnotes = list(dict.fromkeys(sortednotes))
    
    
    
    print('this chord consists of the notes: ' + sortednotes[0] + sortedoctaves[0] + ' ' + sortednotes[1] + sortedoctaves[1]+ ' ' + sortednotes[2] + sortedoctaves[2]+' ' + sortednotes[3]+sortedoctaves[3])

    print('The chord is ' + str(note_to_chord(finalnotes)))
    
    
