from asyncio.windows_events import NULL
import numpy as np 


def matchedFilter(signal,f1,f2,T,Ts):
    #Function to apply a matched filter for the signal recieved
    filtered_signal = np.convolve(signal,f1)
    
   
    return filtered_signal[T/Ts]
    

def decisor(signal_decide_f1,signal_decide_f2):
    signal_return_f1 = NULL
    signal_return_f2 = NULL

    if signal_decide_f1>0:
        signal_return_f1 = 0
    elif signal_decide_f1 <0:
        signal_return_f1 = 1

    if signal_decide_f2>0:
        signal_return_f2 = 0
    elif signal_decide_f2 <0:
        signal_return_f2 = 1

    return signal_return_f1,signal_return_f2

def demodulator(signal,T,Fc,Fs):
    #Funcion to demodulate the recieved signal
    Ts = 1/Fs

    final_vector = []

    #Split the signal on the real and imaginary part
    real_part = np.real(signal)
    imaginary_part = np.imag(signal)

    # Generate the base functions
    total_time = Ts*len(signal)
    # TODO
    t = np.linspace(0,total_time,total_time)# Creating the time vector 
    f1 = np.sqrt(2/T)*np.cos(2*np.pi*Fc*t)
    f2 = np.sqrt(2/T)*np.sin(2*np.pi*Fc*t)

    for i in len(real_part):
        #The signals are passed to the matched filter
        real_filtered = matchedFilter(real_part[i],f1,T,Ts)
        imaginary_filtered= matchedFilter(imaginary_part[i],f2,T,Ts)

        #Passing signals to the decisor
        
        real_detected,imag_detected =decisor(real_filtered,imaginary_filtered)
        final_vector.append([real_detected,imag_detected])
    return final_vector
