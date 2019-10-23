import pyaudio
import numpy as np
p = pyaudio.PyAudio()

def play(volume, duration, f):
    # TODO: fix samples to reduce noise in the end of the sound.
    fs = 44100       # sampling rate, Hz, must be integer

    # generate samples, note conversion to float32 array
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    # play. May repeat with different volume values (if done interactively) 
    stream.write(volume*samples)

    stream.stop_stream()
    stream.close()

if __name__ == '__main__':
    volume = 1.0     # range [0.0, 1.0]
    duration = 2.0   # in seconds, may be float
    f = 440.0        # sine frequency, Hz, may be float
    play(volume, duration, f)
    play(0.5, duration, 800)
    p.terminate()
