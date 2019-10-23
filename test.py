import pyaudio
import numpy as np
p = pyaudio.PyAudio()


def play(vol1, vol2, f1, f2, duration):
    '''Play two different sound.
    Credit: https://stackoverflow.com/a/27978895/7057866
    '''
    # TODO: fix samples to reduce noise in the beginning and end of the sound.

    fs = 44100       # sampling rate, Hz, must be integer

    # generate samples, note conversion to float32 array
    samples1 = (np.sin(2*np.pi*np.arange(fs*duration)*f1/fs)).astype(np.float32)
    samples2 = (np.sin(2*np.pi*np.arange(fs*duration)*f2/fs)).astype(np.float32)

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    # play. May repeat with different volume values (if done interactively) 
    stream.write(vol1*samples1)
    stream.write(vol2*samples2)

    stream.stop_stream()
    stream.close()


def ending_message(vol1, vol2, f1, f2):
    print("volume1: {}\tvolume2: {}".format(vol1, vol2))
    print("freq1: {}\tfreq2: {}".format(f1, f2))


if __name__ == '__main__':
    base_volume = 0.5     # range [0.0, 1.0]
    duration = 2.0   # in seconds, may be float
    f1 = 400.0        # sine frequency, Hz, may be float
    f2 = 600.0        # sine frequency, Hz, may be float
    print("Please tell if the volumes of the two sounds are identical.")
    print("- The volumes are NOT identical --> [Enter]")
    print("- The volumes are identical --> y [Enter]")
    print()
    input("Press [Enter] to start >> ")

    for i in range(10):
        ref_volume = i / 10
        play(base_volume, ref_volume, f1, f2, duration)
        print("sample {}:".format(i + 1))
        ans = input(">> ")
        if ans == "y":
            break
    ending_message(base_volume, ref_volume, f1, f2)
    p.terminate()
