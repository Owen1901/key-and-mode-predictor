# mode_detector_with_ties.py
# Implements your exact rule, plus:
# If multiple major scales tie for highest probability,
# print the mode for EACH tied scale.

ENHARMONIC = {
    "C": "C",   "B#": "C",
    "C#": "C#", "Db": "C#",
    "D": "D",
    "D#": "D#", "Eb": "D#",
    "E": "E",   "Fb": "E",
    "F": "F",   "E#": "F",
    "F#": "F#", "Gb": "F#",
    "G": "G",
    "G#": "G#", "Ab": "G#",
    "A": "A",
    "A#": "A#", "Bb": "A#",
    "B": "B",   "Cb": "B"
}

PITCHES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
MAJOR_INTERVALS = [2,2,1,2,2,2,1]

def build_major_scale(root):
    idx = PITCHES.index(root)
    notes = [root]
    for step in MAJOR_INTERVALS[:-1]:
        idx = (idx + step) % 12
        notes.append(PITCHES[idx])
    return notes

MAJOR_SCALES = {root: build_major_scale(root) for root in PITCHES}

def parse_chord_input(s):
    s = s.replace(" ", "").replace(",", "").strip()
    notes = []
    i = 0
    while i < len(s):
        ch = s[i].upper()
        if ch not in "ABCDEFG":
            return None

        if i + 1 < len(s) and s[i+1] in ("#", "b"):
            token = ch + s[i+1]
            i += 2
        else:
            token = ch
            i += 1

        if token in ENHARMONIC:
            notes.append(ENHARMONIC[token])
        else:
            return None

    return notes

def print_probabilities(counts, total):
    if total == 0:
        prob = 1/12
        print("\nUniform prior:")
        for root in PITCHES:
            print(f"{root}: {prob:.4f}")
        return None

    fractions = {root: counts[root] / total for root in PITCHES}
    s = sum(fractions.values())

    if s == 0:
        prob = 1/12
        print("\nNo matches. Uniform probabilities:")
        for root in PITCHES:
            print(f"{root}: {prob:.4f}")
        return None

    probs = {root: fractions[root] / s for root in PITCHES}

    print(f"\nTotal chords: {total}")
    for root in PITCHES:
        print(f"{root}: count={counts[root]:2d}  prob={probs[root]:.4f}")

    return probs

def determine_mode(scale_root, note_counts):
    tonic = max(note_counts, key=lambda n: note_counts[n])
    scale_notes = MAJOR_SCALES[scale_root]

    if tonic not in scale_notes:
        return f"{tonic} is not in {scale_root} major scale"

    index = scale_notes.index(tonic)
    mode_names = [
        "Ionian (major)", "Dorian", "Phrygian", "Lydian",
        "Mixolydian", "Aeolian (minor)", "Locrian"
    ]

    return f"{tonic} {mode_names[index]}"

def main():
    print("Chord-based major key + mode detector (with tie handling).")
    print("Enter chords like FAC, F#A#C#, DF#A#, CEGA, CG, BbDF")
    print("Type 'end' to finish.\n")

    counts = {root: 0 for root in PITCHES}
    total = 0
    note_counts = {p: 0 for p in PITCHES}

    print_probabilities(counts, total)

    while True:
        user = input("\nEnter chord: ").strip()
        if user.lower() == "end":
            print("\nFinal probabilities:")
            probs = print_probabilities(counts, total)

            if probs is None:
                print("\nCannot determine mode because no scale had any matches.")
                break

            # Find highest probability value
            max_prob = max(probs.values())

            # Find all scales tied for highest probability
            tied_scales = [root for root, p in probs.items() if abs(p - max_prob) < 1e-12]

            print(f"\nMost likely major scales (tie): {tied_scales}")

            print("\nModes for each tied scale:")
            for scale in tied_scales:
                mode = determine_mode(scale, note_counts)
                print(f"{scale} major → {mode}")

            break

        parsed = parse_chord_input(user)
        if parsed is None:
            print("Invalid chord. Try again.")
            continue

        for n in parsed:
            note_counts[n] += 1

        total += 1
        for root, scale_notes in MAJOR_SCALES.items():
            if all(note in scale_notes for note in parsed):
                counts[root] += 1

        print_probabilities(counts, total)

if __name__ == "__main__":
    main()