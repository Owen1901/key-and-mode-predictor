# scale_mode_detector_two_stage.py
# Stage 1: fractional major-scale detection from chords
# Stage 2: measure-based mode detection from melody, with X as a beat

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

def stage1_get_tied_scales_and_note_counts():
    print("Stage 1: Fractional Major Scale Detection (Chords)")
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

        for n in parsed:
            note_counts[n] += 1

        for root, scale_notes in MAJOR_SCALES.items():
            frac = fractional_score(parsed, scale_notes)
            scores[root] += frac

        total_points = sum(scores.values())
        if total_points == 0:
            print("All probabilities = 1/12 (no points yet)")
        else:
            print("\nProbabilities:")
            for root in PITCHES:
                p = scores[root] / total_points
                print(f"{root}: {p:.4f}")

    total_points = sum(scores.values())
    if total_points == 0:
        print("\nNo chords entered.")
        return [], note_counts

    probs = {root: scores[root] / total_points for root in PITCHES}
    max_prob = max(probs.values())
    tied_scales = [root for root, p in probs.items() if abs(p - max_prob) < 1e-12]

    print("\nTied major scales:", tied_scales)
    return tied_scales, note_counts

def get_modes_for_scale(scale_root):
    scale_notes = MAJOR_SCALES[scale_root]
    mode_names = [
        "Ionian (major)", "Dorian", "Phrygian", "Lydian",
        "Mixolydian", "Aeolian (minor)", "Locrian"
    ]
    modes = []
    for i, tonic in enumerate(scale_notes):
        modes.append((tonic, mode_names[i]))
    return modes  # list of (tonic_note, mode_name)

def stage2_mode_detection(tied_scales):
    if not tied_scales:
        print("\nSkipping Stage 2: no tied scales from Stage 1.")
        return

    print("\nStage 2: Measure-based Mode Detection (Melody)")
    beats_per_measure = None
    while beats_per_measure is None:
        try:
            bpm_input = input("Enter number of beats per measure: ").strip()
            beats_per_measure = int(bpm_input)
            if beats_per_measure <= 0:
                print("Beats per measure must be positive.")
                beats_per_measure = None
        except ValueError:
            print("Please enter an integer.")

    # Build mode list: each tied scale has 7 modes
    mode_entries = []  # list of dicts: { 'scale': root, 'tonic': note, 'name': mode_name, 'score': float }
    for scale in tied_scales:
        for tonic, mode_name in get_modes_for_scale(scale):
            mode_entries.append({
                "scale": scale,
                "tonic": tonic,
                "name": mode_name,
                "score": 0.0
            })

    print("\nEnter melody for each measure as a string of length", beats_per_measure,
          "using notes (e.g., C, D#, Bb) or X for no note.")
    print("Type 'end' when done.\n")

    while True:
        measure = input("Enter measure melody: ").strip()
        if measure.lower() == "end":
            break

        # Parse measure into beats: we expect one character or two (for #/b) per beat,
        # but you specified a simple string like FFXF, so we treat each character as a beat.
        # Here we assume single-letter notes or X only.
        if len(measure) != beats_per_measure:
            print(f"Measure must have exactly {beats_per_measure} characters.")
            continue

        beats = list(measure.upper())

        # For each mode, compute fraction of beats that are its tonic (X counts as a beat)
        for entry in mode_entries:
            tonic = entry["tonic"]
            count_tonic = sum(1 for b in beats if b == tonic)
            frac = count_tonic / beats_per_measure
            entry["score"] += frac

        # Print mode probabilities after this measure
        total_mode_score = sum(e["score"] for e in mode_entries)
        if total_mode_score == 0:
            print("\nAll mode probabilities = equal (no tonic evidence yet).")
        else:
            print("\nMode probabilities after this measure:")
            for e in mode_entries:
                p = e["score"] / total_mode_score
                print(f"{e['scale']} major → {e['tonic']} {e['name']}: {p:.4f}")

    # Final mode determination
    total_mode_score = sum(e["score"] for e in mode_entries)
    if total_mode_score == 0:
        print("\nNo melodic evidence for modes.")
        return

    max_score = max(e["score"] for e in mode_entries)
    tied_modes = [e for e in mode_entries if abs(e["score"] - max_score) < 1e-12]

    print("\nFinal tied modes:")
    for e in tied_modes:
        print(f"{e['scale']} major → {e['tonic']} {e['name']}")

def main():
    tied_scales, _ = stage1_get_tied_scales_and_note_counts()
    stage2_mode_detection(tied_scales)

if __name__ == "__main__":
    main()