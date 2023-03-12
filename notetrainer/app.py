import argparse
import itertools
import random
import time

from notetrainer.theory import Key, Chord, NOTE_NAMES, ROMAN_NUMERALS, Mode


def parse_root(arg: str) -> int:
    try:
        return NOTE_NAMES.index(arg.upper())
    except ValueError:
        try:
            return int(arg)
        except ValueError:
            raise argparse.ArgumentTypeError


def parse_mode(arg: str) -> Mode:
    try:
        return Mode[arg.upper()]
    except KeyError:
        try:
            return Mode(int(arg))
        except ValueError:
            raise argparse.ArgumentTypeError

parser = argparse.ArgumentParser()
parser.add_argument('root', type=parse_root, help='root note of scale')
parser.add_argument('mode', type=parse_mode, help='mode of scale')
parser.add_argument('chords', nargs='+', help='4 chord progression, by degree')
parser.add_argument('--bpm', type=float, default=60.0, help='beats per minute')
parser.add_argument('--n-bars', type=int, default=8, help='number of bars to preview')
args = parser.parse_args()


def parse_chord(key: Key, chord: str) -> Chord:
    try:
        return Chord(key, ROMAN_NUMERALS.index(chord.upper()))
    except ValueError:
        return Chord(key, int(chord) - 1)


key = Key(args.root, args.mode)
chords = [parse_chord(key, chord) for chord in args.chords]

def get_chord(bar):
    chord = chords[bar % len(chords)]
    return f'{chord.guitar_notation():7s}|'

def get_melody(bar):
    notes = [random.choice((1, 3, 5, 7)) for _ in range(4)]

    return ' '.join(map(str, notes)) + '|'

chord_buffer = ''.join(get_chord(i) for i in range(args.n_bars + 1))
melody_buffer = ''.join(get_melody(i) for i in range(args.n_bars + 1))

print()
print()

for i in itertools.count():
    print('\r\033[2A', end='')

    print(chord_buffer[i % 8:i % 8 + 8 * args.n_bars])
    print(melody_buffer[i % 8:i % 8 + 8 * args.n_bars])
    time.sleep(30.0 / args.bpm)

    div, mod = divmod(i + 1, 8)
    if mod == 0:
        chord_buffer = chord_buffer[8:] + get_chord(div + args.n_bars + 1)
        melody_buffer = melody_buffer[8:] + get_melody(div + args.n_bars + 1)