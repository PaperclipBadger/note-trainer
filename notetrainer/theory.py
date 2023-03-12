from typing import Sequence

import enum
import dataclasses
import functools
import re


NOTE_NAMES = ('A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯')
OCTAVE = 12
DIATONIC_SCALE = (0, 2, 4, 5, 7, 9, 11)
ROMAN_NUMERALS = ('I', 'II', 'III', 'IV', 'V', 'VI', 'VII')


class Mode(enum.IntEnum):
    IONIAN = 0
    DORIAN = 1
    PHRYGIAN = 2
    LYDIAN = 3
    MIXOLYDIAN = 4
    AEOLIAN = 5
    LOCRIAN = 6

    MAJOR = IONIAN
    MINOR = AEOLIAN


@dataclasses.dataclass(frozen=True)
class Key:
    RE = re.compile(r"""
        (?P<name>[A-G]♯?)
        (?P<mode>[Mm]?)
    """, flags=re.VERBOSE)

    root: int
    mode: Mode

    @classmethod
    def from_str(cls, keysig: str):
        """Parse a key from a string like C, CM, Cm."""
        if (match := cls.RE.match(keysig)):
            root = NOTE_NAMES.index(match.group('name'))

            if match.group('mode') == 'M':
                mode = Mode.MAJOR
            elif match.group('mode') == 'm':
                mode = Mode.MINOR
            else:
                mode = Mode.MAJOR
            
            return cls(root=root, mode=mode)
        else:
            raise ValueError(f'could not parse keysig {keysig}')
    
    def __str__(self):
        parts = [NOTE_NAMES[self.index % OCTAVE]]
        
        if self.mode == Mode.MINOR:
            parts.append('m')
        
        return ''.join(parts)
    
    @functools.cached_property
    def scale(self):
        N = len(DIATONIC_SCALE)
        diatonic_root = self.root - DIATONIC_SCALE[self.mode]

        def generator():
            for i in range(N):
                div, mod = divmod(i + self.mode, N)
                yield diatonic_root + DIATONIC_SCALE[mod] + OCTAVE * div

        return tuple(generator())
    
    @functools.cached_property
    def chords(self):
        return tuple(
            Chord(key=self, degree=i)
            for i in range(len(self.scale))
        )


@dataclasses.dataclass(frozen=True)
class Chord:
    key: Key
    degree: int

    @functools.cached_property
    def notes(self):
        N = len(self.key.scale)

        def generator():
            for i in range(N):
                div, mod = divmod(self.degree + i, N)
                yield self.key.scale[mod] + OCTAVE * div
        
        return tuple(generator())
    
    @property
    def root(self):
        return self.notes[0]

    @property
    def third(self):
        return self.notes[2]
    
    @property
    def fifth(self):
        return self.notes[4]
    
    @property
    def seventh(self):
        return self.notes[6]
        
    @functools.cached_property
    def is_major(self):
        return self.third - self.root == 4

    @functools.cached_property
    def is_minor(self):
        return self.third - self.root == 3

    @functools.cached_property
    def is_flat_fifth(self):
        return self.fifth - self.root == 6
    
    @functools.cached_property
    def is_sharp_fifth(self):
        return self.fifth - self.root == 8

    @functools.cached_property
    def is_minor_seventh(self):
        return self.seventh - self.root == 10

    @functools.cached_property
    def is_major_seventh(self):
        return self.seventh - self.root == 11

    @functools.cached_property
    def is_diminished(self):
        return self.is_minor and self.is_flat_fifth

    @functools.cached_property
    def is_augmented(self):
        return self.is_minor and self.is_sharp_fifth
    
    def degree_notation(self) -> str:
        assert self.is_major or self.is_minor

        roman_numeral = ROMAN_NUMERALS[self.degree]
        if self.is_minor:
            roman_numeral = roman_numeral.lower()

        parts = [roman_numeral]
        if self.is_diminished:
            parts.append('°')
        if self.is_augmented:
            parts.append('⁺')

        return ''.join(parts)

    def guitar_notation(self) -> str:
        assert self.is_major or self.is_minor

        name = NOTE_NAMES[self.root % OCTAVE]
        parts = [name]
        if self.is_minor:
            parts.append('m')
        if self.is_diminished:
            parts.append('°')
        elif self.is_flat_fifth:
            parts.append(' ♭5')
        if self.is_augmented:
            parts.append('⁺')
        elif self.is_sharp_fifth:
            parts.append(' ♯5')

        return ''.join(parts)