from operator import index
import numpy as np 



def demodulator(input_signal,T,fs):
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

    while index_search <= len(input_signal):
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

def calculatePhase(input_bits,reference_code):
    # Module to calculate the phase shift of the recieved constellation
    # Only counter clok-wise shifts are considered
    # There are four possible situations: 
    # 1. There is no rotation
    # 2. There is a rotation of pi/2
    # 3. There is a rotation of pi
    # 4. There is a rotation of 3*pi/4
    # To calculate the shift, the input bits are going to be correlated with a reference vector
    
    # First of all the input array is reshaped on pairs
    paired_bits = np.reshape(input_bits,[len(input_bits)/2,2])
    
    pi_2_phase_array =np.zeros([len(input_bits)/2,2])
    pi_phase_array =np.zeros([len(input_bits)/2,2])
    pi_3_4_phase_array =np.zeros([len(input_bits)/2,2])
    

    # The first phase shift is pi/2
    for i in range(0,len(len(input_bits)/2)-1):
        bits = str(paired_bits[0])+str(paired_bits[1])
        # Calculate the integer value of the pair of bits
        value = int(bits,2)
        if value == 0:
            pi_2_phase_array[i,0] = 1
            pi_2_phase_array[i,1] = 0
        elif value == 1:
            pi_2_phase_array[i,0] = 0
            pi_2_phase_array[i,1] = 0
        elif value == 2:
            pi_2_phase_array[i,0] = 1
            pi_2_phase_array[i,1] = 1
        else:
            pi_2_phase_array[i,0] = 0
            pi_2_phase_array[i,1] = 1

    # The second phase shift is pi
    for i in range(0,len(len(input_bits)/2)-1):
        bits = str(paired_bits[0])+str(paired_bits[1])
        # Calculate the integer value of the pair of bits
        value = int(bits,2)

        if value == 0:
            pi_phase_array[i,0] = 1
            pi_phase_array[i,1] = 1
        elif value == 1:
            pi_phase_array[i,0] = 1
            pi_phase_array[i,1] = 0
        elif value == 2:
            pi_phase_array[i,0] = 0
            pi_phase_array[i,1] = 1
        else:
            pi_phase_array[i,0] = 0
            pi_phase_array[i,1] = 0

    # The third phase shift is 3*pi/4
    for i in range(0,len(len(input_bits)/2)-1):
        bits = str(paired_bits[0])+str(paired_bits[1])
        # Calculate the integer value of the pair of bits
        value = int(bits,2)
        
        if value == 0:
            pi_3_4_phase_array[i,0] = 0
            pi_3_4_phase_array[i,1] = 1
        elif value == 1:
            pi_3_4_phase_array[i,0] = 1
            pi_3_4_phase_array[i,1] = 1
        elif value == 2:
            pi_3_4_phase_array[i,0] = 0
            pi_3_4_phase_array[i,1] = 0
        else:
            pi_3_4_phase_array[i,0] = 1
            pi_3_4_phase_array[i,1] = 0

    # Reshape the arrays
    pi_2_phase_array = np.reshape(pi_2_phase_array,[len(input_bits),1])
    pi_phase_array = np.reshape(pi_phase_array,[len(input_bits),1])
    pi_3_4_phase_array = np.reshape(pi_3_4_phase_array,[len(input_bits),1])

    # Perform the correlation of the different shifts with the input sequence
    no_shift_correlation = np.correlate(input_bits,reference_code)
    pi_2_correlation = np.correlate(pi_2_phase_array,reference_code)
    pi_correlation = np.correlate(pi_phase_array,reference_code)
    pi_3_4_correlation = np.correlate(pi_3_4_phase_array,reference_code)

    # Get the maximum of each correlation
    no_shift_max = np.max(no_shift_correlation)
    pi_2_max = np.max(pi_2_correlation)
    pi_max = np.max(pi_correlation)
    pi_3_4_max = np.max(pi_3_4_correlation)

    # Get the maximun among the maximuns
    maximums_array = [no_shift_max,pi_2_max,pi_max,pi_3_4_max]
    maximum = np.argmax(maximums_array)
    
    # Return the array
    if maximum == 0:
        bits_return = input_bits
    elif maximum == 1:
        bits_return = pi_2_phase_array
    elif maximum == 2:
        bits_return = pi_phase_array
    else:
        bits_return = pi_3_4_phase_array

    return bits_return