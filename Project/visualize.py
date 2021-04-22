import utils as ut
from matplotlib import pyplot as plt
import numpy as np


def plot_msg(msg):
    msg_bits = ut.bits_to_array(ut.text_to_bits(msg))

    x = np.arange(len(msg_bits))
    plt.step(x, y=msg_bits)
    plt.title("Message bits")
    plt.show()


def plot_signals(original_sig, stego_sig):
    fig, axs = plt.subplots(2, 1)
    fig.suptitle("Waveform plot")

    axs[0].plot(original_sig)
    axs[0].title.set_text("Original signal")

    axs[1].plot(stego_sig)
    axs[1].title.set_text("Stego signal")

    plt.show()
