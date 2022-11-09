from scipy.io import wavfile
from algorithms import *
import json
import math
from qpskReciever import *

samplerate, data = wavfile.read('./exampleSignals3/testSignal.wav')


#Variable declaration
with open('src/parameters.json', 'r') as f:
  variables = json.load(f)

inphase = data[:,0]
quadrature = data[:,1]

total_array = inphase+1j*quadrature

fs = samplerate # Hz
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
#showSpectrum(RRCosFilter,fs)



#Process the array on batches of constant size
iterations = math.ceil(len(total_array)/batch_size)
for i in range(0,iterations):
    if i*batch_size+batch_size<= len(total_array):
        # Process a full batch
        array_process = total_array[batch_size*i:batch_size*i+batch_size]
    else:
        array_process = total_array[batch_size*i:len(total_array)]
    

    # Filtering the signal with the root raised cosine filter    
    final_signal_filtered  = filterSignal(array_process,RRCosFilter)

    # Getting one sample for each symbol
    sampled_signal = signalSampling(final_signal_filtered,symbol_period,fs)

    # Applying the costas phase correction algorithm
    signal_costas = costasAlgo(sampled_signal)

    # Demodulating the samples
    demodulated_bits = demodulator(signal_costas)

    # Calculate the phase shift
    phase_corrected_bits = calculatePhase(demodulated_bits,reference_code_encoded)

    phase_corrected_bits = np.append(phase_corrected_bits,np.zeros((1,decoding_depth*2),np.int8))

    # Channel decode the input bits
    decoded_bits = viterbiDecoding(phase_corrected_bits,decoding_depth)
    decoded_bits = decoded_bits[0:len(phase_corrected_bits)]