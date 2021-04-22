import soundfile as sf
import numpy as np


def audio_info(audio):
    print("Samples in the file: ", audio.getnframes())
    print("Sampling rate of the file: ", audio.getframerate())
    print("Number of channels:", audio.getnchannels())
    print("Sampling width of file (bits per file: output*8):", audio.getsampwidth())
    length = round(int(audio.getnframes()) / int(audio.getframerate()), 3)
    print("Length in seconds of the file:", length, "seconds")


def read_audio(audio):
    data, sample_rate = sf.read(audio)
    return data, sample_rate


def write_audio_sf(file_path, audio, sample_rate):
    sf.write(file_path, audio, samplerate=sample_rate)


def text_to_bits(text):
    b_arr = bytearray(text, 'utf-8')
    res = ''.join(format(i, '08b') for i in b_arr)
    return res


def bits_to_array(bits_string):
    return list(int(i) for i in list(bits_string))


def bits_to_text(bits_arr):
    text = ""
    bytes_arr = np.split(bits_arr, int(len(bits_arr)/8))
    for c_arr in bytes_arr:
        char = ''.join(c_arr)
        text = text + chr(int(char, base=2))
    return text


def bits_to_integer(bits_arr):
    num = 0
    for bit in bits_arr:
        num = (num << 1) | int(bit)
    return num
