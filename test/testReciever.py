import numpy as np
from src.qpskReciever import *
from src.algorithms import *
import unittest

#File to test the different functions through the code

class TestREciever(unittest.TestCase):
    def testGetRRCosFilter(self):
        N = 200
        alpha  = 0.5
        Ts = 2
        fs = 30

        cos_filter = getFilter(N,alpha,Ts,fs)

        self.assertEqual(N,len(cos_filter))

    def testDemodulator(self):
        fs = 30
        ts = 1/fs
        T = 2
        N  = 200
        alpha = 0.5
        samples_symbol = T*fs

        cos_filter,time_index_filter = getFilter(N,alpha,T,fs)

        # First a random sequence of bits to send is created
        random_vector = np.random.randint(0,2,10)
        random_vector_reshaped = np.reshape(random_vector,[int(len(random_vector)/2),2])

        signal_real = np.empty([0])
        signal_imag = np.empty([0])

        for i in range(0,len(random_vector_reshaped)-1):
            if random_vector_reshaped[i,0] == 0:
                signal_real = np.append(signal_real,-1*np.ones(samples_symbol))
            else:
                signal_real  = np.append(signal_real,np.ones(samples_symbol))
            
            if random_vector_reshaped[i,1] == 0:
                signal_imag = np.append(signal_imag,-1*np.ones(samples_symbol))
            else:
                signal_imag = np.append(signal_imag,np.ones(samples_symbol))
    
        final_signal = signal_real +1j*signal_imag
    
        final_signal  = filterSignal(final_signal,cos_filter)

        bits = demodulator(final_signal,T,fs,0.75)
        self.assertEqual(bits,random_vector)


if __name__ == '__main__':
    unittest.main()

