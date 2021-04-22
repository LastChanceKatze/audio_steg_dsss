from math import floor
import utils as ut
import numpy as np


def mix(segment_length, msg_bits, upper, lower, k):

    if 2 * k > segment_length:
        k = floor(segment_length/4) - (floor(segment_length/4) % 4)

    k = k - (k % 4)

    # get bits array from bit string
    msg_bits_len = len(msg_bits)
    bits_arr = ut.bits_to_array(msg_bits)

    # matrix shape (segment_length, msg_bits_len)
    # replicate message segment_length times
    matrix = np.ones(shape=(segment_length, 1)) * bits_arr
    # reshape matrix to array
    msg_signal = np.reshape(matrix, msg_bits_len * segment_length, order='F')

    # smooth msg_signal
    # convolve with hanning filter
    conv = np.convolve(msg_signal, np.hanning(k))
    # normalize
    msg_signal_smooth = conv[k//2:- k//2 + 1] / max(abs(conv))

    # convert signal range to [-1, 1]
    msg_signal_smooth = msg_signal_smooth * (upper - lower) + lower
    msg_signal = msg_signal * (upper - lower) + lower

    return msg_signal_smooth, msg_signal
