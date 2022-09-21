
from asyncio.windows_events import NULL
import numpy as np 



def demodulator(input_signal,T,fs,search_multiplier):
    #Funcion to demodulate the recieved input_signal
    Ts = 1/fs
    # Array to output the result of the demodulation
    output_vector = []

    #Split the input_signal on the real and imaginary part
    real_part = np.real(input_signal)
    imaginary_part = np.imag(input_signal)

    index_search  =0
    # The first ns seconds of input_signal are analyzed to get the first maximum, based on the symbol period and a multipier
  
    while index_search+T*search_multiplier*fs <= len(input_signal):
        # Passing the segment of signal to analyze to the
        real_bit,imaginary_bit, new_index = decisor(real_part[index_search:index_search+T*search_multiplier*fs],imaginary_part[index_search:index_search+T*search_multiplier*fs])
        
        #Updating the index to search
        index_search = index_search+new_index

        # Writting the results to the output array
        output_vector.append([real_bit,imaginary_bit])

    return np.reshape(output_vector,[len(output_vector)*2,]) 

def decisor(signal_real_decide, signal_imag_decide):

    max_index_real = np.argmax(np.abs(signal_real_decide))
    max_index_imaginary = np.argmax(np.abs(signal_imag_decide))
    
    bit_real = NULL
    bit_imaginary = NULL

    # TODO
    # Decide the recieved bit on one channel
    if signal_real_decide[max_index_real] >0:
        bit_real = 0
    else:
        bit_real = 1
    
    # Decide the recieved bit on the other channel
    if signal_imag_decide[max_index_imaginary] >0:
        bit_imaginary = 0
    else:
        bit_imaginary = 1

    return bit_real,bit_imaginary,max_index_real
