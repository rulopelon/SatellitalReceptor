from asyncio.windows_events import NULL
import numpy as np 


def matchedFilter(signal,f1,f2,T,Ts):
    #Function to apply a matched filter for the signal recieved
    filtered_signal_f1 = np.convolve(signal,f1)
    filtered_signal_f2 = np.convolve(signal,f2)
    
   
    return filtered_signal_f1[T/Ts],filtered_signal_f2[T/Ts]
    

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

    #Split the signal on the real and imaginary part
    real_part = np.real(signal)
    imaginary_part = np.imag(signal)

    # Generate the base functions
    total_time = Ts*len(signal)
    # TODO
    t = np.linspace(0,total_time,total_time)# Creating the time vector 
    f1 = np.sqrt(2/T)*np.cos(2*np.pi*Fc*t)
    f2 = np.sqrt(2/T)*np.sin(2*np.pi*Fc*t)

    #The signals are passed to the matched filter
    real_f1,real_f2 = matchedFilter(real_part,f1,f2,T,Ts)
    imaginary_f1,imaginary_f2 = matchedFilter(imaginary_part,f1,f2,T,Ts)

    #Passing signals to the decisor
    # TODO
    decisor(real_f1,real_f2)
    decisor(imaginary_f1,imaginary_f2)
