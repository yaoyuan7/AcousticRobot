# -*- coding: utf-8 -*-
import numpy as np
from scipy.io import wavfile
import wave
import matplotlib.pyplot as plt

# MY CODE

f1 = 100.     # Start frequency in [Hz]
f2 = 20000.  # End frequency in [Hz]
T  = 11.      # Pulse duration in [s]
fs = 44100.  # Sampling frequency in [Hz]
Ts = 1./fs   # Sampling period in [s]
N = np.floor(T/Ts)
n  = np.arange(0, N, dtype='float64')  # Sample index

om1 = 2*np.pi*f1
om2 = 2*np.pi*f2

#x_exp = 0.99*np.sin(om1*N*Ts / np.log(om2/om1) * (np.exp(n/N*np.log(om2/om1)) - 1))
bits=16
# louder signal
amplification = (2**(bits-1))
#amplification=1
factor = 0.8
x_exp = factor*amplification*np.sin(om1*N*Ts / np.log(om2/om1) * (np.exp(n/N*np.log(om2/om1)) - 1))


t_win = 0.1
n_win = np.floor(t_win*fs)
win = np.hanning(t_win*fs)
x_exp[:n_win/2] *= win[:n_win/2]
x_exp[-n_win/2:] *= win[-n_win/2:]

plt.figure()
plt.subplot(2,1,1)
plt.plot(x_exp)
plt.subplot(2,1,2)
plt.plot(np.log10(np.abs(np.fft.rfft(x_exp))))

x_exp_int = np.array(x_exp, dtype=np.int16)
# this creates a float64 file that pyaudio cannot read...
wavfile.write('audio/exp_sweep_new.wav', fs, x_exp_int)
'''
# therefore this is added...
nchannels=1
sampwidth=2 # in bytes


x_exp_binary = ''
for i in range(int(N)):
     x_exp_binary += wave.struct.pack('h',x_exp[i]) # transform to binary
f = SoundFile(x_exp_binary,'audio/exp_sweep_louder.wav')
f.write(nchannels,sampwidth,fs,T)
print("my file written")



writer = wave.Wave_write('new_wave')
writer.setnchannels(1)
writer.setframerate(44100)
writer.setnframes(x_exp.shape[0])
writer.setsampwidth(2)
writer.writeframes(x_exp)

'''