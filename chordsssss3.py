from statistics import mode
import matplotlib.pyplot as plt
import colorsys

PITCHES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
#QUALITIES = ["major", "minor", "6", "minor6", "dominant7", "major7", "minor7", "dominant9",
             #"major9", "minor9", "add9", "minoradd9", "11", "minor11", "add11", "minoradd11", "sus2", "major7sus2", "minor7sus2", "dominant7sus2",
             #"sus4", "major7sus4", "minor7sus4", "dominant7sus4"]
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

    "II^4_2": 0.02,

    "V^6_4": 0.004, "vii^6": 0.004,

    "VII^6": 0.002,

    "I^6": 0.01,

    "VII^6_4": 0.002, "vii^6_4": 0.002, "II^6": 0.007, "II^6_5": 0.003,

    "I^6_4": 0.03, "iii^6": 0.004, "I^4_3": 0.003,

    "II^6_4": 0.005,

    "I^4_2": 0.002,

    "iii^6_4": 0.004, "V^6": 0.01, "I^4_2": 0.005,

    "vi^6_5": 0.003,

    "vii^6_5": 0.006,

    "iii^6_5": 0.003,

    "Isus2": 0.005, "Isus4": 0.005, "Imaj7sus2": 0.003,

    "IIsus2": 0.003, "IIsus4": 0.005,

    "vi7sus4": 0.002,

    "Iadd11": 0.005, "I7add11": 0.002,

    "II11": 0.002,

    "iii11": 0.004,

    "Other": 0.0005 * (0.22 / 0.18)
}

#Sum = 0.894

#"ivsus2": 0.003, "iv7sus2": 0.002,

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

    "vi^4_2": 0.003, "iii^6_5": 0.003, "I^6_4": 0.01, "V^11": 0.005, "V11": 0.005,

    "V^6/vi": 0.001, "V^6_5/vi": 0.001, "iv^6": 0.001,

    "ii^6_4": 0.001, "IV^6": 0.005,

    "V^6": 0.01, "V^6_5": 0.001, "iii^6_4": 0.003, "I^4_2": 0.003,

    "vi^6_5": 0.004,

    "ii^6_5": 0.004, "ii^o6_5": 0.002,

    "iii^6_5": 0.003,

    "Isus2": 0.003, "Imaj7sus2": 0.001, "Isus4": 0.003,

    "IVsus2": 0.004,

    "Vsus4": 0.007, "V7sus4": 0.003,

    "Vadd11": 0.001,

    "Other": 0.0005
}

#Sum = 0.884

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

    "I^11": 0.01, "I11": 0.01,

    "IV^6_4": 0.01, "iv^6_4": 0.002, "vi^6": 0.002, "ii^4_2": 0.003,

    "v^6_4": 0.001, "VII^6": 0.004,

    "I^6": 0.01, "I^6_5": 0.001,

    "ii^6": 0.002, "VII^6_4": 0.007,

    "I^6_4": 0.02, "I^4_3": 0.002,

    "iv^6": 0.002,
    
    "IV^6": 0.01,

    "I^4_2": 0.01, "v^6": 0.002, "IV^6_4/VII": 0.002,

    "vi^6_5": 0.005,

    "i^6_5": 0.001,

    "ii^6_5": 0.003,

    "v^6_5": 0.005,

    "Isus2": 0.005, "Isus4": 0.008, "I7sus4": 0.003, "IV^6_4sus4": 0.002,

    "IVsus2": 0.003,

    "vsus4": 0.002, "v7sus4": 0.002,

    "VIIsus2": 0.004,

    "Iadd11": 0.002,

    "ii11": 0.002,

    "v11": 0.002,

    "Other": 0.0005 * (0.26 / 0.18)
}

#Sum = 0.894

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

    "IV^6_4": 0.01, "ii^4_2": 0.005, "IV^4_3": 0.002,

    "VII^6": 0.007, "v^6_4": 0.002,

    "i^6": 0.01, "IV^4_2": 0.003,

    "ii^6": 0.004, "VII^6_4": 0.003,

    "IV^11": 0.002, "IV11": 0.002,

    "i^6_4": 0.01, "i^4_3": 0.002, "III^6": 0.003,

    "IV^6": 0.009, "ii^6_4": 0.001,

    "v^6": 0.003, "III^6_4": 0.005, "i^4_2": 0.008,

    "vi^o6_5": 0.007,

    "i^6_5": 0.006,

    "ii^6_5": 0.004,

    "v^6_5": 0.003,

    "isus2": 0.003, "isus4": 0.002, "i7sus2": 0.003, "i7sus4": 0.002,

    "IIIsus2": 0.001,

    "IVsus2": 0.002, "IVsus4": 0.004, "IV7sus2": 0.002, "IV7sus4": 0.001,

    "vsus4": 0.001,

    "VIIsus2": 0.001, "VIIsus4": 0.001,

    "iadd11": 0.002,

    "i11": 0.004,

    "v11": 0.002,

    "Other": 0.0005 * (0.19 / 0.18)
}

#Sum = 0.89

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

    "i^4_2": 0.005, "v^6": 0.005, "III^6_4": 0.006, "VII^11": 0.001, "VII11": 0.001,

    "V^6": 0.006, "V^6_5": 0.002,

    "i^6_5": 0.003,

    "ii^o6_5": 0.002,

    "iv^6_5": 0.003,

    "v^6_5": 0.005,

    "isus2": 0.003, "isus4": 0.003, "i7sus2": 0.001,

    "ivsus2": 0.002, "iv7sus2": 0.001,

    "vsus4": 0.003, "v7sus4": 0.002,

    "VIsus2": 0.001,

    "VIIsus2": 0.001, "VIIsus4": 0.003,

    "i11": 0.003,
    
    "Other": 0.0005
}

#Sum = 0.

PHRYGIAN_PROBS = {
    "i": 0.27, "II": 0.16, "III": 0.06, "iv": 0.04, "vii": 0.05,

    "I": 0.03, "ii": 0.002, "#ii": 0.004, "iii": 0.002, "#iii": 0.002,

    "IV": 0.008, "bV": 0.01, "v": 0.007, "V": 0.006, "VI": 0.03, "#vi": 0.002, "V/#ii": 0.002,

    "VII": 0.006, "V/#iii": 0.003, "#vii": 0.006,

    "iv^6_4": 0.005, "II^4_2": 0.004, "VI^6": 0.004,

    "vii^6": 0.007, "III^4_2": 0.002,

    "VI^6_4": 0.001, "i^6": 0.008, "iv^4_2": 0.002,

    "II^6": 0.003,

    "i^6_4": 0.01, "III^6": 0.002,

    "II^6_4": 0.006, "iv^6": 0.002,

    "i^4_2": 0.005, "III^6_4": 0.002, "i^4_2sus4": 0.002,

    "i7": 0.02, "isus2": 0.002, "isus4": 0.004, "i7sus4": 0.003, "iadd11": 0.002,

    "IIsus2": 0.002, "II7sus4": 0.002, "IImaj7": 0.03, "IImaj9": 0.003, "IIadd9": 0.002, "vii^6_5": 0.004,

    "III7": 0.002, "IIIadd6": 0.002,

    "iv7": 0.007, "iv9": 0.003, "ivsus2": 0.002, "iv7sus4": 0.002,

    "V7/i": 0.002,

    "VImaj7": 0.01,

    "vii7": 0.009, "viisus2": 0.002, "viiadd9": 0.001,

    "Other": 0.0005 * (0.27 / 0.18)
}

LOCRIAN_PROBS = {
    "i": 0.04, "I": 0.02, "Imaj7": 0.009, "II^4_2": 0.01,

    "II": 0.09,

    "#ii": 0.01,

    "V/VI": 0.01, "iii": 0.07, "iii7": 0.01,

    "#iii": 0.009,

    "V/vii": 0.01, "iv": 0.06,

    "V": 0.14, "iii^6": 0.01,

    "VI": 0.04, "VI7": 0.009,

    "vii": 0.03,

    "Other": 0.0005 * (0.28 / 0.18)
}

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
    elif ch.endswith("m"):
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

        #if interval == 6 and quality == "sus2": return "ivsus2"
        #if interval == 6 and quality == "dominant7sus2": return "iv7sus2"

        if interval == 9 and quality == "dominant7sus4": return "vi7sus4"

        if interval == 0 and quality == "add11": return "Iadd11"
        if interval == 0 and quality == "dominant7add11": return "I7add11"

        if interval == 2 and quality == "11": return "II11"

        if interval == 4 and quality == "minor11": return "iii11"
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
        elif interval == 7 and quality == "11": return "V11"

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

        if interval == 0 and quality == "11": return "I11"

        if interval == 2 and quality == "minor11": return "ii11"

        if interval == 7 and quality == "minor11": return "v11"

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

        #if upper_interval == 3 and bass_interval == 5 and quality == "major11": return "IV11"

        if upper_interval == 3 and bass_interval == 5 and quality == "major": return "IV^11"
        elif interval == 5 and quality == "11": return "IV11"

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
        elif interval == 10 and quality == "11": return "VII11"

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
        return "Other"
    # Phrygian mode degrees
    if mode == "phrygian":
        if interval == 0 and quality == "minor": return "i"
        if interval == 1 and quality == "major": return "II"
        if interval == 3 and quality == "major": return "III"
        if interval == 5 and quality == "minor": return "iv"
        if interval == 10 and quality == "minor": return "vii"
        # Non-diatonic chords
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
    # Locrian mode degrees
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

def compute_posterior(chord_history, PRIORS):
    scores = {}

    for key in PRIORS:
        tonic, mode = key.split()
        score = PRIORS[key]

        for (root_i, quality_i, bass_i) in chord_history:

            if bass_i is None:
                iv = interval(tonic, root_i)
                upper_interval = None
                bass_interval = None
            else:
                iv = None
                upper_interval = interval(tonic, root_i)
                bass_interval = interval(tonic, bass_i)

            deg = degree_name(iv, upper_interval, bass_interval, quality_i, mode)

            if mode == "lydian":
                lk = LYDIAN_PROBS.get(deg, LYDIAN_PROBS["Other"])
            elif mode == "major":
                lk = MAJOR_PROBS.get(deg, MAJOR_PROBS["Other"])
            elif mode == "mixolydian":
                lk = MIXOLYDIAN_PROBS.get(deg, MIXOLYDIAN_PROBS["Other"])
            elif mode == "dorian":
                lk = DORIAN_PROBS.get(deg, DORIAN_PROBS["Other"])
            elif mode == "minor":
                lk = MINOR_PROBS.get(deg, MINOR_PROBS["Other"])
            elif mode == "phrygian":
                lk = PHRYGIAN_PROBS.get(deg, PHRYGIAN_PROBS["Other"])
            elif mode == "locrian":
                lk = LOCRIAN_PROBS.get(deg, LOCRIAN_PROBS["Other"])

            score *= lk

        scores[key] = score

    # Normalize
    Z = sum(scores.values())
    for k in scores:
        scores[k] /= Z

    adjusted_scores = scores

    return adjusted_scores

import numpy as np
from itertools import combinations

def build_likelihood_matrix(ALL_CHORDS, PRIORS):
    keys = list(PRIORS.keys())
    K = len(keys)
    C = len(ALL_CHORDS)

    LIK = np.zeros((K, C))

    for ki, key in enumerate(keys):
        tonic, mode = key.split()
        for ci, (root, quality, bass) in enumerate(ALL_CHORDS):

            if bass is None:
                iv = interval(tonic, root)
                upper_interval = None
                bass_interval = None
            else:
                iv = None
                upper_interval = interval(tonic, root)
                bass_interval = interval(tonic, bass)

            deg = degree_name(iv, upper_interval, bass_interval, quality, mode)

            if mode == "lydian":
                lk = LYDIAN_PROBS.get(deg, LYDIAN_PROBS["Other"])
            elif mode == "major":
                lk = MAJOR_PROBS.get(deg, MAJOR_PROBS["Other"])
            elif mode == "mixolydian":
                lk = MIXOLYDIAN_PROBS.get(deg, MIXOLYDIAN_PROBS["Other"])
            elif mode == "dorian":
                lk = DORIAN_PROBS.get(deg, DORIAN_PROBS["Other"])
            elif mode == "minor":
                lk = MINOR_PROBS.get(deg, MINOR_PROBS["Other"])
            elif mode == "phrygian":
                lk = PHRYGIAN_PROBS.get(deg, PHRYGIAN_PROBS["Other"])
            elif mode == "locrian":
                lk = LOCRIAN_PROBS.get(deg, LOCRIAN_PROBS["Other"])

            LIK[ki, ci] = lk

    return keys, LIK

def grid_search_best_4():
    # Build ALL_CHORDS
    QUALITIES = ["major", "minor", "dominant7", "major7", "minor7", "sus2", "sus4"]
    ALL_CHORDS = [(p, q, None) for p in PITCHES for q in QUALITIES]

    # Build PRIORS
    PRIORS = {}
    for p in PITCHES:
        PRIORS[p + " lydian"] = (1 / 84) * (0.18 / 0.22) * (143 / 133) * (53067 / 49921) * (698894 / 658139)
        PRIORS[p + " major"] = (1 / 84) * (143 / 133) * (53067 / 49921) * (698894 / 658139)
        PRIORS[p + " mixolydian"] = (1 / 84) * (0.18 / 0.26) * (143 / 133) * (53067 / 49921) * (698894 / 658139)
        PRIORS[p + " dorian"] = (1 / 84) * (143 / 133) * (0.18 / 0.19) * (53067 / 49921) * (698894 / 658139)
        #0.19
        PRIORS[p + " minor"] = (1 / 84) * (143 / 133) * (53067 / 49921) * (698894 / 658139)
        #0.18
        PRIORS[p + " phrygian"] = (1 / 84) * (143 / 133) * (0.18 / 0.27) * (53067 / 49921) * (698894 / 658139)
        #0.27
        PRIORS[p + " locrian"] = (1 / 84) * (143 / 133) * (53067 / 49921) * (0.18 / 0.28) * (698894 / 658139)
    # Build likelihood matrix
    keys, LIK = build_likelihood_matrix(ALL_CHORDS, PRIORS)

    # Convert to log-likelihoods
    logLIK = np.log(LIK)
    logPRIORS = np.log(np.array([PRIORS[k] for k in keys]))

    # Key indices
    Cmaj_idx = keys.index("C major")
    Amin_idx = keys.index("A minor")

    best_val = -np.inf
    best_combo = None

    # Precompute roots for distinctness constraint
    roots = [c[0] for c in ALL_CHORDS]

    # Iterate over combinations of 4 chords
    for combo in combinations(range(len(ALL_CHORDS)), 3):

        r1, r2, r3 = roots[combo[0]], roots[combo[1]], roots[combo[2]]
        if len({r1, r2, r3}) < 3:
            continue

        # Sum log-likelihoods
        log_score_vec = logPRIORS + logLIK[:, combo[0]] + logLIK[:, combo[1]] + logLIK[:, combo[2]]

        # Convert back to probabilities
        score_vec = np.exp(log_score_vec)
        score_vec /= score_vec.sum()

        val = score_vec[Cmaj_idx] * score_vec[Amin_idx]

        if val > best_val:
            best_val = val
            best_combo = combo
            print("New best:", best_combo, best_val)

            best_chords = tuple(ALL_CHORDS[i] for i in best_combo)
            print("Best chords:", best_chords)
            print("Best value:", best_val)

    return tuple(ALL_CHORDS[i] for i in best_combo), best_val



def main():
    QUALITIES = ["major", "minor", "6", "minor6", "dominant7", "major7", "minor7", "dominant9",
             "major9", "minor9", "add9", "minoradd9", "11", "minor11", "add11", "minoradd11", "sus2", "major7sus2", "minor7sus2", "dominant7sus2",
             "sus4", "major7sus4", "minor7sus4", "dominant7sus4"]
    PRIORS = {}
    for p in PITCHES:
        PRIORS[p + " lydian"] = (1 / 84) * (0.18 / 0.22) * (143 / 133) * (53067 / 49921) * (698894 / 658139)
        PRIORS[p + " major"] = (1 / 84) * (143 / 133) * (53067 / 49921) * (698894 / 658139)
        PRIORS[p + " mixolydian"] = (1 / 84) * (0.18 / 0.26) * (143 / 133) * (53067 / 49921) * (698894 / 658139)
        PRIORS[p + " dorian"] = (1 / 84) * (143 / 133) * (0.18 / 0.19) * (53067 / 49921) * (698894 / 658139)
        #0.19
        PRIORS[p + " minor"] = (1 / 84) * (143 / 133) * (53067 / 49921) * (698894 / 658139)
        #0.18
        PRIORS[p + " phrygian"] = (1 / 84) * (143 / 133) * (0.18 / 0.27) * (53067 / 49921) * (698894 / 658139)
        #0.27
        PRIORS[p + " locrian"] = (1 / 84) * (143 / 133) * (53067 / 49921) * (0.18 / 0.28) * (698894 / 658139)
    # Initialize scores
    scores = {}
    for p in PITCHES:
        scores[p + " lydian"] = 1 / 84
        scores[p + " major"] = 1 / 84
        scores[p + " mixolydian"] = 1 / 84
        scores[p + " dorian"] = 1 / 84
        scores[p + " minor"] = 1 / 84
        scores[p + " phrygian"] = 1 / 84
        scores[p + " locrian"] = 1 / 84
    chord_history = []
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

        # Store the chord
        chord_history.append((root, quality, bass))

        adjusted_scores = compute_posterior(chord_history, PRIORS)

        items = sorted(adjusted_scores.items(), key=lambda x: x[1], reverse=True)
        labels = [k for k, _ in items]
        values = [v for _, v in items]

        print("\nProbabilities:")
        for k, v in items:
            print(f"{k}: {v:.6f}")
        print()

        # Standard chromatic order (for arithmetic)
        standard_chromatic = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        standard_index = {t: i for i, t in enumerate(standard_chromatic)}

        # Circle of fifths order starting at C (12 tonics)
        cof = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F"]
        cof_index = {t: i for i, t in enumerate(cof)}

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

        # Step around the color wheel: 1/12 of full circle per semitone-step on our 12-part wheel
        step = 1.0 / 12.0

        # Build a mapping from standard tonic -> color, but assign hues according to circle-of-fifths order
        parent_color = {}
        for i, tonic in enumerate(cof):
            hue = (base_h + step * i) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, base_s, base_v)
            parent_color[tonic] = rgb01_to_hex(rgb)
        # Ensure every standard chromatic name has a color (cof covers all 12 names)
        # Fallback color (shouldn't be used)
        default_color = "#888888"

        # Function to compute the parent major tonic for a given "Tonic mode" label
        def parent_major_of(label):
            # label format: "Tonic mode" e.g., "C major" or "C# minor"
            parts = label.split()
            if len(parts) < 2:
                return None
            tonic = parts[0]
            mode = parts[1]
            mode_key = "minor" if mode == "minor" else mode
            if tonic not in standard_index or mode_key not in mode_to_degree:
                return None
            degree = mode_to_degree[mode_key]
            semitone_offset = degree_intervals[degree]
            parent_idx = (standard_index[tonic] - semitone_offset) % 12
            return standard_chromatic[parent_idx]

        # Map each per-mode label to the parent-major color (using circle-of-fifths assignment)
        per_mode_colors = []
        for lab in labels:
            parent = parent_major_of(lab)
            if parent is None:
                per_mode_colors.append(default_color)
            else:
                # parent is a standard chromatic name like "A" or "C#"
                # find its color via the cof->color mapping: parent may appear in cof list
                # if parent is not in cof (shouldn't happen), fallback to default
                per_mode_colors.append(parent_color.get(parent, default_color))

        # -------------------------
        # Second plot: summed "major field" histogram (12 bars)
        # -------------------------
        # Sum probabilities by parent major (reuse probs and parent_major_of)
        parent_sums = {t: 0.0 for t in standard_chromatic}
        for label, p in adjusted_scores.items():
            parent = parent_major_of(label)
            if parent is None:
                continue
            parent_sums[parent] += p

        # Prepare sorted data (highest -> lowest)
        parent_items = sorted(parent_sums.items(), key=lambda x: x[1], reverse=True)
        parent_labels = [f"{t} major field" for t, _ in parent_items]
        parent_values = [v for _, v in parent_items]
        # Colors for parent bars: use the same parent_color mapping (circle-of-fifths assignment)
        parent_colors = [parent_color.get(t, default_color) for t, _ in parent_items]

        # -------------------------
        # Third plot: negative log-loss per-mode (12 * 5 bars)
        # -------------------------
        import math

        # Compute -ln(p) for each per-mode probability
        neglog_values = []
        for v in values:
            if v <= 0:
                neglog_values.append(0.0)
            else:
                neglog_values.append(-math.log(v))

        # -------------------------
        # Fourth plot: negative log-loss major-field histogram (12 bars)
        # -------------------------
        neglog_parent_values = []
        for v in parent_values:
            if v <= 0:
                neglog_parent_values.append(0.0)
            else:
                neglog_parent_values.append(-math.log(v))

    # Plot 1

    # Create figure sized to number of bars (per-mode)
    fig1, ax1 = plt.subplots(figsize=(max(10, len(labels) * 0.35), 6))

    # Vertical bars ordered by probability
    ax1.bar(range(len(labels)), values, color=per_mode_colors)

    # Axes and formatting
    ax1.set_ylim(0, 1)
    ax1.set_ylabel("Probability")
    ax1.set_xlabel("Key and Scale")
    ax1.set_xticks(range(len(labels)))
    ax1.set_xticklabels(labels, rotation=90, fontsize=7)
    ax1.set_yticks([i / 10 for i in range(0, 11)])
    ax1.grid(axis="y", linestyle="--", alpha=0.3)

    # Compact legend: one entry per parent major (12 tonics) in circle-of-fifths order
    from matplotlib.patches import Patch
    legend_patches = [Patch(color=parent_color[t], label=t) for t in cof]
    ax1.legend(handles=legend_patches, title="Parent Major (CoF order)", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8, title_fontsize=9)

    plt.tight_layout()

    # Plot 2

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

    # Optional compact legend (one patch per tonic in circle-of-fifths order)
    legend_patches2 = [Patch(color=parent_color[t], label=f"{t} major") for t in cof]
    ax2.legend(handles=legend_patches2, title="Parent Major (CoF order)", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8, title_fontsize=9)

    plt.tight_layout()

    # Plot 3

    fig3, ax3 = plt.subplots(figsize=(max(10, len(labels) * 0.35), 6))
    ax3.bar(range(len(labels)), neglog_values, color=per_mode_colors)

    ax3.set_ylabel("Negative Log Loss")
    ax3.set_xlabel("Key and Scale")
    ax3.set_xticks(range(len(labels)))
    ax3.set_xticklabels(labels, rotation=90, fontsize=7)
    ax3.grid(axis="y", linestyle="--", alpha=0.3)

    # Legend (same as before)
    legend_patches3 = [Patch(color=parent_color[t], label=t) for t in cof]
    ax3.legend(handles=legend_patches3, title="Parent Major (CoF order)",
                bbox_to_anchor=(1.02, 1), loc="upper left",
                fontsize=8, title_fontsize=9)

    plt.tight_layout()

    # Plot 4
    fig4, ax4 = plt.subplots(figsize=(max(8, len(parent_labels) * 0.6), 5))
    ax4.bar(range(len(parent_labels)), neglog_parent_values,
            color=parent_colors)

    ax4.set_ylabel("Negative Log Loss")
    ax4.set_xlabel("Major Field")
    ax4.set_xticks(range(len(parent_labels)))
    ax4.set_xticklabels(parent_labels, rotation=90, fontsize=8)
    ax4.grid(axis="y", linestyle="--", alpha=0.3)

    legend_patches4 = [Patch(color=parent_color[t], label=f"{t} major") for t in cof]
    ax4.legend(handles=legend_patches4, title="Parent Major (CoF order)",
                bbox_to_anchor=(1.02, 1), loc="upper left",
                fontsize=8, title_fontsize=9)

    plt.tight_layout()
    plt.show()

    # After user enters "end", scores already contains the final normalized posterior.

    # Find the best key/mode
    best_key = max(adjusted_scores, key=adjusted_scores.get)
    best_prob = adjusted_scores[best_key]

    print("\nFinal best key:", best_key)
    print("Probability:", best_prob)

if __name__ == "__main__":
    best_chords, best_val = grid_search_best_4()
    print("Best chords:", best_chords)
    print("Best value:", best_val)