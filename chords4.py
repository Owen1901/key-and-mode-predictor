# fully_chromatic_key_mode_detector.py
# A + B + C combined: theory-aware, statistical, expressive, fully chromatic.

import math

# -----------------------------
# Enharmonic normalization
# -----------------------------
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

# -----------------------------
# Build major scales
# -----------------------------
def build_major_scale(root):
    idx = PITCHES.index(root)
    notes = [root]
    for step in MAJOR_INTERVALS[:-1]:
        idx = (idx + step) % 12
        notes.append(PITCHES[idx])
    return notes

MAJOR_SCALES = {root: build_major_scale(root) for root in PITCHES}

# -----------------------------
# Parse chord input
# -----------------------------
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

# -----------------------------
# Pitch-class profile (Krumhansl-Schmuckler)
# -----------------------------
# Normalized major key profiles
KRUMHANSL_MAJOR = {
    "C":  [6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88],
    "C#": [2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88,6.35],
    "D":  [3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88,6.35,2.23],
    "D#": [2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88,6.35,2.23,3.48],
    "E":  [4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88,6.35,2.23,3.48,2.33],
    "F":  [4.09,2.52,5.19,2.39,3.66,2.29,2.88,6.35,2.23,3.48,2.33,4.38],
    "F#": [2.52,5.19,2.39,3.66,2.29,2.88,6.35,2.23,3.48,2.33,4.38,4.09],
    "G":  [5.19,2.39,3.66,2.29,2.88,6.35,2.23,3.48,2.33,4.38,4.09,2.52],
    "G#": [2.39,3.66,2.29,2.88,6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19],
    "A":  [3.66,2.29,2.88,6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39],
    "A#": [2.29,2.88,6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66],
    "B":  [2.88,6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29]
}

# -----------------------------
# Chord classification relative to a key
# -----------------------------
def classify_chord(notes, key):
    scale = MAJOR_SCALES[key]

    # Diatonic triads
    diatonic = {
        tuple(sorted([scale[0], scale[2], scale[4]])): "I",
        tuple(sorted([scale[1], scale[3], scale[5]])): "ii",
        tuple(sorted([scale[2], scale[4], scale[6]])): "iii",
        tuple(sorted([scale[3], scale[5], scale[0]])): "IV",
        tuple(sorted([scale[4], scale[6], scale[1]])): "V",
        tuple(sorted([scale[5], scale[0], scale[2]])): "vi",
        tuple(sorted([scale[6], scale[1], scale[3]])): "vii°"
    }

    sorted_notes = tuple(sorted(notes))

    if sorted_notes in diatonic:
        return ("diatonic", diatonic[sorted_notes])

    # Secondary dominants: V/X
    for i, target in enumerate(scale):
        # V of target = major triad built on a perfect fifth above target
        target_idx = PITCHES.index(target)
        fifth_idx = (target_idx + 7) % 12
        fifth = PITCHES[fifth_idx]

        # major triad on fifth
        triad = tuple(sorted([
            fifth,
            PITCHES[(fifth_idx + 4) % 12],
            PITCHES[(fifth_idx + 7) % 12]
        ]))

        if sorted_notes == triad:
            return ("secondary", f"V/{target}")

    # Borrowed chords (modal mixture)
    # bIII, bVI, bVII, iv
    borrowed_candidates = {
        "bIII": (PITCHES[(PITCHES.index(key) + 3) % 12],),
        "bVI":  (PITCHES[(PITCHES.index(key) + 8) % 12],),
        "bVII": (PITCHES[(PITCHES.index(key) + 10) % 12],)
    }

    # Check root matches borrowed roots
    root = notes[0]
    for label, roots in borrowed_candidates.items():
        if root in roots:
            return ("borrowed", label)

    # Chromatic mediants: major/minor triads a third away
    # e.g. E major in C, Ab major in C
    return ("chromatic", "chromatic-mediant-or-other")

# -----------------------------
# Weighted likelihood update
# -----------------------------
def update_likelihoods(chord_notes, likelihoods):
    for key in PITCHES:
        ctype, label = classify_chord(chord_notes, key)

        if ctype == "diatonic":
            likelihoods[key] += 3.0

        elif ctype == "secondary":
            likelihoods[key] += 2.0

        elif ctype == "borrowed":
            likelihoods[key] += 1.0

        elif ctype == "chromatic":
            likelihoods[key] += 0.5

# -----------------------------
# Pitch-class profile similarity
# -----------------------------
def profile_similarity(note_counts):
    total = sum(note_counts.values())
    if total == 0:
        return {k: 1/12 for k in PITCHES}

    histogram = [note_counts[p] / total for p in PITCHES]

    sims = {}
    for key in PITCHES:
        profile = KRUMHANSL_MAJOR[key]
        dot = sum(histogram[i] * profile[i] for i in range(12))
        sims[key] = dot

    return sims

# -----------------------------
# Mode detection
# -----------------------------
def determine_mode(key, note_counts):
    tonic = max(note_counts, key=lambda n: note_counts[n])
    scale = MAJOR_SCALES[key]

    if tonic not in scale:
        return f"{tonic} (non-diatonic tonic)"

    index = scale.index(tonic)
    modes = [
        "Ionian (major)", "Dorian", "Phrygian", "Lydian",
        "Mixolydian", "Aeolian (minor)", "Locrian"
    ]
    return f"{tonic} {modes[index]}"

# -----------------------------
# Main program
# -----------------------------
def main():
    print("Fully Chromatic Key + Mode Detector")
    print("Enter chords like: FAC, F#A#C#, DF#A#, CEGA, CG, BbDF")
    print("Type 'end' to finish.\n")

    likelihoods = {k: 0.0 for k in PITCHES}
    note_counts = {p: 0 for p in PITCHES}

    while True:
        user = input("\nEnter chord: ").strip()
        if user.lower() == "end":
            break

        parsed = parse_chord_input(user)
        if parsed is None:
            print("Invalid chord.")
            continue

        for n in parsed:
            note_counts[n] += 1

        update_likelihoods(parsed, likelihoods)

    # Combine likelihoods with pitch-class profile similarity
    sims = profile_similarity(note_counts)

    final_scores = {k: likelihoods[k] + sims[k] for k in PITCHES}

    max_score = max(final_scores.values())
    tied = [k for k, v in final_scores.items() if abs(v - max_score) < 1e-12]

    print("\nMost likely keys:", tied)

    print("\nModes:")
    for key in tied:
        print(f"{key} major → {determine_mode(key, note_counts)}")

if __name__ == "__main__":
    main()