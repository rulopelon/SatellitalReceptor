# Code just to recieve data from the sdr and store it
import numpy as np
import matplotlib.pyplot as plt
from algorithms import *
from qpskReciever import *
from libhackrf import *
import json
import adi 

#Variable declaration
with open('src/parameters.json', 'r') as f:
  variables = json.load(f)

#Variable declaration
fs = int(variables['fs']) # Hz
center_freq = int(variables['center_freq']) # Hz
num_samples = int(variables['num_samples_rx']) # number of samples returned per call to rx()
alpha = float(variables['alpha'])
symbol_period = int(variables['symbol_period'])
recieve = True



hackrf = HackRF()

hackrf.sample_rate = int(fs)
hackrf.center_freq = int(center_freq)
hackrf.enable_amp()


sdr = adi.Pluto()
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 70.0 # dB
sdr.rx_lo = int(center_freq)
sdr.fs = int(fs)
sdr.rx_rf_bandwidth = int(fs) # filter width, just set it to the same as sample rate for now
sdr.rx_buffer_size = num_samples


i = 0
while recieve:
    samples = sdr.rx() # receive samples

    # Save the samples
    np.save(str(i)+'.npy',samples)    

    # Add one iteration
    i =i+1    