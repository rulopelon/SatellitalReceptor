import numpy as np
import adi 
import matplotlib.pyplot as plt
from algorithms import *
from qpskReciever import *


#Variable declaration
fs = 1e6 # Hz
center_freq = 100e6 # Hz
num_samples = 10000 # number of samples returned per call to rx()
recieve = True
alpha = 0.6
symbol_period = 4
N  = 100

sdr = adi.Pluto()
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 70.0 # dB
sdr.rx_lo = int(center_freq)
sdr.fs = int(fs)
sdr.rx_rf_bandwidth = int(fs) # filter width, just set it to the same as sample rate for now
sdr.rx_buffer_size = num_samples

#Filter to filter the recieved signal
RRCosFilter = getFilter(N,alpha,symbol_period,fs)
# The filter is shown
showSpectrum(RRCosFilter,fs)

i = 0
while recieve:
    samples = sdr.rx() # receive samples off Pluto
    np.save(str(i)+'.npy')

    print("Recieved signal")
    showSpectrum(samples,fs)
    
    # Recovering frecuency and phase 
    synchronized_signal = costasAlgo(samples,fs)

    # Filter the samples
    filtered_signal = filterSignal(synchronized_signal,RRCosFilter)

    print("Filtered signal")
    showSpectrum(filtered_signal,fs)

    #Decoding the bit on each channel

    # Saving the decoded signal
    i =i+1    