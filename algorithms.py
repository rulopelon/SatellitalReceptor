import compy.filters as filter
import numpy as np
import matplotlib.pyplot as plt


def costasAlgo(samples,Ts):
    # imaginary por el seno
    real_signal = np.zeros((len(samples),))
    imag_signal = np.zeros((len(samples),))
    
    #Variables initialization
    phase_correction = 0
    alpha = 0.132
    beta = 0.00932
    
    #Vector for the time
    total_time = Ts*len(samples)
    t = np.linspace(0,total_time,total_time)# Creating the time vector

    for i in len(samples):
        im_part = np.imag(samples[i])
        real_part = np.real(samples[i])
        #The sample is multiplied by the phase correction

        im_part_corrected = im_part*np.sin(2*np.pi*t[i]+phase_correction)
        real_part_corrected = real_part*np.cos(2*np.pi*t[i]+phase_correction)
        
        real_signal[i] = real_part_corrected
        imag_signal[i]= im_part_corrected

        #Calculating the new phase shift
        if real_part > 0:
            a = 1.0
        else:
            a = -1.0
        if im_part > 0:
            b = 1.0
        else:
            b = -1.0

        error =  a * im_part - b * real_part
        phase =(error*beta)+(alpha*error)
        
        phase_correction =phase

    #Filtering the signal
    lpf = getLPF()
    real_signal_filtered = filterSignal(real_signal,lpf)
    imag_signal_filtered = filterSignal(imag_signal,lpf)

    return np.complex(real_signal_filtered,imag_signal_filtered)
    
def getLPF():
    pass
def getFilter(N,alpha,Ts,Fs):
    return filter.rrcosfilter(N,alpha,Ts,Fs)

def filterSignal(signal,filter):
    filtered_signal = np.convolve(filter,signal)
    return filtered_signal[len(filter)-1:]

def showSpectrum(signal,fs):
    fft_signal = np.fft.fft(signal)
    frequency_axis = np.linspace(-0.5*fs,0.5*fs,len(signal))
    plt.plot(frequency_axis,np.abs(fft_signal),'.-')

    