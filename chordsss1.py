PITCHES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
pitch_to_index = {p:i for i,p in enumerate(PITCHES)}

MAJOR_PROBS = {
    "I": 0.18, "ii": 0.03, "iii": 0.03, "IV": 0.12, "V": 0.12,
    "vi": 0.07,

    # Non-diatonic chords
    "iv": 0.006, "v": 0.001,
    
    "II": 0.007, "bIII": 0.004, "III": 0.007, "VI": 0.004,
    "bVI": 0.005, "bVII": 0.01, "VII": 0.001,

    "Other": 0.00
}

MINOR_PROBS = {
    "i": 0.18, "III": 0.06, "iv": 0.05, "v": 0.04,
    "VI": 0.10, "VII": 0.10,

    # Non-diatonic chords
    "I": 0.01, "ii": 0.002, "IV": 0.01, "V": 0.03, "vii": 0.001,

    "bII": 0.005, "II": 0.002, "bV": 0.002, "#vi": 0.001,

    "Other": 0.00
}

def parse_chord(ch):
    ch = ch.strip()
    if ch.endswith("m"):
        return ch[:-1], "minor"
    return ch, "major"

def interval(a, b):
    return (pitch_to_index[b] - pitch_to_index[a]) % 12

def degree_name(interval, quality, mode):
    # Major mode degrees
    if mode == "major":
        if interval == 0 and quality == "major": return "I"
        if interval == 2 and quality == "minor": return "ii"
        if interval == 4 and quality == "minor": return "iii"
        if interval == 5 and quality == "major": return "IV"
        if interval == 7 and quality == "major": return "V"
        if interval == 9 and quality == "minor": return "vi"

        # Non-diatonic chords
        if interval == 5 and quality == "minor": return "iv"
        if interval == 7 and quality == "minor": return "v"

        if interval == 2 and quality == "major": return "II"
        if interval == 4 and quality == "major": return "III"
        if interval == 3 and quality == "major": return "bIII"
        if interval == 8 and quality == "major": return "bVI"
        if interval == 9 and quality == "major": return "VI"
        if interval == 10 and quality == "major": return "bVII"
        if interval == 11 and quality == "major": return "VII"
        return "Other"

    # Minor mode degrees
    if mode == "minor":
        if interval == 0 and quality == "minor": return "i"
        if interval == 3 and quality == "major": return "III"
        if interval == 5 and quality == "minor": return "iv"
        if interval == 7 and quality == "minor": return "v"
        if interval == 8 and quality == "major": return "VI"
        if interval == 10 and quality == "major": return "VII"

        # Non-diatonic chords
        if interval == 0 and quality == "major": return "I"
        if interval == 2 and quality == "minor": return "ii"
        if interval == 5 and quality == "major": return "IV"
        if interval == 7 and quality == "major": return "V"
        if interval == 10 and quality == "minor": return "vii"

        if interval == 1 and quality == "major": return "bII"
        if interval == 6 and quality == "major": return "bV"
        if interval == 2 and quality == "major": return "II"
        if interval == 9 and quality == "minor": return "#vi"
        return "Other"

def main():
    # Initialize scores
    scores = {}
    for p in PITCHES:
        scores[p + " major"] = 0.0
        scores[p + " minor"] = 0.0

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

            if mode == "major":
                prob = MAJOR_PROBS.get(deg, MAJOR_PROBS["Other"])
            else:
                prob = MINOR_PROBS.get(deg, MINOR_PROBS["Other"])

            scores[key] += prob

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