# Code read the date from the .np files and decode the image frames
import numpy as np
import matplotlib.pyplot as plt
from pandas import array
from algorithms import *
from qpskReciever import *
import math
import json
import os



#Variable declaration
with open('src/parameters.json', 'r') as f:
  variables = json.load(f)

fs = int(variables['fs']) # Hz
center_freq = int(variables['center_freq']) # Hz
num_samples = int(variables['num_samples_rx']) # number of samples returned per call to rx()
alpha = float(variables['alpha'])
symbol_period = float(variables['symbol_period'])
batch_size = int(variables['batch_size'])   # 10 image frames
reference_code = variables['reference_code']
decoding_depth = int(variables['decoding_depth'])

filter_time = 10*symbol_period
t_index = np.linspace(int(-filter_time/2),int(filter_time/2),math.ceil(fs*filter_time)) # fs*filter_time
length_rrcos_filter = len(t_index)


# Filter to filter the recieved signal
RRCosFilter,time_index_filter = getFilter(length_rrcos_filter,alpha,symbol_period,fs)

# Encode the reference secuence
reference_code_encoded = viterbiEncoding(reference_code)

# The filter is shown
showSpectrum(RRCosFilter,fs)

total_array = np.empty([0])
# Read all the files
for file in os.listdir("exampleSignals"):
    new_array = np.load("exampleSignals/"+file)
    total_array = np.append(total_array, new_array)
    

final_bits = np.empty([0])

#Process the array on batches of constant size
iterations = math.ceil(len(total_array)/batch_size)
for i in range(0,iterations):
    if i*batch_size+batch_size<= len(total_array):
        # Process a full batch
        array_process = total_array[batch_size*i:batch_size*i+batch_size]
    else:
        array_process = total_array[batch_size*i:len(total_array)]
    
    # Process the signal on the costa algorithm
    signal = costasAlgo(array_process,1/fs)
    
    # Filter the signal with the adapted filter
    signal_filtered  = filterSignal(signal,RRCosFilter)

    # Decode the recieved signal
    demodulated_bits = demodulator(signal_filtered,symbol_period,fs)

    # Calculate the phase shift
    phase_corrected_bits = calculatePhase(demodulated_bits,reference_code_encoded)

    phase_corrected_bits = np.append(phase_corrected_bits,np.zeros((1,decoding_depth*2),np.int8))

    # Channel decode the input bits
    decoded_bits = viterbiDecoding(phase_corrected_bits,decoding_depth)
    decoded_bits = decoded_bits[0:len(phase_corrected_bits)]
