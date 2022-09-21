from asyncio.windows_events import NULL
import numpy as np 



def demodulator(input_signal,T,Fs,search_multiplier):
    #Funcion to demodulate the recieved input_signal
    Ts = 1/Fs

    final_vector = []

    #Split the input_signal on the real and imaginary part
    real_part = np.real(input_signal)
    imaginary_part = np.imag(input_signal)

    # Generate the base functions
    total_time = Ts*len(input_signal)
    # TODO
    t = np.linspace(0,total_time,total_time)# Creating the time vector 
    
    # The first ns seconds of input_signal are analyzed to get the first maximum, based on the symbol period and a multipier
    

    index_search = max_index

    while index_search+T*search_multiplier*Fs <= len(input_signal):
        # Passing the segment of signal to analyze to the
        real_bit,imaginary_bit, new_index = decisor(real_part[index_search:index_search+T*search_multiplier*Fs],imaginary_part[index_search:index_search+T*search_multiplier*Fs])
        
        #Updating the index to search
        index_search = index_search+new_index

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
