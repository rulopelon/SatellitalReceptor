# Code read the date from the .np files and decode the image frames
import numpy as np
import matplotlib.pyplot as plt
from pandas import array
from algorithms import *
from qpskReciever import *
from libhackrf import *
import math



#Variable declaration
fs = 1e6 # Hz
center_freq = 100e6 # Hz
num_samples = 10000 # number of samples returned per call to rx()
recieve = True
alpha = 0.6
symbol_period = 4
batch_size = 10*8192   # 20 image frames
reference_code = [0,1,1,0,1]
decoding_depth = 10

filter_time = 10*symbol_period
t_index = np.linspace(int(-filter_time/2),int(filter_time/2),fs*filter_time)
length_rrcos_filter = len(t_index)


# Filter to filter the recieved signal
RRCosFilter = getFilter(length_rrcos_filter,alpha,symbol_period,fs)

# Encode the reference secuence
reference_code_encoded = viterbiEncoding(reference_code)

# The filter is shown
showSpectrum(RRCosFilter,fs)

total_array = np.empty([0])
# Read all the files
for file in os.listdir("signals"):
    new_array = np.load(file)
    np.append(total_array, new_array)

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

    # Channel decode the input bits
    decoded_bits = viterbiDecoding(phase_corrected_bits,decoding_depth)