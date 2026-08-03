# key_detector.py
# Simple major-key predictor based on notes entered by the user.
# Type notes like: C, D, E, F#, Bb, Ab, A#  (case-insensitive)
# Type "end" to stop.

# Map flat names to equivalent sharp names
ENHARMONIC = {
    "C": "C", "B#": "C",
    "C#": "C#", "Db": "C#",
    "D": "D",
    "D#": "D#", "Eb": "D#",
    "E": "E", "Fb": "E",
    "F": "F", "E#": "F",
    "F#": "F#", "Gb": "F#",
    "G": "G",
    "G#": "G#", "Ab": "G#",
    "A": "A",
    "A#": "A#", "Bb": "A#",
    "B": "B", "Cb": "B"
}

# Canonical pitch class order (using sharps)
PITCHES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

# Build major scales programmatically using semitone intervals for major scale
# Major scale intervals in semitones: 2,2,1,2,2,2,1
MAJOR_INTERVALS = [2,2,1,2,2,2,1]

def build_major_scale(root):
    """Return list of pitch names (canonical sharps) in the major scale for root."""
    root_idx = PITCHES.index(root)
    notes = [root]
    idx = root_idx
    for step in MAJOR_INTERVALS[:-1]:  # last step returns to octave
        idx = (idx + step) % 12
        notes.append(PITCHES[idx])
    return notes  # 7 notes

# Create dictionary of 12 major scales
MAJOR_SCALES = {root: build_major_scale(root) for root in PITCHES}

def normalize_note(note_str):
    """Normalize user input to canonical sharp pitch (e.g., 'Bb' -> 'A#')."""
    note = note_str.strip().upper()
    # Allow inputs like 'A#' or 'Bb' or 'c' or ' f# '
    # Normalize accidental characters: accept '#' and 'B' for flat (user uses 'b' or 'B')
    # If user typed 'b' as lowercase flat, upper() made it 'B' which collides with note B.
    # So handle two-character tokens where second char is '#' or 'b'/'B'.
    if len(note) >= 2 and note[1] in ("#", "B"):
        # keep first char and second char as accidental
        token = note[0] + note[1]
    else:
        token = note[0]
    # Map flats like 'DB' to 'C#' etc. Also accept 'BB' as 'A#' (Bb)
    # Convert 'B' accidental to 'b' meaning flat only when token length==2 and second char is 'B'
    if len(token) == 2 and token[1] == "B":
        token = token[0] + "b"  # convert to 'Db' style for lookup
    # Try direct mapping
    if token in ENHARMONIC:
        return ENHARMONIC[token]
    # If not found, try full uppercase input (covers 'EB' etc.)
    if note in ENHARMONIC:
        return ENHARMONIC[note]
    return None

def print_probabilities(counts, total_notes):
    """Compute fractions and normalized probabilities and print them."""
    if total_notes == 0:
        # Uniform prior before any notes
        prob = 1.0 / 12.0
        print("\nNo notes entered yet. Prior is uniform:")
        for root in PITCHES:
            print(f"{root} major: {prob:.4f}")
        return

    # Unnormalized fractions: count_in_scale / total_notes
    fractions = {root: counts[root] / total_notes for root in PITCHES}
    s = sum(fractions.values())
    if s == 0:
        # No scale matched any entered notes (unlikely), fall back to uniform
        prob = 1.0 / 12.0
        print("\nNo matches found for entered notes. Reporting uniform probabilities:")
        for root in PITCHES:
            print(f"{root} major: {prob:.4f}")
        return

    # Normalized probabilities
    probs = {root: fractions[root] / s for root in PITCHES}

    print(f"\nTotal notes entered: {total_notes}")
    print("Counts of notes that belong to each major scale and normalized probabilities:")
    for root in PITCHES:
        print(f"{root} major: count={counts[root]:2d}  prob={probs[root]:.4f}")

def main():
    print("Major-key predictor (major scales only).")
    print("Enter notes one at a time (C, D, E, F#, Bb, Ab, A#). Type 'end' to finish.\n")

    # Initialize counts for each scale
    counts = {root: 0 for root in PITCHES}
    total_notes = 0

    # Show initial uniform prior
    print_probabilities(counts, total_notes)

    while True:
        user = input("\nEnter next note (or 'end'): ").strip()
        if user.lower() == "end":
            print("\nFinished. Final probabilities:")
            print_probabilities(counts, total_notes)
            break
        if user == "":
            print("Empty input; please enter a note or 'end'.")
            continue

        normalized = normalize_note(user)
        if normalized is None:
            print("Unrecognized note. Valid examples: C, C#, Db, D, D#, Eb, E, F, F#, Gb, G, G#, Ab, A, A#, Bb, B.")
            continue

        # Update totals
        total_notes += 1
        # For each major scale, check if the normalized note is in that scale
        for root, scale_notes in MAJOR_SCALES.items():
            if normalized in scale_notes:
                counts[root] += 1

        # Print updated probabilities
        print_probabilities(counts, total_notes)

if __name__ == "__main__":
    main()