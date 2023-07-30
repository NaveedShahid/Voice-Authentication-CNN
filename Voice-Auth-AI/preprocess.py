import librosa
import numpy as np
from scipy.signal import lfilter, butter
from python_speech_features import sigproc

import parameters as p


def load(filename, sample_rate):
    audio, sr = librosa.load(filename, sr=sample_rate, mono=True)
    audio = audio.flatten()
    return audio


def normalize_frames(m,epsilon=1e-12):
    return np.array([(v - np.mean(v)) / max(np.std(v),epsilon) for v in m])


# Valuable dc and dither removal function implemented 
# https://github.com/christianvazquez7/ivector/blob/master/MSRIT/rm_dc_n_dither.m
def remove_dc_and_dither(sin, sample_rate):
    if sample_rate == 16e3:
        alpha = 0.99
    elif sample_rate == 8e3:
        alpha = 0.999
    else:
        print("Sample rate must be 16kHz or 8kHz only")
        exit(1)
    sin = lfilter([1,-1], [1,-alpha], sin)
    dither = np.random.random_sample(len(sin)) + np.random.random_sample(len(sin)) - 1
    spow = np.std(dither)
    sout = sin + 1e-6 * spow * dither
    return sout


def get_fft_spectrum(filename, buckets):
    signal = load(filename,p.SAMPLE_RATE)
    signal *= 2**15

    # get FFT spectrum
    signal = remove_dc_and_dither(signal, p.SAMPLE_RATE)
    signal = sigproc.preemphasis(signal, coeff=p.PREEMPHASIS_ALPHA)
    frames = sigproc.framesig(signal, frame_len=p.FRAME_LEN*p.SAMPLE_RATE, frame_step=p.FRAME_STEP*p.SAMPLE_RATE, winfunc=np.hamming)
    fft = abs(np.fft.fft(frames,n=p.NUM_FFT))
    fft_norm = normalize_frames(fft.T)

    # truncate to max bucket sizes
    rsize = max(k for k in buckets if k <= fft_norm.shape[1])
    rstart = int((fft_norm.shape[1]-rsize)/2)
    out = fft_norm[:,rstart:rstart+rsize]

    return out
