import numpy as np
from qpskReciever import demodulator
#File to test the different functions through the code

import unittest

class TestCalculaMedia(unittest.TestCase):
    def testGetRRCosFilter(self):
        self.assertEqual(1,1)

    def testDemodulator(self):
        fs = 30
        ts = 1/fs
        T = 2
        samples_symbol = T*fs

        # First a random sequence of bits to send is created
        random_vector = np.random.randint(0,2,10000)
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


        bits = demodulator(final_signal,T,fs,0.75)
        self.assertEqual(bits,random_vector)


if __name__ == '__main__':
    unittest.main()

