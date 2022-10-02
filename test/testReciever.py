from decimal import ROUND_HALF_DOWN
import numpy as np
from src.qpskReciever import *
from src.algorithms import *
import unittest

#File to test the different functions through the code

class TestREciever(unittest.TestCase):
    def testGetRRCosFilter(self):
        alpha  = 0.5
        Ts = 2
        fs = 30
        filter_time = 10*Ts

        t_index = np.linspace(int(-filter_time/2),int(filter_time/2),fs*filter_time)
        N = len(t_index)
        cos_filter,time_index = getFilter(N,alpha,Ts,fs)

        self.assertEqual(N,len(cos_filter))

    def testDemodulator(self):
        fs = 30
        ts = 1/fs
        T = 2
        alpha = 0.8
        samples_symbol = T*fs
        test_symbols = 100
        filter_time = 10*T

        t_index = np.linspace(int(-filter_time/2),int(filter_time/2),fs*filter_time)
        N = len(t_index)
  
        cos_filter,time_index_filter = getFilter(N,alpha,T,fs)

        # First a random sequence of bits to send is created
        random_vector = np.random.randint(0,2,test_symbols)
        random_vector_reshaped = np.reshape(random_vector,[int(len(random_vector)/2),2])

        signal_real = np.empty([0])
        signal_imag = np.empty([0])
        for i in range(0,len(random_vector_reshaped)):
            if random_vector_reshaped[i,1] == 0:
                signal_real = np.append(signal_real,-1*np.ones(samples_symbol))
            else:
                signal_real  = np.append(signal_real,np.ones(samples_symbol))
            
            if random_vector_reshaped[i,0] == 0:
                signal_imag = np.append(signal_imag,-1*np.ones(samples_symbol))
            else:
                signal_imag = np.append(signal_imag,np.ones(samples_symbol))
    
        final_signal = signal_real +1j*signal_imag
    
        final_signal_filtered  = filterSignal(final_signal,cos_filter)

        bits = demodulator(final_signal_filtered,T,fs)
        self.assertEqual(sum(np.abs(bits-random_vector)),0)

    """
    def testGetLPFilter(self):
        filter = getLPF()
        self.assertIsInstance(type(filter),type(list))
    """
    def testViterbiLengthEncoder(self):
        N = 1000
        random_vector = np.random.randint(0,2,N)
        encoded_bits = viterbiEncoding(random_vector)

        self.assertEqual(len(random_vector)*2,len(encoded_bits))

    def testViterbiDecoder(self):
        depth = 8
        N = 1000
        random_vector = np.random.randint(0,2,N)
        encoded_bits = viterbiEncoding(random_vector)
        encoded_bits = np.append(encoded_bits,np.zeros((1,depth*2),np.int8))
        decoded_bits = viterbiDecoding(encoded_bits,depth)
        decoded_bits = decoded_bits[0:len(random_vector)]
        self.assertEqual(sum(decoded_bits-random_vector),0)


if __name__ == '__main__':
    unittest.main()

