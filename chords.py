# chord_key_detector_clean.py

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
        return

    fractions = {root: counts[root] / total for root in PITCHES}
    s = sum(fractions.values())

    if s == 0:
        prob = 1/12
        print("\nNo matches. Uniform probabilities:")
        for root in PITCHES:
            print(f"{root}: {prob:.4f}")
        return

    probs = {root: fractions[root] / s for root in PITCHES}

    print(f"\nTotal chords: {total}")
    for root in PITCHES:
        print(f"{root}: count={counts[root]:2d}  prob={probs[root]:.4f}")

def main():
    print("Chord-based major key predictor.")
    print("Enter chords like FAC, F#A#C#, DF#A#, CEGA, CG, BbDF")
    print("Type 'end' to finish.\n")

    counts = {root: 0 for root in PITCHES}
    total = 0

    print_probabilities(counts, total)

    while True:
        user = input("\nEnter chord: ").strip()
        if user.lower() == "end":
            print("\nFinal probabilities:")
            print_probabilities(counts, total)
            break

        parsed = parse_chord_input(user)
        if parsed is None:
            print("Invalid chord. Try again.")
            continue

        total += 1
        for root, scale_notes in MAJOR_SCALES.items():
            if all(note in scale_notes for note in parsed):
                counts[root] += 1

        print_probabilities(counts, total)

if __name__ == "__main__":
    main()