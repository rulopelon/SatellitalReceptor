import numpy as np
import adi 
import matplotlib.pyplot as plt



#Variable declaration
fs = 1e6 # Hz
center_freq = 100e6 # Hz
num_samples = 10000 # number of samples returned per call to rx()
recieve = True

sdr = adi.Pluto()
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 70.0 # dB
sdr.rx_lo = int(center_freq)
sdr.fs = int(fs)
sdr.rx_rf_bandwidth = int(fs) # filter width, just set it to the same as sample rate for now
sdr.rx_buffer_size = num_samples

while recieve:
    samples = sdr.rx() # receive samples off Pluto
    fft_signal = np.fft.fft(samples)
    frequency_axis = np.linspace(-0.5*fs,0.5*fs,num_samples)
    plt.plot(frequency_axis,np.abs(fft_signal),'.-')
