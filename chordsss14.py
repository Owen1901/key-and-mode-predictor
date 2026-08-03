from statistics import mode
import matplotlib.pyplot as plt
import colorsys

PITCHES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
QUALITIES = ["major", "minor", "dominant7", "major7", "minor7", "dominant9", "major9", "minor9", "add9", "madd9"]
pitch_to_index = {p:i for i,p in enumerate(PITCHES)}

LYDIAN_PROBS = {
    "I": 0.22, "Imaj7": 0.06, "II": 0.11, "iii": 0.05, "V": 0.07, "vi": 0.03, "vii": 0.03,

    # Non-diatonic chords
    "i": 0.004, "bII": 0.003, "bIII": 0.007, "III": 0.01, "bIV": 0.01, "IV": 0.005,
    "bVI": 0.007, "bVII": 0.003,

    "Vmaj7": 0.01, "bVImaj7": 0.002,

    "iii7": 0.01, "vi7": 0.01, "vii7": 0.02,

    "I7": 0.003, "II7": 0.009, "V7": 0.003, 

    "Imaj9": 0.02,

    "iii9": 0.004,

    "II9": 0.003,

    "Iadd9": 0.01, "IIadd9": 0.006,

    "iiiadd9": 0.003,

    "Other": 0.00
}

MAJOR_PROBS = {
    "I": 0.18, "Imaj7": 0.02, "ii": 0.03, "iii": 0.03, "IV": 0.12, "IVmaj7": 0.02, "V": 0.12,
    "vi": 0.07,

    # Non-diatonic chords
    "iv": 0.006, "v": 0.001,
    
    "II": 0.007, "bIII": 0.004, "III": 0.007, "VI": 0.004,
    "bVI": 0.005, "bVImaj7": 0.002, "bVII": 0.01, "bVIImaj7": 0.001, "VII": 0.001,

    "ii7": 0.03, "iii7": 0.02, "iv7": 0.001, "v7": 0.002, "vi7": 0.02,

    "I7": 0.005, "II7": 0.005, "III7": 0.006,
    "IV7": 0.001, "V7": 0.002, "VI7": 0.004, 

    "Imaj9": 0.003, "IVmaj9": 0.003, 

    "ii9": 0.003, "vi9": 0.001,

    "V9": 0.001,

    "Iadd9": 0.005, "IVadd9": 0.007, "Vadd9": 0.002,

    "IV^6_4": 0.007, "vi^6": 0.003, "ii^4_2": 0.002,
    
    "V^6_4": 0.004, "V^4_3": 0.002,

    "I^6": 0.02, "vi^6_4": 0.002, "I^6_5": 0.001,

    "V^4_2": 0.003, "ii^6": 0.002,

    "V^6/V": 0.001,

    "vi^4_2": 0.003, "iii^6_5": 0.003, "I^6_4": 0.01, "V^11": 0.005,

    "V^6/vi": 0.001, "V^6_5/vi": 0.001, "iv^6": 0.001,

    "ii^6_4": 0.001, "IV^6": 0.005,

    "V^6": 0.01, "V^6_5": 0.001, "iii^6_4": 0.003, "I^4_2": 0.003,

    "Other": 0.00
}

MIXOLYDIAN_PROBS = {
    "I": 0.26, "ii": 0.02, "bIII": 0.03, "IV": 0.11, "v": 0.03, "VII": 0.14,

    # Borrowed / chromatic
    "i": 0.002, "bII": 0.003, "II": 0.005, "iii": 0.001, "iv": 0.005,
    "bV": 0.002, "V": 0.02, "bVI": 0.02, "vi": 0.02, "bI": 0.001,

    "Imaj7": 0.002, "bIIImaj7": 0.003, "IVmaj7": 0.006, "bVImaj7": 0.004, "VIImaj7": 0.006,

    "i7": 0.002, "ii7": 0.007, "iv7": 0.001, "v7": 0.01, "vi7": 0.008,

    "I7": 0.03, "II7": 0.002, "IV7": 0.006, "V7": 0.004, "VII7": 0.002,

    "VIImaj9": 0.002,

    "I9": 0.003,

    "Iadd9": 0.006, "IVadd9": 0.004, "VIIadd9": 0.009,

    "I^11": 0.01,

    "IV^6_4": 0.01, "iv^6_4": 0.002, "vi^6": 0.002, "ii^4_2": 0.003,

    "v^6_4": 0.001, "VII^6": 0.004,

    "I^6": 0.01, "I^6_5": 0.001,

    "ii^6": 0.002, "VII^6_4": 0.007,

    "I^6_4": 0.02, "I^4_3": 0.002,

    "iv^6": 0.002,
    
    "IV^6": 0.01,

    "I^4_2": 0.01, "v^6": 0.002, "IV^6_4/VII": 0.002,

    "Other": 0.00
}

DORIAN_PROBS = {
    "i": 0.19, "ii": 0.02, "III": 0.09, "IIImaj7": 0.009, "IV": 0.12,
    "v": 0.04, "VII": 0.08, "VIImaj7": 0.005,

    # Borrowed / chromatic
    "I": 0.02, "bII": 0.003, "II": 0.004, "iv": 0.002,
    "bV": 0.003, "V": 0.01, "bVI": 0.02, "bVImaj7": 0.005, "vi": 0.001,

    "i7": 0.06, "ii7": 0.01, "iv7": 0.001, "v7": 0.01,

    "I7": 0.003, "II7": 0.001, "IV7": 0.02, "V7": 0.005, "VII7": 0.001,

    "IIImaj9": 0.001, "VIImaj9": 0.001,

    "i9": 0.01, "v9": 0.002,

    "IV9": 0.004,

    "IIIadd9": 0.002, "IVadd9": 0.004, "VIIadd9": 0.004, 

    "iadd9": 0.004, 

    "Other": 0.00
}

MINOR_PROBS = {
    "i": 0.18, "III": 0.06, "IIImaj7": 0.005, "iv": 0.05, "v": 0.04,
    "VI": 0.10, "VImaj7": 0.03, "VII": 0.10,

    # Non-diatonic chords
    "I": 0.01, "ii": 0.002, "IV": 0.01, "V": 0.03, "vii": 0.001,

    "bII": 0.005, "bIImaj7": 0.002, "II": 0.002, "bV": 0.002, "#vi": 0.001,

    "i7": 0.03, "iv7": 0.02, "v7": 0.02, "vii7": 0.002,

    "I7": 0.002, "II7": 0.001, "IV7": 0.002, "V7": 0.01, "VI7": 0.001, "VII7": 0.005,

    "VImaj9": 0.003, 

    "i9": 0.005, "iv9": 0.004,

    "IIIadd9": 0.001, "VIadd9": 0.004, "VIIadd9": 0.003,

    "iadd9": 0.004, "ivadd9": 0.001,

    "VI^6": 0.004, "iv^6_4": 0.003, "VI^6_5": 0.002,

    "VII^6": 0.007, "V^6_4": 0.002, "v^6_4": 0.003,

    "VI^6_4": 0.003, "i^6": 0.01,

    "VII^6_4": 0.003,

    "i^6_4": 0.01, "III^6": 0.006, "VI^4_2": 0.001,

    "VII^4_2": 0.002, "iv^6": 0.004,

    "IV^6": 0.003,

    "i^4_2": 0.005, "v^6": 0.005, "III^6_4": 0.006, "VII^11": 0.001,

    "V^6": 0.006, "V^6_5": 0.002,
    
    "Other": 0.00
}

def parse_chord(ch):
    ch = ch.strip()
    
    # longest suffixes first
    if ch.endswith("maj7"):
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
        return ch[:-5], "madd9"
    elif ch.endswith("add9"):
        return ch[:-4], "add9"
    elif ch.endswith("9"):
        return ch[:-1], "dominant9"
    if ch.endswith("m"):
        return ch[:-1], "minor"
    else:
        return ch, "major"
    
def parse_full_chord(ch):
    """
    Generalized parser that supports slash chords like Dm/C or C/E.
    Returns (root, quality, bass).
    """

    ch = ch.strip()

    # 1. Detect slash chords
    if "/" in ch:
        upper, bass = ch.split("/", 1)
        upper = upper.strip()
        bass = bass.strip()
    else:
        upper, bass = ch, None

    # 2. Parse the upper chord using your existing logic
    root, quality = parse_chord(upper)

    return root, quality, bass

def interval(a, b):
    return (pitch_to_index[b] - pitch_to_index[a]) % 12

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

        # Non-diatonic chords
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
        if interval == 4 and quality == "madd9": return "iiiadd9"
        return "Other"
    
    # Major mode degrees
    if mode == "major":
        if interval == 0 and quality == "major": return "I"
        if interval == 0 and quality == "major7": return "Imaj7"
        if interval == 2 and quality == "minor": return "ii"
        if interval == 4 and quality == "minor": return "iii"
        if interval == 5 and quality == "major": return "IV"
        if interval == 5 and quality == "major7": return "IVmaj7"
        if interval == 7 and quality == "major": return "V"
        if interval == 9 and quality == "minor": return "vi"

        # Non-diatonic chords
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

        if interval == 0 and quality == "dominant7": return "I"
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

        if upper_interval == 2 and bass_interval == 9 and quality == "minor": return "ii^6_4"
        if upper_interval == 5 and bass_interval == 9 and quality == "major": return "IV^6"

        if upper_interval == 4 and bass_interval == 10 and quality == "major": return "V^6/vi"
        if upper_interval == 4 and bass_interval == 10 and quality == "dominant7": return "V^6_5/vi"
        if upper_interval == 5 and bass_interval == 10 and quality == "minor": return "iv^6"

        if upper_interval == 7 and bass_interval == 11 and quality == "major": return "V^6"
        if upper_interval == 4 and bass_interval == 11 and quality == "minor": return "iii^6_4"
        if upper_interval == 0 and bass_interval == 11 and quality == "major": return "I^4_2"
        if upper_interval == 7 and bass_interval == 11 and quality == "dominant7": return "V^6_5"
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

        # Non-diatonic chords
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

        if interval == 0 and quality == "major11": return "I^11"

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

        # Non-diatonic chords
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
        if interval == 0 and quality == "madd9": return "iadd9"
        return "Other"

    # Minor mode degrees
    if mode == "minor":
        if interval == 0 and quality == "minor": return "i"
        if interval == 3 and quality == "major": return "III"
        if interval == 3 and quality == "major7": return "IIImaj7"
        if interval == 5 and quality == "minor": return "iv"
        if interval == 7 and quality == "minor": return "v"
        if interval == 8 and quality == "major": return "VI"
        if interval == 8 and quality == "major7": return "VImaj7"
        if interval == 10 and quality == "major": return "VII"

        # Non-diatonic chords
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

        if interval == 0 and quality == "madd9": return "iadd9"
        if interval == 5 and quality == "madd9": return "ivadd9"

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

        if upper_interval == 7 and bass_interval == 11 and quality == "major": return "V^6"
        if upper_interval == 7 and bass_interval == 11 and quality == "dominant7": return "V^6_5"
        return "Other"

def main():
    # Initialize scores
    scores = {}
    for p in PITCHES:
        scores[p + " lydian"] = 1.0
        scores[p + " major"] = 1.0
        scores[p + " mixolydian"] = 1.0
        scores[p + " dorian"] = 1.0
        scores[p + " minor"] = 1.0

    print("Enter chords like C, Fm, G#, D#m. Type 'end' to finish.\n")

    while True:
        user = input("Chord: ").strip()
        if user.lower() == "end":
            break

        root, quality, bass = parse_full_chord(user)

        print("Root:", root)
        print("Quality:", quality)
        print("Bass:", bass)

        # Validate chord
        if root not in PITCHES:
            print("Invalid root.")
            continue

        if quality not in QUALITIES:
            print("Invalid quality.")
            continue

        if bass is not None and bass not in PITCHES:
            print("Invalid bass note.")
            continue

        for key in scores:
            tonic, mode = key.split()
            if bass == None:
                iv = interval(tonic, root)
                upper_interval = None
                bass_interval = None
            else:
                iv = None  
                upper_interval = interval(tonic, root)
                bass_interval = interval(tonic, bass)

            deg = degree_name(iv, upper_interval, bass_interval, quality, mode)

            if mode == "lydian":
                prob = LYDIAN_PROBS.get(deg, LYDIAN_PROBS["Other"])
            elif mode == "major":
                prob = MAJOR_PROBS.get(deg, MAJOR_PROBS["Other"])
            elif mode == "mixolydian":
                prob = MIXOLYDIAN_PROBS.get(deg, MIXOLYDIAN_PROBS["Other"])
            elif mode == "dorian":
                prob = DORIAN_PROBS.get(deg, DORIAN_PROBS["Other"])
            elif mode == "minor":
                prob = MINOR_PROBS.get(deg, MINOR_PROBS["Other"])
            
            scores[key] *= prob

        # Print normalized probabilities

                # -------------------------
        # Per-mode sorted bar chart (12 * 5 bars)
        # -------------------------
        total = sum(scores.values())
        probs = {k: scores[k] / total for k in scores}

        # Sort from highest to lowest probability
        items = sorted(probs.items(), key=lambda x: x[1], reverse=True)
        labels = [k for k, _ in items]
        values = [v for _, v in items]

        # Chromatic tonics in order starting at C (12 steps)
        chromatic = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        chromatic_index = {t: i for i, t in enumerate(chromatic)}

        # Degree -> semitone offset in a major scale (degree 1..7)
        degree_intervals = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
        mode_to_degree = {
            "major": 1,
            "dorian": 2,
            "phrygian": 3,
            "lydian": 4,
            "mixolydian": 5,
            "minor": 6,   # aeolian
            "locrian": 7,
        }

        # Base red hex (C major and its relatives)
        base_red_hex = "#FF0000"

        # Helper: convert hex to RGB (0..1), and back from HSV to hex
        def hex_to_rgb01(hx: str):
            hx = hx.lstrip("#")
            r = int(hx[0:2], 16) / 255.0
            g = int(hx[2:4], 16) / 255.0
            b = int(hx[4:6], 16) / 255.0
            return (r, g, b)

        def rgb01_to_hex(rgb):
            r, g, b = rgb
            return "#{:02x}{:02x}{:02x}".format(int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))

        # Determine base hue from the provided base red hex
        base_rgb = hex_to_rgb01(base_red_hex)
        base_h, base_s, base_v = colorsys.rgb_to_hsv(*base_rgb)

        # Step around the color wheel: 1/12 of full circle per semitone
        step = 1.0 / 12.0

        # Precompute parent-major -> hex color mapping (same color for all modes that belong to that major)
        parent_color = {}
        for i, tonic in enumerate(chromatic):
            hue = (base_h + step * i) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, base_s, base_v)
            parent_color[tonic] = rgb01_to_hex(rgb)

        # Function to compute the parent major tonic for a given "Tonic mode" label
        def parent_major_of(label):
            # label format: "Tonic mode" e.g., "C major" or "C# minor"
            parts = label.split()
            if len(parts) < 2:
                return None
            tonic = parts[0]
            mode = parts[1]
            # Normalize synonyms
            mode_key = "minor" if mode == "minor" else mode
            if tonic not in chromatic or mode_key not in mode_to_degree:
                return None
            degree = mode_to_degree[mode_key]
            semitone_offset = degree_intervals[degree]
            parent_idx = (chromatic_index[tonic] - semitone_offset) % 12
            return chromatic[parent_idx]

        # Map each label to the parent-major color for the per-mode plot
        colors = []
        for lab in labels:
            parent = parent_major_of(lab)
            colors.append(parent_color.get(parent, "#888888"))

        # Create figure sized to number of bars (per-mode)
        fig, ax = plt.subplots(figsize=(max(10, len(labels) * 0.35), 6))

        # Vertical bars ordered by probability
        ax.bar(range(len(labels)), values, color=colors)

        # Axes and formatting
        ax.set_ylim(0, 1)
        ax.set_ylabel("Probability")
        ax.set_xlabel("Key and Scale")
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=90, fontsize=7)
        ax.set_yticks([i / 10 for i in range(0, 11)])
        ax.grid(axis="y", linestyle="--", alpha=0.3)

        # Compact legend: one entry per parent major (12 tonics)
        from matplotlib.patches import Patch
        legend_patches = [Patch(color=parent_color[t], label=t) for t in chromatic]
        ax.legend(handles=legend_patches, title="Parent Major", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8, title_fontsize=9)

        plt.tight_layout()
        #plt.show()

        # Also print the numeric probabilities to the console for reference
        print("\nProbabilities:")
        for k, v in items:
            print(f"{k}: {v:.4f}")
        print()

        # -------------------------
        # Second plot: summed "major field" histogram (12 bars)
        # -------------------------
        # Sum probabilities by parent major (reuse probs and parent_major_of)
        parent_sums = {t: 0.0 for t in chromatic}
        for label, p in probs.items():
            parent = parent_major_of(label)
            if parent is None:
                continue
            parent_sums[parent] += p

        # Prepare sorted data (highest -> lowest)
        parent_items = sorted(parent_sums.items(), key=lambda x: x[1], reverse=True)
        parent_labels = [f"{t} major field" for t, _ in parent_items]
        parent_values = [v for _, v in parent_items]
        parent_colors = [parent_color[t] for t, _ in parent_items]

        # Plot the 12-bar parent-major histogram
        fig2, ax2 = plt.subplots(figsize=(max(8, len(parent_labels) * 0.6), 5))
        ax2.bar(range(len(parent_labels)), parent_values, color=parent_colors)
        ax2.set_ylim(0, 1)
        ax2.set_ylabel("Fraction of the progression's color")
        ax2.set_xlabel("Major Field")
        ax2.set_xticks(range(len(parent_labels)))
        ax2.set_xticklabels(parent_labels, rotation=90, fontsize=8)
        ax2.set_yticks([i / 10 for i in range(0, 11)])
        ax2.grid(axis="y", linestyle="--", alpha=0.3)

        # Optional compact legend (one patch per tonic)
        legend_patches2 = [Patch(color=parent_color[t], label=f"{t} major") for t in chromatic]
        ax2.legend(handles=legend_patches2, title="Parent Major", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8, title_fontsize=9)

        plt.tight_layout()
        plt.show()


        # Also print the numeric probabilities to the console for reference
        #print("\nProbabilities:")
        #for k, v in items:
        #    print(f"{k}: {v:.4f}")
        #print()

    # Final result
    total = sum(scores.values())
    final_probs = {k: scores[k]/total for k in scores}
    best = max(final_probs, key=final_probs.get)

    print("\nMost likely key:", best)
    print("Probability:", final_probs[best])

if __name__ == "__main__":
    main()