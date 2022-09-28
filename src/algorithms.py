import numpy as np
import matplotlib.pyplot as plt
import sk_dsp_comm.fec_conv as fec

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
    # TODO
    lpf = getLPF()
    real_signal_filtered = filterSignal(real_signal,lpf)
    imag_signal_filtered = filterSignal(imag_signal,lpf)

    return np.complex(real_signal_filtered,imag_signal_filtered)
    
def getLPF():

    with open('lpFilter.txt') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines
    

def getFilter(N,alpha,Ts,Fs):
    """
    Generates a root raised cosine (RRC) filter (FIR) impulse response.

    Parameters
    ----------
    N : int
        Length of the filter in samples.

    alpha : float
        Roll off factor (Valid values are [0, 1]).

    Ts : float
        Symbol period in seconds.

    Fs : float
        Sampling Rate in Hz.

    Returns
    ---------

    time_idx : 1-D ndarray of floats
        Array containing the time indices, in seconds, for
        the impulse response.

    h_rrc : 1-D ndarray of floats
        Impulse response of the root raised cosine filter.
    """

    T_delta = 1/float(Fs)
    time_idx = ((np.arange(N)-N/2))*T_delta
    sample_num = np.arange(N)
    h_rrc = np.zeros(N, dtype=float)

    for x in sample_num:
        t = (x-N/2)*T_delta
        if t == 0.0:
            h_rrc[x] = 1.0 - alpha + (4*alpha/np.pi)
        elif alpha != 0 and t == Ts/(4*alpha):
            h_rrc[x] = (alpha/np.sqrt(2))*(((1+2/np.pi)* \
                    (np.sin(np.pi/(4*alpha)))) + ((1-2/np.pi)*(np.cos(np.pi/(4*alpha)))))
        elif alpha != 0 and t == -Ts/(4*alpha):
            h_rrc[x] = (alpha/np.sqrt(2))*(((1+2/np.pi)* \
                    (np.sin(np.pi/(4*alpha)))) + ((1-2/np.pi)*(np.cos(np.pi/(4*alpha)))))
        else:
            h_rrc[x] = (np.sin(np.pi*t*(1-alpha)/Ts) +  \
                    4*alpha*(t/Ts)*np.cos(np.pi*t*(1+alpha)/Ts))/ \
                    (np.pi*t*(1-(4*alpha*t/Ts)*(4*alpha*t/Ts))/Ts)

    return h_rrc,time_idx

def filterSignal(signal,filter):
    filtered_signal = np.convolve(filter,signal)
    filtered_signal = filtered_signal[int((len(filter)-1)/2):]
    filtered_signal = filtered_signal[:len(filtered_signal)-int((len(filter)-1)/2)-1]
    #return filtered_signal[int((len(filter)-1)/2):]
    return filtered_signal

def filterLowPass(b,a,signal):
    # The filter signal could replace this but this is preferred as the filter could have a coeficients
    filtered_signal = signal.lfilter(b,a,signal)
    return filtered_signal

def showSpectrum(signal,fs):
    fft_signal = np.fft.fftshift(np.fft.fft(signal))
    frequency_axis = np.linspace(-0.5*fs,0.5*fs,len(signal))
    plt.plot(frequency_axis,np.abs(fft_signal),'.-')

def viterbiDecoding(input_bits,depth):
    #Creates the
    #https://scikit-dsp-comm.readthedocs.io/en/latest/_modules/sk_dsp_comm/fec_conv.html#FECConv
    cc1 = fec.FECConv(('1001111','1101101'),depth)
    signal_decoded = cc1.viterbi_decoder(input_bits,'hard')
    return signal_decoded.astype(int)

def viterbiEncoding(bits):
    #Function to perform the viterbi enconding of the input signal based on xor
    cc = fec.FECConv(('1001111','1101101'))
    encoded_bits, state = cc.conv_encoder(bits, '0000000')
    
    return encoded_bits.astype(int)
