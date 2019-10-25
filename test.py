import pyaudio
import numpy as np
import random
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


def test(base_volume, base_sound, reference_sound):
    ref_volume = random.randint(1, 10) / 10
    while True:
        play(base_volume, ref_volume, base_sound, reference_sound, 2.0)

        command = input('type + or - >> ')
        if command == '+':
            ref_volume += 0.1
        elif command == '-':
            ref_volume -= 0.1
        elif command == '':
            continue
        elif command == 'e':
            break

        else:
            print('please type + or -')

        if ref_volume < 0:
            ref_volume = 0
        elif 10 < ref_volume:
            ref_volume = 10
    return ref_volume


if __name__ == '__main__':
    base_volume = 0.5     # range [0.0, 1.0]
    print("Please tell if the volumes of the two sounds are identical.")
    print("- The volumes are NOT identical --> [Enter]")
    print("- The volumes are identical --> y [Enter]")
    print()
    name = input("Enter your name to start \n>> ")
    csv_lines = []

    base_sounds = [1200, 3400, 5600, 7800]
    ref_sounds = list(range(100, 11100, 1100))  # [100, 1200, 2300, 3400, 4500, 5600, 6700, 7800, 8900, 10000]
    # base_sounds = [5600, 7800]
    # ref_sounds = base_sounds.copy()  # [100, 1200, 2300, 3400, 4500, 5600, 6700, 7800, 8900, 10000]
    random.shuffle(base_sounds)
    for base_sound in base_sounds:
        random.shuffle(ref_sounds)
        for reference_sound in ref_sounds:
            ref_vol = test(base_volume, base_sound, reference_sound)
            print('base_volume', base_volume)
            print('base_sound', base_sound)
            print('reference_volume', ref_vol)
            print('reference_sound', reference_sound)
            csv_lines.append(','.join(str(e) for e in (name, base_volume, ref_vol, base_sound, reference_sound)))

    with open('output.csv', 'a') as f:
        f.write('\n'.join(csv_lines))

    # ending_message(base_volume, ref_volume, f1, f2)
    p.terminate()
