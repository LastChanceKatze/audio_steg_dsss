import utils as ut
from math import sqrt, log10
import numpy as np


def bit_error_rate(original_msg, retrieved_msg):
    original_bits = ut.text_to_bits(original_msg)
    retrieved_bits = ut.text_to_bits(retrieved_msg)

    msg_len = min(len(original_bits), len(retrieved_bits))
    original_bits = original_bits[:msg_len]
    retrieved_bits = retrieved_bits[:msg_len]

    diff = sum([original_bits[i] != retrieved_bits[i] for i in range(msg_len)])
    return diff / msg_len


def normalized_corr_coef(original_msg, retrieved_msg):
    original_bits = ut.bits_to_array(ut.text_to_bits(original_msg))
    retrieved_bits = ut.bits_to_array(ut.text_to_bits(retrieved_msg))

    msg_len = min(len(original_bits), len(retrieved_bits))
    original_bits = np.array(original_bits[:msg_len])
    retrieved_bits = np.array(retrieved_bits[:msg_len])

    corr = (original_bits.dot(retrieved_bits))\
           / sqrt(sum(original_bits) * sum(retrieved_bits))

    return corr


def mse(original_sig, stego_sig):
    sig_len = len(original_sig)
    error = sum((original_sig - stego_sig)**2) / sig_len
    return error


def psnr(original_sig, stego_sig):
    return 10*log10(1/mse(original_sig, stego_sig))