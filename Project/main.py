import warnings
import utils as ut
from audio_steg import DSSS_Steg
import evaluate as evl
import visualize as vs
import argparse
from os import path


def run_encode(audio_list_org, sample_rate, original_msg,
               dsss, alpha, smooth_signal, steg_file_path):
    # encode and write to file
    enc_audio = dsss.encode(audio_list_org, original_msg, alpha=alpha, smooth_signal=smooth_signal)

    if enc_audio is not None:
        ut.write_audio_sf(steg_file_path, enc_audio, sample_rate)


def run_decode(audio_list_org, original_msg,
               dsss, steg_file_path, plot=True):
    # read steg file and decode message
    audio_list_stego, sample_rate = ut.read_audio(steg_file_path)
    decoded_msg = dsss.decode(audio_list_stego)
    print(f'Decoded message: {decoded_msg}')

    # evaluate
    print("BER: ", evl.bit_error_rate(original_msg, decoded_msg))
    print("NC: ", evl.normalized_corr_coef(original_msg, decoded_msg))
    print("MSE: ", evl.mse(audio_list_org, audio_list_stego))
    print("PSNR: ", evl.psnr(audio_list_org, audio_list_stego))

    if plot:
        vs.plot_signals(audio_list_org, audio_list_stego)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-e', '--encode', action='store_true',
                        help="Encode data.")
    parser.add_argument('-d', '--decode', action='store_true',
                        help="Decode data.")
    parser.add_argument('-c', '--cover_signal', type=str, default='./audio_in/Bankok.wav',
                        help="Path of the cover file.")
    parser.add_argument('-m', '--message', type=str, default='./audio_in/msg.txt',
                        help="Path of the message file.")
    parser.add_argument('-k', '--key', type=str, help="Stego key.")
    parser.add_argument('-s', '--stego_signal', type=str, default='./audio_steg/steg_out.wav',
                        help="Path of the stego file.")
    parser.add_argument('-p', '--pn_freq', type=int, default=4 * 1024,
                        help="Minimal PN sequence freq.")
    parser.add_argument('-a', '--alpha', type=float, default=0.002,
                        help="Strength factor.")
    parser.add_argument('-f', '--hanning_filter', action='store_true',
                        help="Use Hanning smoothing.")
    parser.add_argument('--plot', action='store_true',
                        help="Plot results.")

    args = parser.parse_args()

    # DSSS_Steg object
    dsss = DSSS_Steg(args.key, args.pn_freq)

    # read cover file
    if not path.exists(args.cover_signal):
        warnings.warn("Cover file not found!")
        return

    audio_list_org, sample_rate = ut.read_audio(args.cover_signal)
    #

    # original message
    if not path.exists(args.message):
        warnings.warn("Message file not found!")
        return

    msg_file = open(args.message)
    original_msg = msg_file.read()
    print(f'Original message: {original_msg}')
    #

    # run encode
    if args.encode:
        # encode
        run_encode(audio_list_org, sample_rate, original_msg,
               dsss, args.alpha, args.hanning_filter, args.stego_signal)
    #

    # run decode
    if args.decode:
        if not path.exists(args.stego_signal):
            warnings.warn("Stego file not found!")
            return

        run_decode(audio_list_org, original_msg, dsss, args.stego_signal, args.plot)
    #


if __name__ == '__main__':
    main()
