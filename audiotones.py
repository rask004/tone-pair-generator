import numpy as np
import simpleaudio as sa
import time
import argparse

fs = 44100  # 44100 samples per second

def play_tone(tone):
    # Start playback
    play_obj = sa.play_buffer(tone, 1, 2, fs)

    # Wait for playback to finish before exiting
    play_obj.wait_done()

def create_tone(f, d=1.0, v=1.0):
    t = np.linspace(0, d, int(d * fs), False)

    note = np.sin(f * t * 2 * np.pi)

    vol_factor = int((2 ** (v * 15) - 1))
    audio = note * vol_factor / np.max(np.abs(note))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)
    return audio

def play_two_tone_pattern(freq_1, freq_2, d, p, v):
    audio = create_tone(freq_1, d, v)
    play_tone(audio)
    time.sleep(p)
    audio = create_tone(freq_2, d, v)
    play_tone(audio)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Settings for the tone pattern generator for Tinnitus Therapy.',
                                     epilog='''Use these settings to create pairs of tones played through speakers / headphones. 
                                     The tones will change frequency and converge, becoming more similar with each cycle.''',
                                     allow_abbrev=False)
    parser.add_argument('cycles', type=int, help='Number of times to play tone pairs. Must be a whole number of at least 1.')
    parser.add_argument('frequency', nargs=2, type=int, help='frequencies of the tones. Two whole numbers are expected. They should be in the range 100-20000.')
    parser.add_argument("-t", '--target-freq', type=int, help='''frequency to converge tones toward. Must be a whole number. Should be in the range 100-20000. 
                        Defaults to exactly between the two tone frequencies.''')
    parser.add_argument("-v", '--volume', default=50.0, type=float,
                        help='Volume to use when playing tones. A Number (percentage) from 0.0 - 100.0. Default is 50%.')
    parser.add_argument("-c", '--change-rate', default=50.0, type=float,
                        help='Rate to change frequencies by with each cycle. A Number (percentage) from 5.0 - 80.0. Default is 50%.')
    parser.add_argument("-d", '--tone-duration', default=1.0, type=float,
                        help='Time in Seconds, for each tone to play. Number ranging from 0.1 to 3.0. Default is 1 second.')
    parser.add_argument("-p", '--tone-pause', default=0.5, type=float,
                        help='Time in Seconds, to pause between individual tones. Number ranging from  0.1 to 3.0. Default is 0.5 seconds.')
    parser.add_argument("-l", '--long-pause', default=2.0, type=float,
                        help='Time in Seconds, to pause between pairs of tones. Number ranging from 0.1 to 3.0. Default is 1 second.')
    args = parser.parse_args()
    if args.cycles < 1:
        parser.error("cycles should be a whole number of 1 or greater.")
    if min(args.frequency) < 100:
        parser.error("the minimum frequency should be a whole number of 100 or greater.")
    if max(args.frequency) > 20000:
        parser.error("the maximum frequency should be a whole number of 20000 or less.")
    if args.target_freq and not (args.target_freq <= 20000 and args.target_freq >= 100):
        parser.error("the convergence frequency should be a whole number ranging from 100 to 20000.")
    if args.change_rate < 5.0 or args.change_rate > 80.0:
        parser.error("the rate of change for frequencies should be a decimal number (representing a percentage) ranging from 5.0 to 80.0.")
    if args.volume < 0.0 or args.volume > 100.0:
        parser.error("the volume should be a decimal number (representing a percentage) ranging from 0 to 100.")
    if args.tone_duration < 0.1 or args.tone_duration > 3.0:
        parser.error("the tone duration should be a decimal number in seconds, ranging from 0.1 to 3.0.")
    if args.tone_pause < 0.1 or args.tone_pause > 3.0:
        parser.error("the pause between individual tones should be a decimal number in seconds, ranging from 0.1 to 3.0.")
    if args.long_pause < 0.1 or args.long_pause > 3.0:
        parser.error("the long pause between tone pairs should be a decimal number in seconds, ranging from 0.1 to 3.0.")
    return args

def main():
    args = parse_arguments()
    frequency_max = max(args.frequency)
    frequency_min = min(args.frequency)
    frequency_center = int((frequency_max - frequency_min) / 2) + frequency_min
    if args.target_freq:
        frequency_center = args.target_freq
    change_factor = args.change_rate / 100.0
    volume = abs(args.volume) / 100.0
    play_two_tone_pattern(frequency_min, frequency_max, args.tone_duration, args.tone_pause, volume)
    for i in range(args.cycles - 1):
        time.sleep(args.long_pause)
        frequency_max -= int(abs(frequency_max - frequency_center) * change_factor)
        frequency_min += int(abs(frequency_min - frequency_center) * change_factor)
        play_two_tone_pattern(frequency_min, frequency_max, args.tone_duration, args.tone_pause, args.volume)


if __name__ == '__main__':
    main()

