# fractional_scale_mode_detector.py
# Implements EXACTLY the rules you specified:
# - fractional scoring (0 to 1 per chord per scale)
# - repeated notes counted individually
# - chromatic notes treated fractionally (no special handling)
# - mode detection using most frequent notes
# - tie-handling: all combinations of tied scales × tied tonics

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

def fractional_score(chord_notes, scale_notes):
    count = sum(1 for n in chord_notes if n in scale_notes)
    return count / len(chord_notes)

def determine_modes(tied_scales, tied_tonics):
    modes = []
    mode_names = [
        "Ionian (major)", "Dorian", "Phrygian", "Lydian",
        "Mixolydian", "Aeolian (minor)", "Locrian"
    ]

    for scale in tied_scales:
        scale_notes = MAJOR_SCALES[scale]
        for tonic in tied_tonics:
            if tonic in scale_notes:
                idx = scale_notes.index(tonic)
                modes.append(f"{scale} major → {tonic} {mode_names[idx]}")
            else:
                modes.append(f"{scale} major → {tonic} (non-diatonic tonic)")
    return modes

def main():
    print("Fractional Major Scale Detector + Multi-Mode Tie Expansion")
    print("Enter chords like: FAC, GGBD, CEGF#, F#A#C#, BbDF")
    print("Type 'end' to finish.\n")

    scores = {root: 0.0 for root in PITCHES}
    note_counts = {p: 0 for p in PITCHES}

    while True:
        user = input("\nEnter chord: ").strip()
        if user.lower() == "end":
            break

        parsed = parse_chord_input(user)
        if parsed is None:
            print("Invalid chord.")
            continue

        # Count repeated notes individually
        for n in parsed:
            note_counts[n] += 1

        # Fractional scoring
        for root, scale_notes in MAJOR_SCALES.items():
            frac = fractional_score(parsed, scale_notes)
            scores[root] += frac

        # Print probability distribution
        total_points = sum(scores.values())
        if total_points == 0:
            print("All probabilities = 1/12 (no points yet)")
        else:
            print("\nProbabilities:")
            for root in PITCHES:
                p = scores[root] / total_points
                print(f"{root}: {p:.4f}")

    # Final probability distribution
    total_points = sum(scores.values())
    if total_points == 0:
        print("\nNo chords entered.")
        return

    probs = {root: scores[root] / total_points for root in PITCHES}
    max_prob = max(probs.values())

    tied_scales = [root for root, p in probs.items() if abs(p - max_prob) < 1e-12]

    # Determine tied tonics (most frequent notes)
    max_count = max(note_counts.values())
    tied_tonics = [n for n, c in note_counts.items() if c == max_count]

    print("\nTied scales:", tied_scales)
    print("Tied tonics:", tied_tonics)

    print("\nModes:")
    modes = determine_modes(tied_scales, tied_tonics)
    for m in modes:
        print(m)

if __name__ == "__main__":
    main()