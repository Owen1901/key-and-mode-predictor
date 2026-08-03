from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
import colorsys
from statistics import mode

# Basic data
PITCHES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
pitch_to_index = {p:i for i,p in enumerate(PITCHES)}

# Qualities (matches parse_chord)
QUALITIES = [
    "minor6","6","major7","minor7","dominant7","major9","minor9", "minoradd9","add9","dominant9",
    "minor11","minoradd11","add11","11","major7sus2","minor7sus2","dominant7sus2","sus2",
    "major7sus4","minor7sus4","dominant7sus4","sus4","minor","major","diminished"
]

# Probability tables of several chords
LYDIAN_PROBS = {
    "I": 0.22, "Imaj7": 0.06, "II": 0.11, "iii": 0.05, "V": 0.07, "vi": 0.03, "vii": 0.03,
    "i": 0.004, "bII": 0.003, "bIII": 0.007, "III": 0.01, "bIV": 0.01, "IV": 0.005, "bVI": 0.007,
    "bVII": 0.003, "Vmaj7": 0.01, "bVImaj7": 0.002, "iii7": 0.01, "vi7": 0.01, "vii7": 0.02,
    "I7": 0.003, "II7": 0.009, "V7": 0.003, "Imaj9": 0.02, "iii9": 0.004, "II9": 0.003,
    "Iadd9": 0.01, "IIadd9": 0.006, "iiiadd9": 0.003, "II^4_2": 0.02, "V^6_4": 0.004,
    "vii^6": 0.004, "VII^6": 0.002, "I^6": 0.01, "VII^6_4": 0.002, "vii^6_4": 0.002, "II^6": 0.007,
    "II^6_5": 0.003, "I^6_4": 0.03, "iii^6": 0.004, "I^4_3": 0.003, "II^6_4": 0.005, "I^4_2": 0.002,
    "iii^6_4": 0.004, "V^6": 0.01, "I^4_2": 0.005, "vi^6_5": 0.003, "vii^6_5": 0.006,
    "iii^6_5": 0.003, "Isus2": 0.005, "Isus4": 0.005, "Imaj7sus2": 0.003, "IIsus2": 0.003,
    "IIsus4": 0.005, "vi7sus4": 0.002, "Iadd11": 0.005, "I7add11": 0.002, "II11": 0.002,
    "iii11": 0.004, "iv^o6_4": 0.005, "iv^o": 0.006, "vii^o": 0.002, "Other": 0.0005 * (0.22 / 0.18)
}

MAJOR_PROBS = {
    "I": 0.18, "Imaj7": 0.02, "ii": 0.03, "iii": 0.03, "IV": 0.12, "IVmaj7": 0.02, "V": 0.12,
    "vi": 0.07, "iv": 0.006, "v": 0.001, "II": 0.007, "bIII": 0.004, "III": 0.007, "VI": 0.004,
    "bVI": 0.005, "bVImaj7": 0.002, "bVII": 0.01, "bVIImaj7": 0.001, "VII": 0.001, "ii7": 0.03,
    "iii7": 0.02, "iv7": 0.001, "v7": 0.002, "vi7": 0.02, "I7": 0.005, "II7": 0.005, "III7": 0.006,
    "IV7": 0.001, "V7": 0.002, "VI7": 0.004, "Imaj9": 0.003, "IVmaj9": 0.003, "ii9": 0.003,
    "vi9": 0.001, "V9": 0.001, "Iadd9": 0.005, "IVadd9": 0.007, "Vadd9": 0.002, "IV^6_4": 0.007,
    "vi^6": 0.003, "ii^4_2": 0.002, "V^6_4": 0.004, "V^4_3": 0.002, "I^6": 0.02, "vi^6_4": 0.002,
    "I^6_5": 0.001, "V^4_2": 0.003, "ii^6": 0.002, "V^6/V": 0.001, "vi^4_2": 0.003,
    "iii^6_5": 0.003, "I^6_4": 0.01, "V^11": 0.005, "V11": 0.005, "V^6/vi": 0.001,
    "V^6_5/vi": 0.001, "iv^6": 0.001, "ii^6_4": 0.001, "IV^6": 0.005, "V^6": 0.01, "V^6_5": 0.001,
    "iii^6_4": 0.003, "I^4_2": 0.003, "vi^6_5": 0.004, "ii^6_5": 0.004, "ii^o6_5": 0.002,
    "iii^6_5": 0.003, "Isus2": 0.003, "Imaj7sus2": 0.001, "Isus4": 0.003, "IVsus2": 0.004, 
    "Vsus4": 0.007, "V7sus4": 0.003, "Vadd11": 0.001, "vii^o/V": 0.001, "vii^o": 0.002,
    "Other": 0.0005
}

MIXOLYDIAN_PROBS = {
    "I": 0.26, "ii": 0.02, "bIII": 0.03, "IV": 0.11, "v": 0.03, "VII": 0.14, "i": 0.002,
    "bII": 0.003, "II": 0.005, "iii": 0.001, "iv": 0.005, "bV": 0.002, "V": 0.02, "bVI": 0.02,
    "vi": 0.02, "bI": 0.001, "Imaj7": 0.002, "bIIImaj7": 0.003, "IVmaj7": 0.006, "bVImaj7": 0.004,
    "VIImaj7": 0.006, "i7": 0.002, "ii7": 0.007, "iv7": 0.001, "v7": 0.01, "vi7": 0.008, "I7": 0.03,
    "II7": 0.002, "IV7": 0.006, "V7": 0.004, "VII7": 0.002, "VIImaj9": 0.002, "I9": 0.003,
    "Iadd9": 0.006, "IVadd9": 0.004, "VIIadd9": 0.009, "I^11": 0.01, "I11": 0.01, "IV^6_4": 0.01,
    "iv^6_4": 0.002, "vi^6": 0.002, "ii^4_2": 0.003, "v^6_4": 0.001, "VII^6": 0.004, "I^6": 0.01,
    "I^6_5": 0.001, "ii^6": 0.002, "VII^6_4": 0.007, "I^6_4": 0.02, "I^4_3": 0.002, "iv^6": 0.002,
    "IV^6": 0.01, "I^4_2": 0.01, "v^6": 0.002, "IV^6_4/VII": 0.002, "vi^6_5": 0.005, "i^6_5": 0.001,
    "ii^6_5": 0.003, "v^6_5": 0.005, "Isus2": 0.005, "Isus4": 0.008, "I7sus4": 0.003,
    "IV^6_4sus4": 0.002, "IVsus2": 0.003, "vsus4": 0.002, "v7sus4": 0.002, "VIIsus2": 0.004,
    "Iadd11": 0.002, "ii11": 0.002, "v11": 0.002, "iii^o": 0.002, "Other": 0.0005 * (0.26 / 0.18)
}

DORIAN_PROBS = {
    "i": 0.19, "ii": 0.02, "III": 0.09, "IIImaj7": 0.009, "IV": 0.12, "v": 0.04, "VII": 0.08,
    "VIImaj7": 0.005, "I": 0.02, "bII": 0.003, "II": 0.004, "iv": 0.002, "bV": 0.003, "V": 0.01,
    "bVI": 0.02, "bVImaj7": 0.005, "vi": 0.001, "i7": 0.06, "ii7": 0.01, "iv7": 0.001, "v7": 0.01,
    "I7": 0.003, "II7": 0.001, "IV7": 0.02, "V7": 0.005, "VII7": 0.001, "IIImaj9": 0.001,
    "VIImaj9": 0.001, "i9": 0.01, "v9": 0.002, "IV9": 0.004, "IIIadd9": 0.002, "IVadd9": 0.004,
    "VIIadd9": 0.004, "iadd9": 0.004, "IV^6_4": 0.01, "ii^4_2": 0.005, "IV^4_3": 0.002,
    "VII^6": 0.007, "v^6_4": 0.002, "i^6": 0.01, "IV^4_2": 0.003, "ii^6": 0.004, "VII^6_4": 0.003,
    "IV^11": 0.002, "IV11": 0.002, "i^6_4": 0.01, "i^4_3": 0.002, "III^6": 0.003, "IV^6": 0.009,
    "ii^6_4": 0.001, "v^6": 0.003, "III^6_4": 0.005, "i^4_2": 0.008, "vi^o6_5": 0.007,
    "i^6_5": 0.006, "ii^6_5": 0.004, "v^6_5": 0.003, "isus2": 0.003, "isus4": 0.002,
    "i7sus2": 0.003, "i7sus4": 0.002, "IIIsus2": 0.001, "IVsus2": 0.002, "IVsus4": 0.004,
    "IV7sus2": 0.002, "IV7sus4": 0.001, "vsus4": 0.001, "VIIsus2": 0.001, "VIIsus4": 0.001,
    "iadd11": 0.002, "i11": 0.004, "v11": 0.002, "vi^o": 0.004, "vii^o/i": 0.001,
    "Other": 0.0005 * (0.19 / 0.18)
}

MINOR_PROBS = {
    "i": 0.18, "III": 0.06, "IIImaj7": 0.005, "iv": 0.05, "v": 0.04, "VI": 0.10, "VImaj7": 0.03,
    "VII": 0.10, "I": 0.01, "ii": 0.002, "IV": 0.01, "V": 0.03, "vii": 0.001, "bII": 0.005,
    "bIImaj7": 0.002, "II": 0.002, "bV": 0.002, "#vi": 0.001, "i7": 0.03, "iv7": 0.02, "v7": 0.02,
    "vii7": 0.002, "I7": 0.002, "II7": 0.001, "IV7": 0.002, "V7": 0.01, "VI7": 0.001, "VII7": 0.005,
    "VImaj9": 0.003, "i9": 0.005, "iv9": 0.004, "IIIadd9": 0.001, "VIadd9": 0.004, "VIIadd9": 0.003,
    "iadd9": 0.004, "ivadd9": 0.001, "VI^6": 0.004, "iv^6_4": 0.003, "VI^6_5": 0.002,
    "VII^6": 0.007, "V^6_4": 0.002, "v^6_4": 0.003, "VI^6_4": 0.003, "i^6": 0.01, "VII^6_4": 0.003,
    "i^6_4": 0.01, "III^6": 0.006, "VI^4_2": 0.001, "VII^4_2": 0.002, "iv^6": 0.004, "IV^6": 0.003,
    "i^4_2": 0.005, "v^6": 0.005, "III^6_4": 0.006, "VII^11": 0.001, "VII11": 0.001, "V^6": 0.006,
    "V^6_5": 0.002, "i^6_5": 0.003, "ii^o6_5": 0.002, "iv^6_5": 0.003, "v^6_5": 0.005,
    "isus2": 0.003, "isus4": 0.003, "i7sus2": 0.001, "ivsus2": 0.002, "iv7sus2": 0.001,
    "vsus4": 0.003, "v7sus4": 0.002, "VIsus2": 0.001, "VIIsus2": 0.001, "VIIsus4": 0.003,
    "i11": 0.003, "ii^o": 0.004, "vii^o/i": 0.003, "Other": 0.0005
}

PHRYGIAN_PROBS = {
    "i": 0.27, "II": 0.16, "III": 0.06, "iv": 0.04, "vii": 0.05, "I": 0.03, "ii": 0.002,
    "#ii": 0.004, "iii": 0.002, "#iii": 0.002, "IV": 0.008, "bV": 0.01, "v": 0.007, "V": 0.006,
    "VI": 0.03, "#vi": 0.002, "V/#ii": 0.002, "VII": 0.006, "V/#iii": 0.003, "#vii": 0.006,
    "iv^6_4": 0.005, "II^4_2": 0.004, "VI^6": 0.004, "vii^6": 0.007, "III^4_2": 0.002,
    "VI^6_4": 0.001, "i^6": 0.008, "iv^4_2": 0.002, "II^6": 0.003, "i^6_4": 0.01, "III^6": 0.002,
    "II^6_4": 0.006, "iv^6": 0.002, "i^4_2": 0.005, "III^6_4": 0.002, "i^4_2sus4": 0.002,
    "i7": 0.02, "isus2": 0.002, "isus4": 0.004, "i7sus4": 0.003, "iadd11": 0.002, "IIsus2": 0.002,
    "II7sus4": 0.002, "IImaj7": 0.03, "IImaj9": 0.003, "IIadd9": 0.002, "vii^6_5": 0.004,
    "III7": 0.002, "IIIadd6": 0.002, "iv7": 0.007, "iv9": 0.003, "ivsus2": 0.002, "iv7sus4": 0.002,
    "V7/i": 0.002, "VImaj7": 0.01, "vii7": 0.009, "viisus2": 0.002, "viiadd9": 0.001,
    "v^o6_4": 0.002, "v^o": 0.009, "Other": 0.0005 * (0.27 / 0.18)
}

LOCRIAN_PROBS = {
    "i": 0.04, "I": 0.02, "Imaj7": 0.009, "II^4_2": 0.01, "II": 0.09, "#ii": 0.01, "V/VI": 0.01,
    "iii": 0.07, "iii7": 0.01, "#iii": 0.009, "V/vii": 0.01, "iv": 0.06, "V": 0.14, "iii^6": 0.01,
    "VI": 0.04, "VI7": 0.009, "vii": 0.03,"i^o": 0.28, "#ii^o": 0.02, "i^o6": 0.02, "i^o6_4": 0.02,
    "#iv^o": 0.008, "vii^o": 0.009, "vii^o/i": 0.02, "Other": 0.0005 * (0.28 / 0.18)
}

# Take user's chord input and deconstruct it into its key and quality
def parse_chord(ch):
    ch = ch.strip()
    if ch.endswith("m6"):
        return ch[:-2], "minor6"
    elif ch.endswith("6"):
        return ch[:-1], "6"
    elif ch.endswith("maj7"):
        return ch[:-4], "major7"
    elif ch.endswith("m7"):
        return ch[:-2], "minor7"
    elif ch.endswith("7"):
        return ch[:-1], "dominant7"
    elif ch.endswith("maj9"):
        return ch[:-4], "major9"
    elif ch.endswith("m9"):
        return ch[:-2], "minor9"
    elif ch.endswith("madd9"):
        return ch[:-5], "minoradd9"
    elif ch.endswith("add9"):
        return ch[:-4], "add9"
    elif ch.endswith("9"):
        return ch[:-1], "dominant9"
    elif ch.endswith("m11"):
        return ch[:-3], "minor11"
    elif ch.endswith("madd11"):
        return ch[:-6], "minoradd11"
    elif ch.endswith("add11"):
        return ch[:-5], "add11"
    elif ch.endswith("11"):
        return ch[:-2], "11"
    elif ch.endswith("maj7sus2"):
        return ch[:-8], "major7sus2"
    elif ch.endswith("m7sus2"):
        return ch[:-6], "minor7sus2"
    elif ch.endswith("7sus2"):
        return ch[:-5], "dominant7sus2"
    elif ch.endswith("sus2"):
        return ch[:-4], "sus2"
    elif ch.endswith("maj7sus4"):
        return ch[:-8], "major7sus4"
    elif ch.endswith("m7sus4"):
        return ch[:-6], "minor7sus4"
    elif ch.endswith("7sus4"):
        return ch[:-5], "dominant7sus4"
    elif ch.endswith("sus4"):
        return ch[:-4], "sus4"
    elif ch.endswith("dim"):
        return ch[:-3], "diminished"
    elif ch.endswith("m"):
        return ch[:-1], "minor"
    else:
        return ch, "major"
    
# Parse a chord string possibly containing a slash bass (ex: Fsus2/C, where C is the bass, F is the
# root, and sus2 is the quality). Returns (root, quality, bass) where bass is None or a pitch name.
def parse_full_chord(ch):
    ch = ch.strip()
    if "/" in ch:
        upper, bass = ch.split("/", 1)
        upper = upper.strip()
        bass = bass.strip()
    else:
        upper, bass = ch, None
    root, quality = parse_chord(upper)
    return root, quality, bass

# Compute number of semitones (the interval) between two keys. Used in calculations that assign
# chord probabilities depending on which key a chord progression is proposed to be in.
def interval(a, b):
    return (pitch_to_index[b] - pitch_to_index[a]) % 12

# For each of the 12 keys (C, C#, D,...), take in an interval that the user's inputted chord is away
# from the root and the chord's quality and return the scale degree and quality (ex: Vmaj7) of that
# chord.
def degree_name(interval, upper_interval, bass_interval, quality, mode):
    if mode == "lydian":
        if interval == 0 and quality == "major": return "I"
        if interval == 0 and quality == "major7": return "Imaj7"
        if interval == 2 and quality == "major": return "II"
        if interval == 4 and quality == "minor": return "iii"
        if interval == 7 and quality == "major": return "V"
        if interval == 7 and quality == "major7": return "Vmaj7"
        if interval == 9 and quality == "minor": return "vi"
        if interval == 11 and quality == "minor": return "vii"
        if interval == 0 and quality == "minor": return "i"
        if interval == 1 and quality == "major": return "bII"
        if interval == 3 and quality == "major": return "bIII"
        if interval == 5 and quality == "major": return "bIV"
        if interval == 6 and quality == "major": return "IV"
        if interval == 8 and quality == "major": return "bVI"
        if interval == 8 and quality == "major7": return "bVImaj7"
        if interval == 10 and quality == "major": return "bVII"
        if interval == 4 and quality == "minor7": return "iii7"
        if interval == 9 and quality == "minor7": return "vi7"
        if interval == 11 and quality == "minor7": return "vii7"
        if interval == 0 and quality == "dominant7": return "I7"
        if interval == 2 and quality == "dominant7": return "II7"
        if interval == 7 and quality == "dominant7": return "V7"
        if interval == 0 and quality == "major9": return "Imaj9"
        if interval == 4 and quality == "minor9": return "iii9"
        if interval == 2 and quality == "dominant9": return "II9"
        if interval == 0 and quality == "add9": return "Iadd9"
        if interval == 2 and quality == "add9": return "IIadd9"
        if interval == 4 and quality == "minoradd9": return "iiiadd9"
        if upper_interval == 2 and bass_interval == 0 and quality == "dominant7": return "II^4_2"
        if upper_interval == 7 and bass_interval == 2 and quality == "major": return "V^6_4"
        if upper_interval == 11 and bass_interval == 2 and quality == "minor": return "vii^6"
        if upper_interval == 0 and bass_interval == 2 and quality == "major": return "I11"
        if upper_interval == 11 and bass_interval == 3 and quality == "major": return "VII^6"
        if upper_interval == 0 and bass_interval == 4 and quality == "major": return "I^6"
        if upper_interval == 11 and bass_interval == 6 and quality == "major": return "VII^6_4"
        if upper_interval == 11 and bass_interval == 6 and quality == "minor": return "vii^6_4"
        if upper_interval == 2 and bass_interval == 6 and quality == "major": return "II^6"
        if upper_interval == 2 and bass_interval == 6 and quality == "dominant7": return "II^6_5"
        if upper_interval == 0 and bass_interval == 7 and quality == "major": return "I^6_4"
        if upper_interval == 4 and bass_interval == 7 and quality == "minor": return "iii^6"
        if upper_interval == 0 and bass_interval == 7 and quality == "major7": return "I^4_3"
        if upper_interval == 2 and bass_interval == 9 and quality == "major": return "II^6_4"
        if upper_interval == 0 and bass_interval == 10 and quality == "dominant7": return "I^4_2"
        if upper_interval == 4 and bass_interval == 11 and quality == "minor": return "iii^6_4"
        if upper_interval == 7 and bass_interval == 11 and quality == "major": return "V^6"
        if upper_interval == 0 and bass_interval == 11 and quality == "major": return "I^4_2"
        if interval == 0 and quality == "6": return "vi^6_5"
        if interval == 2 and quality == "6": return "vii^6_5"
        if interval == 7 and quality == "6": return "iii^6_5"
        if interval == 0 and quality == "sus2": return "Isus2"
        if interval == 0 and quality == "sus4": return "Isus4"
        if interval == 0 and quality == "major7sus2": return "Imaj7sus2"
        if interval == 2 and quality == "sus2": return "IIsus2"
        if interval == 2 and quality == "sus4": return "IIsus4"
        if interval == 9 and quality == "dominant7sus4": return "vi7sus4"
        if interval == 0 and quality == "add11": return "Iadd11"
        if interval == 0 and quality == "dominant7add11": return "I7add11"
        if interval == 2 and quality == "11": return "II11"
        if interval == 4 and quality == "minor11": return "iii11"
        if upper_interval == 6 and bass_interval == 0 and quality == "diminished": return "iv^o6_4"
        if interval == 6 and quality == "diminished": return "iv^o"
        if interval == 11 and quality == "diminished": return "vii^o"
        return "Other"
    
    if mode == "major":
        if interval == 0 and quality == "major": return "I"
        if interval == 0 and quality == "major7": return "Imaj7"
        if interval == 2 and quality == "minor": return "ii"
        if interval == 4 and quality == "minor": return "iii"
        if interval == 5 and quality == "major": return "IV"
        if interval == 5 and quality == "major7": return "IVmaj7"
        if interval == 7 and quality == "major": return "V"
        if interval == 9 and quality == "minor": return "vi"
        if interval == 5 and quality == "minor": return "iv"
        if interval == 7 and quality == "minor": return "v"
        if interval == 2 and quality == "major": return "II"
        if interval == 4 and quality == "major": return "III"
        if interval == 3 and quality == "major": return "bIII"
        if interval == 8 and quality == "major": return "bVI"
        if interval == 8 and quality == "major7": return "bVImaj7"
        if interval == 9 and quality == "major": return "VI"
        if interval == 10 and quality == "major": return "bVII"
        if interval == 10 and quality == "major7": return "bVIImaj7"
        if interval == 11 and quality == "major": return "VII"
        if interval == 2 and quality == "minor7": return "ii7"
        if interval == 4 and quality == "minor7": return "iii7"
        if interval == 5 and quality == "minor7": return "iv7"
        if interval == 7 and quality == "minor7": return "v7"
        if interval == 9 and quality == "minor7": return "vi7"
        if interval == 0 and quality == "dominant7": return "I7"
        if interval == 2 and quality == "dominant7": return "II7"
        if interval == 4 and quality == "dominant7": return "III7"
        if interval == 5 and quality == "dominant7": return "IV7"
        if interval == 7 and quality == "dominant7": return "V7"
        if interval == 9 and quality == "dominant7": return "VI7"
        if interval == 0 and quality == "major9": return "Imaj9"
        if interval == 5 and quality == "major9": return "IVmaj9"
        if interval == 2 and quality == "minor9": return "ii9"
        if interval == 9 and quality == "minor9": return "vi9"
        if interval == 7 and quality == "dominant9": return "V9"
        if interval == 0 and quality == "add9": return "Iadd9"
        if interval == 5 and quality == "add9": return "IVadd9"
        if interval == 7 and quality == "add9": return "Vadd9"
        if upper_interval == 5 and bass_interval == 0 and quality == "major": return "IV^6_4"
        if upper_interval == 9 and bass_interval == 0 and quality == "minor": return "vi^6"
        if upper_interval == 2 and bass_interval == 0 and quality == "minor": return "ii^4_2"
        if upper_interval == 7 and bass_interval == 2 and quality == "major": return "V^6_4"
        if upper_interval == 7 and bass_interval == 2 and quality == "dominant7": return "V^4_3"
        if upper_interval == 0 and bass_interval == 4 and quality == "major": return "I^6"
        if upper_interval == 9 and bass_interval == 4 and quality == "minor": return "vi^6_4"
        if upper_interval == 0 and bass_interval == 4 and quality == "major7": return "I^6_5"
        if upper_interval == 7 and bass_interval == 5 and quality == "dominant7": return "V^4_2"
        if upper_interval == 2 and bass_interval == 5 and quality == "minor": return "ii^6"
        if upper_interval == 2 and bass_interval == 5 and quality == "minor": return"V^6/V"
        if upper_interval == 9 and bass_interval == 7 and quality == "minor": return "vi^4_2"
        if upper_interval == 4 and bass_interval == 7 and quality == "minor": return "iii^6_5"
        if upper_interval == 0 and bass_interval == 7 and quality == "major": return "I^6_4"
        if upper_interval == 5 and bass_interval == 7 and quality == "major": return "V^11"
        if interval == 7 and quality == "11": return "V11"
        if upper_interval == 2 and bass_interval == 9 and quality == "minor": return "ii^6_4"
        if upper_interval == 5 and bass_interval == 9 and quality == "major": return "IV^6"
        if upper_interval == 4 and bass_interval == 10 and quality == "major": return "V^6/vi"
        if upper_interval == 4 and bass_interval == 10 and quality == "dominant7": return "V^6_5/vi"
        if upper_interval == 5 and bass_interval == 10 and quality == "minor": return "iv^6"
        if upper_interval == 7 and bass_interval == 11 and quality == "major": return "V^6"
        if upper_interval == 4 and bass_interval == 11 and quality == "minor": return "iii^6_4"
        if upper_interval == 0 and bass_interval == 11 and quality == "major": return "I^4_2"
        if upper_interval == 7 and bass_interval == 11 and quality == "dominant7": return "V^6_5"
        if interval == 0 and quality == "6": return "vi^6_5"
        if interval == 5 and quality == "6": return "ii^6_5"
        if interval == 5 and quality == "minor6": return "ii^o6_5"
        if interval == 7 and quality == "6": return "iii^6_5"
        if interval == 0 and quality == "sus2": return "Isus2"
        if interval == 0 and quality == "sus4": return "Isus4"
        if interval == 0 and quality == "major7sus2": return "Imaj7sus2"
        if interval == 5 and quality == "sus2": return "IVsus2"
        if interval == 7 and quality == "sus4": return "Vsus4"
        if interval == 7 and quality == "dominant7sus4": return "V7sus4"
        if interval == 7 and quality == "add11": return "Vadd11"
        if interval == 6 and quality == "diminished": return "vii^o/V"
        if interval == 11 and quality == "diminished": return "vii^o"
        return "Other"

    if mode == "mixolydian":
        if interval == 0 and quality == "major": return "I"
        if interval == 0 and quality == "major7": return "Imaj7"
        if interval == 2 and quality == "minor": return "ii"
        if interval == 3 and quality == "major": return "bIII"
        if interval == 3 and quality == "major7": return "bIIImaj7"
        if interval == 4 and quality == "minor": return "iii"
        if interval == 5 and quality == "major": return "IV"
        if interval == 5 and quality == "major7": return "IVmaj7"
        if interval == 7 and quality == "minor": return "v"
        if interval == 10 and quality == "major": return "VII"
        if interval == 10 and quality == "major7": return "VIImaj7"
        if interval == 0 and quality == "minor": return "i"
        if interval == 1 and quality == "major": return "bII"
        if interval == 2 and quality == "major": return "II"
        if interval == 5 and quality == "minor": return "iv"
        if interval == 6 and quality == "major": return "bV"
        if interval == 7 and quality == "major": return "V"
        if interval == 8 and quality == "major": return "bVI"
        if interval == 8 and quality == "major7": return "bVImaj7"
        if interval == 9 and quality == "minor": return "vi"
        if interval == 11 and quality == "major": return "bI"
        if interval == 0 and quality == "minor7": return "i7"
        if interval == 2 and quality == "minor7": return "ii7"
        if interval == 5 and quality == "minor7": return "iv7"
        if interval == 7 and quality == "minor7": return "v7"
        if interval == 9 and quality == "minor7": return "vi7"
        if interval == 0 and quality == "dominant7": return "I7"
        if interval == 2 and quality == "dominant7": return "II7"
        if interval == 5 and quality == "dominant7": return "IV7"
        if interval == 7 and quality == "dominant7": return "V7"
        if interval == 10 and quality == "dominant7": return "VII7"
        if interval == 10 and quality == "major9": return "VIImaj9"
        if interval == 0 and quality == "dominant9": return "I9"
        if interval == 0 and quality == "add9": return "Iadd9"
        if interval == 5 and quality == "add9": return "IVadd9"
        if interval == 10 and quality == "add9": return "VIIadd9"
        if interval == 0 and quality == "11": return "I11"
        if upper_interval == 10 and bass_interval == 0 and quality == "major": return "I^11"
        if upper_interval == 5 and bass_interval == 0 and quality == "major": return "IV^6_4"
        if upper_interval == 5 and bass_interval == 0 and quality == "minor": return "iv^6_4"
        if upper_interval == 9 and bass_interval == 0 and quality == "minor": return "vi^6"
        if upper_interval == 2 and bass_interval == 0 and quality == "minor": return "ii^4_2"
        if upper_interval == 7 and bass_interval == 2 and quality == "minor": return "v^6_4"
        if upper_interval == 10 and bass_interval == 2 and quality == "major": return "VII^6"
        if upper_interval == 0 and bass_interval == 4 and quality == "major": return "I^6"
        if upper_interval == 0 and bass_interval == 4 and quality == "dominant7": return "I^6_5"
        if upper_interval == 2 and bass_interval == 5 and quality == "minor": return "ii^6"
        if upper_interval == 10 and bass_interval == 5 and quality == "major": return "VII^6_4"
        if upper_interval == 0 and bass_interval == 7 and quality == "major": return "I^6_4"
        if upper_interval == 0 and bass_interval == 7 and quality == "dominant7": return "I^4_3"
        if upper_interval == 5 and bass_interval == 8 and quality == "minor": return "iv^6"
        if upper_interval == 5 and bass_interval == 9 and quality == "major": return "IV^6"
        if upper_interval == 0 and bass_interval == 10 and quality == "dominant7": return "I^4_2"
        if upper_interval == 7 and bass_interval == 10 and quality == "minor": return "v^6"
        if upper_interval == 3 and bass_interval == 10 and quality == "major": return "IV^6_4/VII"
        if interval == 0 and quality == "6": return "vi^6_5"
        if interval == 3 and quality == "6": return "i^6_5"
        if interval == 5 and quality == "6": return "ii^6_5"
        if interval == 10 and quality == "6": return "v^6_5"
        if interval == 0 and quality == "sus2": return "Isus2"
        if interval == 0 and quality == "sus4": return "Isus4"
        if interval == 0 and quality == "dominant7sus4": return "I7sus4"
        if upper_interval == 5 and bass_interval == 0 and quality == "sus4": return "IV^6_4sus4"
        if interval == 5 and quality == "sus2": return "IVsus2"
        if interval == 7 and quality == "sus4": return "vsus4"
        if interval == 7 and quality == "dominant7sus4": return "v7sus4"
        if interval == 10 and quality == "sus2": return "VIIsus2"
        if interval == 0 and quality == "add11": return "Iadd11"
        if interval == 2 and quality == "minor11": return "ii11"
        if interval == 7 and quality == "minor11": return "v11"
        if interval == 4 and quality == "diminished": return "iii^o"
        return "Other"
    
    if mode == "dorian":
        if interval == 0 and quality == "minor": return "i"
        if interval == 2 and quality == "minor": return "ii"
        if interval == 3 and quality == "major": return "III"
        if interval == 3 and quality == "major7": return "IIImaj7"
        if interval == 5 and quality == "major": return "IV"
        if interval == 7 and quality == "minor": return "v"
        if interval == 10 and quality == "major": return "VII"
        if interval == 10 and quality == "major7": return "VIImaj7"
        if interval == 0 and quality == "major": return "I"
        if interval == 1 and quality == "major": return "bII"
        if interval == 2 and quality == "major": return "II"
        if interval == 5 and quality == "minor": return "iv"
        if interval == 6 and quality == "major": return "bV"
        if interval == 7 and quality == "major": return "V"
        if interval == 8 and quality == "major": return "bVI"
        if interval == 8 and quality == "major7": return "bVImaj7"
        if interval == 9 and quality == "minor": return "vi"
        if interval == 0 and quality == "minor7": return "i7"
        if interval == 2 and quality == "minor7": return "ii7"
        if interval == 5 and quality == "minor7": return "iv7"
        if interval == 7 and quality == "minor7": return "v7"
        if interval == 0 and quality == "dominant7": return "I7"
        if interval == 2 and quality == "dominant7": return "II7"
        if interval == 5 and quality == "dominant7": return "IV7"
        if interval == 7 and quality == "dominant7": return "V7"
        if interval == 10 and quality == "dominant7": return "VII7"
        if interval == 3 and quality == "major9": return "IIImaj9"
        if interval == 10 and quality == "major9": return "VIImaj9"
        if interval == 0 and quality == "minor9": return "i9"
        if interval == 7 and quality == "minor9": return "v9"
        if interval == 5 and quality == "dominant9": return "IV9"
        if interval == 3 and quality == "add9": return "IIIadd9"
        if interval == 5 and quality == "add9": return "IVadd9"
        if interval == 10 and quality == "add9": return "VIIadd9"
        if interval == 0 and quality == "minoradd9": return "iadd9"
        if upper_interval == 5 and bass_interval == 0 and quality == "major": return "IV^6_4"
        if upper_interval == 2 and bass_interval == 0 and quality == "minor": return "ii^4_2"
        if upper_interval == 5 and bass_interval == 0 and quality == "dominant7": return "IV^4_3"
        if upper_interval == 10 and bass_interval == 2 and quality == "major": return "VII^6"
        if upper_interval == 7 and bass_interval == 2 and quality == "major": return "v^6_4"
        if upper_interval == 0 and bass_interval == 3 and quality == "minor": return "i^6"
        if upper_interval == 5 and bass_interval == 3 and quality == "dominant7": return "IV^4_2"
        if upper_interval == 2 and bass_interval == 5 and quality == "minor": return "ii^6"
        if upper_interval == 10 and bass_interval == 5 and quality == "major": return "VII^6_4"
        if upper_interval == 3 and bass_interval == 5 and quality == "major": return "IV^11"
        if interval == 5 and quality == "11": return "IV11"
        if upper_interval == 0 and bass_interval == 7 and quality == "minor": return "i^6_4"
        if upper_interval == 0 and bass_interval == 7 and quality == "minor7": return "i^4_3"
        if upper_interval == 3 and bass_interval == 7 and quality == "major": return "III^6"
        if upper_interval == 5 and bass_interval == 9 and quality == "major": return "IV^6"
        if upper_interval == 2 and bass_interval == 9 and quality == "minor": return "ii^6_4"
        if upper_interval == 7 and bass_interval == 10 and quality == "minor": return "v^6"
        if upper_interval == 3 and bass_interval == 10 and quality == "major": return "III^6_4"
        if upper_interval == 0 and bass_interval == 10 and quality == "minor": return "i^4_2"
        if interval == 0 and quality == "minor6": return "vi^o6_5"
        if interval == 3 and quality == "6": return "i^6_5"
        if interval == 5 and quality == "6": return "ii^6_5"
        if interval == 10 and quality == "6": return "v^6_5"
        if interval == 0 and quality == "sus2": return "isus2"
        if interval == 0 and quality == "sus4": return "isus4"
        if interval == 0 and quality == "dominant7sus2": return "i7sus2"
        if interval == 0 and quality == "dominant7sus4": return "i7sus4"
        if interval == 3 and quality == "sus2": return "IIIsus2"
        if interval == 5 and quality == "sus2": return "IVsus2"
        if interval == 5 and quality == "sus4": return "IVsus4"
        if interval == 5 and quality == "dominant7sus2": return "IV7sus2"
        if interval == 5 and quality == "dominant7sus4": return "IV7sus4"
        if interval == 7 and quality == "sus4": return "vsus4"
        if interval == 10 and quality == "sus2": return "VIIsus2"
        if interval == 10 and quality == "sus4": return "VIIsus4"
        if interval == 0 and quality == "minoradd11": return "iadd11"
        if interval == 0 and quality == "minor11": return "i11"
        if interval == 7 and quality == "minor11": return "v11"
        if interval == 9 and quality == "diminished": return "vi^o"
        if interval == 11 and quality == "diminished": return "vii^o/i"
        return "Other"
    
    if mode == "minor":
        if interval == 0 and quality == "minor": return "i"
        if interval == 3 and quality == "major": return "III"
        if interval == 3 and quality == "major7": return "IIImaj7"
        if interval == 5 and quality == "minor": return "iv"
        if interval == 7 and quality == "minor": return "v"
        if interval == 8 and quality == "major": return "VI"
        if interval == 8 and quality == "major7": return "VImaj7"
        if interval == 10 and quality == "major": return "VII"
        if interval == 0 and quality == "major": return "I"
        if interval == 2 and quality == "minor": return "ii"
        if interval == 5 and quality == "major": return "IV"
        if interval == 7 and quality == "major": return "V"
        if interval == 10 and quality == "minor": return "vii"
        if interval == 1 and quality == "major": return "bII"
        if interval == 1 and quality == "major7": return "bIImaj7"
        if interval == 6 and quality == "major": return "bV"
        if interval == 2 and quality == "major": return "II"
        if interval == 9 and quality == "minor": return "#vi"
        if interval == 0 and quality == "minor7": return "i7"
        if interval == 5 and quality == "minor7": return "iv7"
        if interval == 7 and quality == "minor7": return "v7"
        if interval == 10 and quality == "minor7": return "vii7"
        if interval == 0 and quality == "dominant7": return "I7"
        if interval == 2 and quality == "dominant7": return "II7"
        if interval == 5 and quality == "dominant7": return "IV7"
        if interval == 7 and quality == "dominant7": return "V7"
        if interval == 8 and quality == "dominant7": return "VI7"
        if interval == 10 and quality == "dominant7": return "VII7"
        if interval == 8 and quality == "major9": return "VImaj9"
        if interval == 0 and quality == "minor9": return "i9"
        if interval == 5 and quality == "minor9": return "iv9"
        if interval == 3 and quality == "add9": return "IIIadd9"
        if interval == 8 and quality == "add9": return "VIadd9"
        if interval == 10 and quality == "add9": return "VIIadd9"
        if interval == 0 and quality == "minoradd9": return "iadd9"
        if interval == 5 and quality == "minoradd9": return "ivadd9"
        if upper_interval == 8 and bass_interval == 0 and quality == "major": return "VI^6"
        if upper_interval == 5 and bass_interval == 0 and quality == "minor": return "iv^6_4"
        if upper_interval == 8 and bass_interval == 0 and quality == "major7": return "VI^6_5"
        if upper_interval == 10 and bass_interval == 2 and quality == "major": return "VII^6"
        if upper_interval == 7 and bass_interval == 2 and quality == "major": return "V^6_4"
        if upper_interval == 7 and bass_interval == 2 and quality == "minor": return "v^6_4"
        if upper_interval == 8 and bass_interval == 3 and quality == "major": return "VI^6_4"
        if upper_interval == 0 and bass_interval == 3 and quality == "minor": return "i^6"
        if upper_interval == 10 and bass_interval == 5 and quality == "major": return "VII^6_4"
        if upper_interval == 0 and bass_interval == 7 and quality == "minor": return "i^6_4"
        if upper_interval == 3 and bass_interval == 7 and quality == "major": return "III^6"
        if upper_interval == 8 and bass_interval == 7 and quality == "major": return "VI^4_2"
        if upper_interval == 10 and bass_interval == 8 and quality == "dominant7": return "VII^4_2"
        if upper_interval == 5 and bass_interval == 8 and quality == "minor": return "iv^6"
        if upper_interval == 5 and bass_interval == 9 and quality == "major": return "IV^6"
        if upper_interval == 0 and bass_interval == 10 and quality == "minor": return "i^4_2"
        if upper_interval == 7 and bass_interval == 10 and quality == "minor": return "v^6"
        if upper_interval == 3 and bass_interval == 10 and quality == "major": return "III^6_4"
        if upper_interval == 8 and bass_interval == 10 and quality == "major": return "VII^11"
        if interval == 10 and quality == "11": return "VII11"
        if upper_interval == 7 and bass_interval == 11 and quality == "major": return "V^6"
        if upper_interval == 7 and bass_interval == 11 and quality == "dominant7": return "V^6_5"
        if interval == 3 and quality == "6": return "i^6_5"
        if interval == 5 and quality == "minor6": return "ii^o6_5"
        if interval == 8 and quality == "6": return "iv^6_5"
        if interval == 10 and quality == "6": return "v^6_5"
        if interval == 0 and quality == "sus2": return "isus2"
        if interval == 0 and quality == "sus4": return "isus4"
        if interval == 0 and quality == "dominant7sus2": return "i7sus2"
        if interval == 5 and quality == "sus2": return "ivsus2"
        if interval == 5 and quality == "dominant7sus2": return "iv7sus2"
        if interval == 7 and quality == "sus4": return "vsus4"
        if interval == 7 and quality == "dominant7sus4": return "v7sus4"
        if interval == 8 and quality == "sus2": return "VIsus2"
        if interval == 10 and quality == "sus2": return "VIIsus2"
        if interval == 10 and quality == "sus4": return "VIIsus4"
        if interval == 0 and quality == "minor11": return "i11"
        if interval == 2 and quality == "diminished": return "ii^o"
        if interval == 11 and quality == "diminished": return "vii^o/i"
        return "Other"

    if mode == "phrygian":
        if interval == 0 and quality == "minor": return "i"
        if interval == 1 and quality == "major": return "II"
        if interval == 3 and quality == "major": return "III"
        if interval == 5 and quality == "minor": return "iv"
        if interval == 10 and quality == "minor": return "vii"
        if interval == 0 and quality == "major": return "I"
        if interval == 1 and quality == "minor": return "ii"
        if interval == 2 and quality == "minor": return "#ii"
        if interval == 3 and quality == "minor": return "iii"
        if interval == 4 and quality == "minor": return "#iii"
        if interval == 5 and quality == "major": return "IV"
        if interval == 6 and quality == "major": return "bV"
        if interval == 7 and quality == "minor": return "v"
        if interval == 7 and quality == "major": return "V"
        if interval == 8 and quality == "major": return "VI"
        if interval == 9 and quality == "major": return "V/#ii"
        if interval == 9 and quality == "minor": return "#vi"
        if interval == 10 and quality == "major": return "VII"
        if interval == 11 and quality == "major": return "V/#iii"
        if interval == 11 and quality == "minor": return "#vii"
        if upper_interval == 5 and bass_interval == 0 and quality == "minor": return "iv^6_4"
        if upper_interval == 1 and bass_interval == 0 and quality == "major": return "II^4_2"
        if upper_interval == 8 and bass_interval == 0 and quality == "major": return "VI^6"
        if upper_interval == 10 and bass_interval == 1 and quality == "minor": return "vii^6"
        if upper_interval == 3 and bass_interval == 1 and quality == "major": return "III^4_2"
        if upper_interval == 8 and bass_interval == 3 and quality == "major": return "VI^6_4"
        if upper_interval == 0 and bass_interval == 3 and quality == "minor": return "i^6"
        if upper_interval == 5 and bass_interval == 3 and quality == "minor": return "iv^4_2"
        if upper_interval == 1 and bass_interval == 5 and quality == "major": return "II^6"
        if upper_interval == 0 and bass_interval == 7 and quality == "minor": return "i^6_4"
        if upper_interval == 3 and bass_interval == 7 and quality == "major": return "III^6"
        if upper_interval == 1 and bass_interval == 8 and quality == "major": return "II^6_4"
        if upper_interval == 5 and bass_interval == 8 and quality == "minor": return "iv^6"
        if upper_interval == 0 and bass_interval == 10 and quality == "minor": return "i^4_2"
        if upper_interval == 3 and bass_interval == 10 and quality == "major": return "III^6_4"
        if upper_interval == 0 and bass_interval == 10 and quality == "minor7sus4": return "i^4_2sus4"
        if interval == 0 and quality == "minor7": return "i7"
        if interval == 0 and quality == "minorsus2": return "isus2"
        if interval == 0 and quality == "minorsus4": return "isus4"
        if interval == 0 and quality == "minor7sus4": return "i7sus4"
        if interval == 0 and quality == "minoradd11": return "iadd11"
        if interval == 1 and quality == "sus2": return "IIsus2"
        if interval == 1 and quality == "dominant7sus4": return "II7sus4"
        if interval == 1 and quality == "major7": return "IImaj7"
        if interval == 1 and quality == "major9": return "IImaj9"
        if interval == 1 and quality == "add9": return "IIadd9"
        if interval == 1 and quality == "6": return "vii^6_5"
        if interval == 3 and quality == "dominant7": return "III7"
        if interval == 3 and quality == "6": return "IIIadd6"
        if interval == 5 and quality == "minor7": return "iv7"
        if interval == 5 and quality == "minor9": return "iv9"
        if interval == 5 and quality == "minorsus2": return "ivsus2"
        if interval == 5 and quality == "minor7sus4": return "iv7sus4"
        if interval == 7 and quality == "dominant7": return "V7/i"
        if interval == 8 and quality == "major7": return "VImaj7"
        if interval == 10 and quality == "minor7": return "vii7"
        if interval == 10 and quality == "minorsus2": return "viisus2"
        if interval == 10 and quality == "minoradd9": return "viiadd9"
        if upper_interval == 7 and bass_interval == 1 and quality == "diminished": return "v^o6_4"
        if interval == 7 and quality == "diminished": return "v^o"
        return "Other"

    if mode == "locrian":
        if interval == 0 and quality == "minor": return "i"
        if interval == 0 and quality == "major": return "I"
        if interval == 0 and quality == "major7": return "Imaj7"
        if upper_interval == 1 and bass_interval == 0 and quality == "major": return "II^4_2"
        if interval == 1 and quality == "major": return "II"
        if interval == 2 and quality == "minor": return "#ii"
        if interval == 3 and quality == "major": return "V/VI"
        if interval == 3 and quality == "minor": return "iii"
        if interval == 3 and quality == "minor7": return "iii7"
        if interval == 4 and quality == "minor": return "#iii"
        if interval == 5 and quality == "major": return "V/vii"
        if interval == 5 and quality == "minor": return "iv"
        if interval == 6 and quality == "major": return "V"
        if upper_interval == 3 and bass_interval == 6 and quality == "major": return "iii^6"
        if interval == 8 and quality == "major": return "VI"
        if interval == 8 and quality == "dominant7": return "VI7"
        if interval == 10 and quality == "minor": return "vii"
        if interval == 0 and quality == "diminished": return "i^o"
        if interval == 2 and quality == "diminished": return "#ii^o"
        if upper_interval == 0 and bass_interval == 3 and quality == "diminished": return "i^o6"
        if upper_interval == 0 and bass_interval == 6 and quality == "diminished": return "i^o6_4"
        if interval == 6 and quality == "diminished": return "#iv^o"
        if interval == 10 and quality == "diminished": return "vii^o"
        if interval == 11 and quality == "diminished": return "vii^o/i"
        return "Other"

# Establish (uniform) prior probaiblity distribution of each key and mode
def build_priors():
    priors = {}
    for p in PITCHES:
        priors[f"{p} lydian"]    = 1/84
        priors[f"{p} major"]     = 1/84
        priors[f"{p} mixolydian"] = 1/84
        priors[f"{p} dorian"]    = 1/84
        priors[f"{p} minor"]     = 1/84
        priors[f"{p} phrygian"]  = 1/84
        priors[f"{p} locrian"]   = 1/84
    return priors

# Weights are such that a major triad built on the root is scored equally in lydian,
# major and mixolydian, a minor triad built on the root is scored equally in dorian,
# minor, phrygian and a diminished triad built on the root in locrian, and so that a major triad
# built on the root is scored equally in major compared to a minor triad built on the root in minor
# (ex: C gets the same score in C major as Am gets in A minor and as B diminished gets in B locrian)
def weights():
    weights = {}
    for p in PITCHES:
        weights["lydian"]    = 0.18/0.22
        weights["major"]     = 1.0
        weights["mixolydian"] = 0.18/0.26
        weights["dorian"]    = 0.18/0.19
        weights["minor"]     = 1.0
        weights["phrygian"]  = 0.18/0.27
        weights["locrian"]   = 0.18/0.28
    return weights

# Return a list containing all possible chords that the user could enter
def build_all_chords(include_bass=True, qualities=None):
    if qualities is None:
        qualities = QUALITIES
    basses = [None] + PITCHES if include_bass else [None]
    return [(root, q, b) for root in PITCHES for q in qualities for b in basses]

# Return a matrix of the liklihoods of all possible chords that the user could enter
def build_likelihood_matrix(all_chords, priors_keys):
    keys = list(priors_keys)
    K = len(keys)
    C = len(all_chords)
    LIK = np.zeros((K, C), dtype=float)

    probs_map = {
        "lydian": LYDIAN_PROBS,
        "major": MAJOR_PROBS,
        "mixolydian": MIXOLYDIAN_PROBS,
        "dorian": DORIAN_PROBS,
        "minor": MINOR_PROBS,
        "phrygian": PHRYGIAN_PROBS,
        "locrian": LOCRIAN_PROBS
    }

    MODE_WEIGHTS = {
        "lydian": (0.18/0.22),
        "major": 1.0,
        "mixolydian": (0.18/0.26),
        "dorian": (0.18/0.19),
        "minor": 1.0,
        "phrygian": (0.18/0.27),
        "locrian": (0.18/0.28)
    }

    for ki, key in enumerate(keys):
        tonic, mode = key.split()
        table = probs_map[mode]
        weight = MODE_WEIGHTS[mode]

        for ci, (root, quality, bass) in enumerate(all_chords):

            if bass is None:
                iv = interval(tonic, root)
                upper_interval = None
                bass_interval = None
            else:
                iv = None
                upper_interval = interval(tonic, root)
                bass_interval = interval(tonic, bass)

            deg = degree_name(iv, upper_interval, bass_interval, quality, mode)

            # Apply mode weight directly to likelihood
            LIK[ki, ci] = table.get(deg, table.get("Other", 1e-30)) * weight
    return keys, LIK

# Compute the posterior probability of all possible chord progressions of length n that the user
# could enter
def compute_posterior_for_combo(combo_indices, logPRIORS, logLIK):
    log_sum = logPRIORS.copy()
    for idx in combo_indices:
        log_sum = log_sum + logLIK[:, idx]
    maxv = np.max(log_sum)
    probs = np.exp(log_sum - maxv)
    probs = probs / probs.sum()
    return probs

# To obtain nontrivial chord progressions, require that every progression's chords must have roots
# distinct from those within its progression (ex: G - C - D is valid, but G - C - G is not)
def chord_pitches(ch):
    root, _, bass = ch
    return {root} if bass is None else {root, bass}

def combo_has_unique_pitches(combo_indices, all_chords):
    total = 0
    union = set()
    for i in combo_indices:
        p = chord_pitches(all_chords[i])
        total += len(p)
        union |= p
    return len(union) == total


# Grid search to compute the best chord progression of length n that maximizes the product of
# posterior probabilities for two target keys (ex: C major and A minor)
def grid_search_best_n(all_chords, priors, LIK, n=4, target_keys=("C major","A minor")):
    """
    all_chords: list of (root, quality, bass)
    priors: dict mapping "Tonic mode" -> prior
    LIK: (K, C) likelihood matrix
    n: number of chords in progression
    target_keys: tuple of two keys whose posterior product we maximize
    """
    keys = list(priors.keys())
    logPRIORS = np.log(np.array([priors[k] for k in keys], dtype=float))
    # floor LIK to avoid log(0)
    eps = 1e-300
    logLIK = np.log(LIK + eps)

    # indices of target keys
    try:
        Cmaj_idx = keys.index(target_keys[0])
        Amin_idx = keys.index(target_keys[1])
    except ValueError:
        raise ValueError("Target keys not found in priors keys")

    best_val = -np.inf
    best_combo = None

    count = 0
    # iterate combinations (order doesn't matter)
    for combo in combinations(range(len(all_chords)), n):
        # enforce unique pitch classes across the chords (roots and basses)
        if not combo_has_unique_pitches(combo, all_chords):
            continue

        probs = compute_posterior_for_combo(combo, logPRIORS, logLIK)
        val = probs[Cmaj_idx] * probs[Amin_idx]

        if val > best_val:
            best_val = val
            best_combo = combo
            # print progress (optional)
            print("New best:", best_combo, best_val)
            best_chords = tuple(all_chords[i] for i in best_combo)
            print("Best chords:", best_chords)
        count += 1
        if count % 100000 == 0:
            print(count)

    if best_combo is None:
        return None, None
    return tuple(all_chords[i] for i in best_combo), best_val

# -------------------------------------------------------------------------------------------------
# Plotting utilities
# -------------------------------------------------------------------------------------------------

# Assign each parent major key a unique color for plotting purposes. The colors are chosen to be
# visually distinct and are based on a color wheel approach.
def build_parent_color_map():
    # base red hex (C major and its relatives)
    base_red_hex = "#FF0000"
    def hex_to_rgb01(hx: str):
        hx = hx.lstrip("#")
        r = int(hx[0:2], 16) / 255.0
        g = int(hx[2:4], 16) / 255.0
        b = int(hx[4:6], 16) / 255.0
        return (r, g, b)
    def rgb01_to_hex(rgb):
        r, g, b = rgb
        return "#{:02x}{:02x}{:02x}".format(int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))

    base_rgb = hex_to_rgb01(base_red_hex)
    base_h, base_s, base_v = colorsys.rgb_to_hsv(*base_rgb)
    step = 1.0 / 12.0
    cof = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F"]
    parent_color = {}
    for i, tonic in enumerate(cof):
        hue = (base_h + step * i) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, base_s, base_v)
        parent_color[tonic] = rgb01_to_hex(rgb)
    default_color = "#888888"
    return parent_color, default_color, cof

# Helper function to determine the parent major key of a given "Tonic mode" label. This is useful
# for grouping modes under their corresponding major keys for analysis and visualization.
def parent_major_of(label):
    """
    label: "Tonic mode" e.g., "C major"
    returns parent major tonic name (standard chromatic)
    """
    standard_chromatic = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    mode_to_degree = {
        "major": 1,
        "dorian": 2,
        "phrygian": 3,
        "lydian": 4,
        "mixolydian": 5,
        "minor": 6,
        "locrian": 7,
    }
    degree_intervals = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
    parts = label.split()
    if len(parts) < 2:
        return None
    tonic = parts[0]
    mode = parts[1]
    mode_key = "minor" if mode == "minor" else mode
    if tonic not in standard_chromatic or mode_key not in mode_to_degree:
        return None
    degree = mode_to_degree[mode_key]
    semitone_offset = degree_intervals[degree]
    standard_index = {t: i for i, t in enumerate(standard_chromatic)}
    parent_idx = (standard_index[tonic] - semitone_offset) % 12
    return standard_chromatic[parent_idx]

def plot_results(adjusted_scores):
    """
    adjusted_scores: dict mapping "Tonic mode" -> probability
    Produces four plots: per-mode probabilities, parent-major histogram,
    negative log-loss per-mode, negative log-loss parent-major.
    """
    labels = list(adjusted_scores.keys())
    values = [adjusted_scores[k] for k in labels]

    # Sort indices by value descending
    order = sorted(range(len(values)), key=lambda i: values[i], reverse=True)
    labels = [labels[i] for i in order]
    values = [values[i] for i in order]

    parent_color, default_color, cof = build_parent_color_map()

    # Map colors in the same sorted order
    per_mode_colors = []
    for lab in labels:
        parent = parent_major_of(lab)
        per_mode_colors.append(parent_color.get(parent, default_color))

    # Sum by parent major
    standard_chromatic = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    parent_sums = {t: 0.0 for t in standard_chromatic}
    for label, p in adjusted_scores.items():
        parent = parent_major_of(label)
        if parent is None:
            continue
        parent_sums[parent] += p
    parent_items = sorted(parent_sums.items(), key=lambda x: x[1], reverse=True)
    parent_labels = [f"{t} major field" for t, _ in parent_items]
    parent_values = [v for _, v in parent_items]
    parent_colors = [parent_color.get(t, default_color) for t, _ in parent_items]

    # Negative log values
    import math
    neglog_values = [(-math.log(v) if v > 0 else 0.0) for v in values]
    neglog_parent_values = [(-math.log(v) if v > 0 else 0.0) for v in parent_values]

    # Plot 1: per-mode probabilities
    fig1, ax1 = plt.subplots(figsize=(max(10, len(labels) * 0.35), 6))
    ax1.bar(range(len(labels)), values, color=per_mode_colors)
    ax1.set_ylim(0, 1)
    ax1.set_ylabel("Probability")
    ax1.set_xlabel("Key and Scale")
    ax1.set_xticks(range(len(labels)))
    ax1.set_xticklabels(labels, rotation=90, fontsize=7)
    ax1.set_yticks([i / 10 for i in range(0, 11)])
    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    from matplotlib.patches import Patch
    legend_patches = [Patch(color=parent_color[t], label=t) for t in cof]
    ax1.legend(handles=legend_patches, title="Parent Major (CoF order)", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8, title_fontsize=9)
    plt.tight_layout()

    # Plot 2: parent-major histogram
    # Visualize the distribution of probabilities across parent-major keys.
    fig2, ax2 = plt.subplots(figsize=(max(8, len(parent_labels) * 0.6), 5))
    ax2.bar(range(len(parent_labels)), parent_values, color=parent_colors)
    ax2.set_ylim(0, 1)
    ax2.set_ylabel("Fraction of the progression's color")
    ax2.set_xlabel("Major Field")
    ax2.set_xticks(range(len(parent_labels)))
    ax2.set_xticklabels(parent_labels, rotation=90, fontsize=8)
    ax2.set_yticks([i / 10 for i in range(0, 11)])
    ax2.grid(axis="y", linestyle="--", alpha=0.3)
    legend_patches2 = [Patch(color=parent_color[t], label=f"{t} major") for t in cof]
    ax2.legend(handles=legend_patches2, title="Parent Major (CoF order)", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8, title_fontsize=9)
    plt.tight_layout()

    # Plot 3: negative log-loss per-mode
    fig3, ax3 = plt.subplots(figsize=(max(10, len(labels) * 0.35), 6))
    ax3.bar(range(len(labels)), neglog_values, color=per_mode_colors)
    ax3.set_ylabel("Negative Log Loss")
    ax3.set_xlabel("Key and Scale")
    ax3.set_xticks(range(len(labels)))
    ax3.set_xticklabels(labels, rotation=90, fontsize=7)
    ax3.grid(axis="y", linestyle="--", alpha=0.3)
    legend_patches3 = [Patch(color=parent_color[t], label=t) for t in cof]
    ax3.legend(handles=legend_patches3, title="Parent Major (CoF order)", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8, title_fontsize=9)
    plt.tight_layout()

    # Plot 4: negative log-loss parent-major
    fig4, ax4 = plt.subplots(figsize=(max(8, len(parent_labels) * 0.6), 5))
    ax4.bar(range(len(parent_labels)), neglog_parent_values, color=parent_colors)
    ax4.set_ylabel("Negative Log Loss")
    ax4.set_xlabel("Major Field")
    ax4.set_xticks(range(len(parent_labels)))
    ax4.set_xticklabels(parent_labels, rotation=90, fontsize=8)
    ax4.grid(axis="y", linestyle="--", alpha=0.3)
    legend_patches4 = [Patch(color=parent_color[t], label=f"{t} major") for t in cof]
    ax4.legend(handles=legend_patches4, title="Parent Major (CoF order)", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8, title_fontsize=9)
    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------------------------------------------
# Interactive scoring of chord progressions by key and mode probabilities
# -------------------------------------------------------------------------------------------------

# The user can input chords one at a time, and the program will compute and display the posterior
# probabilities of each key and mode based on the entered chords. The user can also visualize the
# results through plots.
def interactive_main():
    priors = build_priors()
    all_chords = build_all_chords(include_bass=True)
    keys, LIK = build_likelihood_matrix(all_chords, priors.keys())

    print("Enter chords like C, Fm, G#, D#m, or slash chords like Gsus2/E. Type 'end' to finish.\n")
    chord_history = []

    while True:
        user = input("Chord: ").strip()
        if user.lower() == "end":
            break

        root, quality, bass = parse_full_chord(user)
        print("Root:", root, "Quality:", quality, "Bass:", bass)

        # Validate
        if root not in PITCHES:
            print("Invalid root.")
            continue
        if quality not in QUALITIES:
            print("Invalid quality.")
            continue
        if bass is not None and bass not in PITCHES:
            print("Invalid bass note.")
            continue

        chord_history.append((root, quality, bass))

        # Compute posterior for current history
        # Build a temporary ALL_CHORDS-like mapping for the history chords
        # We need to find indices in the global all_chords list that match the history chords
        # For simplicity, compute posterior by summing logLIK columns for matching chords
        # Build mapping from chord tuple to index
        chord_to_index = {ch: i for i, ch in enumerate(all_chords)}
        indices = []
        for ch in chord_history:
            if ch not in chord_to_index:
                print("Chord not in ALL_CHORDS (unexpected).")
                continue
            indices.append(chord_to_index[ch])

        # Compute posterior
        logPRIORS = np.log(np.array([priors[k] for k in keys], dtype=float))
        logLIK = np.log(LIK + 1e-300)
        probs = compute_posterior_for_combo(indices, logPRIORS, logLIK)

        # Normalize and build adjusted_scores dict
        adjusted_scores = {k: float(probs[i]) for i, k in enumerate(keys)}

        # Print probabilities
        items = sorted(adjusted_scores.items(), key=lambda x: x[1], reverse=True)
        print("\nProbabilities:")
        for k, v in items:
            print(f"{k}: {v:.6f}")
        print()

        # Plot results
        # plot_results(adjusted_scores)

    # After loop, print final best key
    if chord_history:
        chord_to_index = {ch: i for i, ch in enumerate(all_chords)}
        indices = [chord_to_index[ch] for ch in chord_history if ch in chord_to_index]
        logPRIORS = np.log(np.array([priors[k] for k in keys], dtype=float))
        logLIK = np.log(LIK + 1e-300)
        probs = compute_posterior_for_combo(indices, logPRIORS, logLIK)
        adjusted_scores = {k: float(probs[i]) for i, k in enumerate(keys)}
        best_key = max(adjusted_scores, key=adjusted_scores.get)
        print("\nFinal best key:", best_key)
        print("Probability:", adjusted_scores[best_key])
    
    # Plot results
    plot_results(adjusted_scores)

# -------------------------------------------------------------------------------------------------
# Grid search for best chord progressions to maximize indifference to two keys
# -------------------------------------------------------------------------------------------------

# Run grid search and print best combination that maximizes the product of the scores of two keys
# and modes
def best_chords_main():
    # Build priors and chords
    priors = build_priors()
    # include_bass=True to allow slash chords; set False to restrict to root-only chords
    all_chords = build_all_chords(include_bass=False)
    keys, LIK = build_likelihood_matrix(all_chords, priors.keys())

    # Run grid search for n-chord progressions
    best_chords, best_val = grid_search_best_n(all_chords, priors, LIK, n=2, target_keys=("C major",
        "D dorian"))
    print("\n=== GRID SEARCH RESULT ===")
    print("Best chord progression (root, quality, bass):")
    print(best_chords)
    print("Best objective value:", best_val)

if __name__ == "__main__":
    # interactive_main() to input a chord progression and return mode and key probabilities.
    # best_chords_main() to find best chords to maximize indifference to the chord progression being
    # in two specified keys.
    # interactive_main()
    interactive_main()