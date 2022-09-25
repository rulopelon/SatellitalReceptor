from operator import index
import numpy as np 



def demodulator(input_signal,T,fs,search_multiplier):
    #Funcion to demodulate the recieved input_signal
    Ts = 1/fs
    # Array to output the result of the demodulation
    output_vector = []
    #input_signal  = input_signal/max(np.abs(input_signal))
    #Split the input_signal on the real and imaginary part
    real_part = np.real(input_signal)
    imaginary_part = np.imag(input_signal)

    index_search  = int(T*fs/2)
    #Search for the first symbol
    index_search = index_search+np.argmax(np.abs(real_part[index_search:index_search*2]))

    while index_search+int(T*fs/2) <= len(input_signal):
        # Passing the segment of signal to analyze to the
        bits = decisor(real_part[index_search],imaginary_part[index_search])
        
        #Updating the index to search
        index_search = index_search+int(T*fs)

        # Writting the results to the output array
        output_vector.append([bits])


    return np.reshape(output_vector,[len(output_vector)*2,]) 

def decisor(signal_real_decide, signal_imag_decide):

    #max_index_real = np.argmax(np.abs(signal_real_decide))
    #max_index_imaginary = np.argmax(np.abs(signal_imag_decide))
    
       
    if signal_real_decide >0 and signal_imag_decide >0:
        bits = [1,1]
    elif signal_real_decide >0 and signal_imag_decide <0:
        bits = [0,1]
    elif signal_real_decide <0 and signal_imag_decide <0:
        bits = [0,0]
    else:
        bits = [1,0]

    return bits
