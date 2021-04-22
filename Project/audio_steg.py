import warnings
import utils as ut
from math import floor
import numpy as np
import mixer


class DSSS_Steg:

    __num_reserved_bits = 40

    def __init__(self, key, min_segment_length):
        self.__key = key
        self.__min_segment_len = min_segment_length

    def encode(self, original_signal, msg, alpha=0.005, smooth_signal=True):
        # convert string message to bits array
        bin_text = ut.text_to_bits(msg)

        # lengths of signal and message
        signal_length = len(original_signal) - self.__num_reserved_bits
        msg_length = len(bin_text)

        # calculate the segment length
        # make sure the segment is big enough
        segment_length = floor(signal_length / msg_length)
        segment_length = max(self.__min_segment_len, segment_length)

        # number of segments
        # make sure number%8=0
        num_segments = floor(signal_length / segment_length)
        num_segments = num_segments - (num_segments % 8)

        # if message is too long for the cover file, stop encoding
        if msg_length > num_segments:
            warnings.warn("Message too long")
            return None

        # generate pseudo random noise of segment length
        pn = self.__prng(segment_length)
        pn = np.reshape(pn, newshape=(segment_length, 1))
        # expand the pn to num_segments*segment_length length
        # in order to match the signal
        pn = np.reshape(pn * np.ones(shape=(1, num_segments), dtype='int'),
                        newshape=(num_segments*segment_length), order='F')

        # create a signal that contains the hidden message, cr times
        msg_sig_smooth, msg_sig_original = mixer.mix(segment_length, bin_text, 1, -1, 256)

        # embed the message into the noise signal
        if smooth_signal:
            pn_msg = msg_sig_smooth * pn
        else:
            pn_msg = msg_sig_original * pn

        # add the pn with higher frequency to the original signal
        steg_signal = original_signal[: num_segments * segment_length] + alpha * pn_msg

        # add the rest of the original signal to the steg_signal
        signal_with_len = self.__embed_msg_length(original_signal, msg_length)
        steg_signal = np.append(steg_signal, signal_with_len[num_segments * segment_length:])

        return steg_signal

    def decode(self, steg_signal):
        signal_length = len(steg_signal) - self.__num_reserved_bits

        msg_length = self.__get_msg_length(steg_signal)

        # calculate the segment length
        # same as the encoder
        segment_length = floor(signal_length / msg_length)
        segment_length = max(self.__min_segment_len, segment_length)

        # calculate number of segments
        # same as the encoder
        num_segments = floor(signal_length / segment_length)
        num_segments = num_segments - (num_segments % 8)

        # divide the signal into segments, arrange in a matrix
        signal_matrix = np.reshape(steg_signal[:num_segments * segment_length],
                                   (segment_length, num_segments), order='F')

        # get the same pseudo random sequence
        pn = self.__prng(segment_length)

        data = np.empty(shape=num_segments, dtype='str')
        for i in range(num_segments):
            # calculate sum
            corr = sum(signal_matrix[:, i] * pn) / segment_length
            # decide val of original bit
            if corr < 0:
                data[i] = '0'
            else:
                data[i] = '1'

        # get original text from bits
        decoded_text = ut.bits_to_text(data)
        return decoded_text

    def __prng(self, length):
        # use key to generate seed for rand sequence
        password = 0
        for i in range(len(self.__key)):
            # transform string into integer
            password = password + ord(self.__key[i]) * i

        np.random.seed(password)

        # generate sequence in range [-1, 1]
        pn = 2 * np.random.randint(2, size=length) - 1
        return pn

    def __embed_msg_length(self, signal, msg_length):
        signal_cpy = np.copy(signal)

        msg_length_bits = ut.bits_to_array('{0:040b}'.format(msg_length))

        max_s = max(signal_cpy[-self.__num_reserved_bits:])
        min_s = min(signal_cpy[-self.__num_reserved_bits:])

        for i in range(0, len(msg_length_bits)):
            if msg_length_bits[i] == 0:
                msg_length_bits[i] = min_s
            else:
                msg_length_bits[i] = max_s

        signal_cpy[-self.__num_reserved_bits:] = msg_length_bits
        return signal_cpy

    def __get_msg_length(self, signal):
        max_s = max(signal[-self.__num_reserved_bits:])
        signal_slice = signal[-self.__num_reserved_bits:]

        msg_length_bits = []
        for i in range(0, self.__num_reserved_bits):
            if signal_slice[i] == max_s:
                msg_length_bits.append(1)
            else:
                msg_length_bits.append(0)

        msg_length = ut.bits_to_integer(msg_length_bits)
        return msg_length
