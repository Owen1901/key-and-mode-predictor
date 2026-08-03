from statistics import mode


PITCHES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
pitch_to_index = {p:i for i,p in enumerate(PITCHES)}

LYDIAN_PROBS = {
    "I": 0.22, "Imaj7": 0.06, "II": 0.11, "iii": 0.05, "V": 0.07, "vi": 0.03, "vii": 0.03,

    # Non-diatonic chords
    "i": 0.004, "bII": 0.003, "bIII": 0.007, "III": 0.01, "bIV": 0.01, "IV": 0.005,
    "bVI": 0.007, "bVII": 0.003,

    "Vmaj7": 0.01, "bVImaj7": 0.002,

    "iii7": 0.01, "vi7": 0.01, "vii7": 0.02, 

    "Other": 0.00
}

MAJOR_PROBS = {
    "I": 0.18, "Imaj7": 0.02, "ii": 0.03, "iii": 0.03, "IV": 0.12, "IVmaj7": 0.02, "V": 0.12,
    "vi": 0.07,

    # Non-diatonic chords
    "iv": 0.006, "v": 0.001,
    
    "II": 0.007, "bIII": 0.004, "III": 0.007, "VI": 0.004,
    "bVI": 0.005, "bVImaj7": 0.002, "bVII": 0.01, "bVIImaj7": 0.001, "VII": 0.001,

    "ii7": 0.03, "iii7": 0.007, "iv7": 0.001, "v7": 0.002, "vi7": 0.02,

    "Other": 0.00
}

MIXOLYDIAN_PROBS = {
    "I": 0.26, "ii": 0.02, "bIII": 0.03, "IV": 0.11, "v": 0.03, "VII": 0.14,

    # Borrowed / chromatic
    "i": 0.002, "bII": 0.003, "II": 0.005, "iii": 0.001, "iv": 0.005,
    "bV": 0.002, "V": 0.02, "bVI": 0.02, "vi": 0.02, "bI": 0.001,

    "Imaj7": 0.002, "bIIImaj7": 0.003, "IVmaj7": 0.006, "bVImaj7": 0.004, "VIImaj7": 0.006,

    "i7": 0.002, "ii7": 0.007, "iv7": 0.001, "v7": 0.01, "vi7": 0.008,

    "Other": 0.00
}

DORIAN_PROBS = {
    "i": 0.19, "ii": 0.02, "III": 0.09, "IIImaj7": 0.009, "IV": 0.12,
    "v": 0.04, "VII": 0.08, "VIImaj7": 0.005,

    # Borrowed / chromatic
    "I": 0.02, "bII": 0.003, "II": 0.004, "iv": 0.002,
    "bV": 0.003, "bVI": 0.02, "bVImaj7": 0.005, "vi": 0.001,

    "i7": 0.06, "ii7": 0.01, "iv7": 0.001, "v7": 0.01,

    "Other": 0.00
}

MINOR_PROBS = {
    "i": 0.18, "III": 0.06, "IIImaj7": 0.005, "iv": 0.05, "v": 0.04,
    "VI": 0.10, "VImaj7": 0.03, "VII": 0.10,

    # Non-diatonic chords
    "I": 0.01, "ii": 0.002, "IV": 0.01, "V": 0.03, "vii": 0.001,

    "bII": 0.005, "bIImaj7": 0.002, "II": 0.002, "bV": 0.002, "#vi": 0.001,

    "i7": 0.03, "iv7": 0.02, "v7": 0.02, "vii7": 0.002, 

    "Other": 0.00
}

def parse_chord(ch):
    ch = ch.strip()

    # longest suffixes first
    if ch.endswith("maj7"):
        return ch[:-4], "major7"
    elif ch.endswith("m7"):
        return ch[:-2], "minor7"
    elif ch.endswith("m"):
        return ch[:-1], "minor"
    else:
        return ch, "major"

def interval(a, b):
    return (pitch_to_index[b] - pitch_to_index[a]) % 12

def degree_name(interval, quality, mode):

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
        if interval == 8 and quality == "major": return "bVI"
        if interval == 8 and quality == "major7": return "bVImaj7"
        if interval == 9 and quality == "minor": return "vi"

        if interval == 0 and quality == "minor7": return "i7"
        if interval == 2 and quality == "minor7": return "ii7"
        if interval == 5 and quality == "minor7": return "iv7"
        if interval == 7 and quality == "minor7": return "v7"
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

        root, quality = parse_chord(user)
        if root not in PITCHES:
            print("Invalid chord.")
            continue

        for key in scores:
            tonic, mode = key.split()
            iv = interval(tonic, root)
            deg = degree_name(iv, quality, mode)

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
        total = sum(scores.values())
        print("\nProbabilities:")
        for k in scores:
            print(f"{k}: {scores[k]/total:.4f}")
        print()

    # Final result
    total = sum(scores.values())
    final_probs = {k: scores[k]/total for k in scores}
    best = max(final_probs, key=final_probs.get)

    print("\nMost likely key:", best)
    print("Probability:", final_probs[best])

if __name__ == "__main__":
    main()