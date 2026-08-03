# bayesian_major_minor_detector.py
# Full Bayesian major/minor key detector using Hooktheory chord probabilities.

PITCHES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

# Hooktheory chord probabilities (major context)
MAJOR_PROBS = {
    "I": 0.18,
    "ii": 0.03,
    "ii7": 0.03,
    "IV": 0.12,
    "V": 0.12,
    "vi": 0.07,
    "III": 0.06,
    "VI": 0.10,
    "VII": 0.10,
    "Other": 0.46
}

# Hooktheory chord probabilities (minor context)
MINOR_PROBS = {
    "i": 0.18,
    "III": 0.06,
    "iv": 0.05,
    "v": 0.04,
    "VI": 0.10,
    "VII": 0.10,
    "Other": 0.46
}

def fifth_above(root):
    idx = PITCHES.index(root)
    return PITCHES[(idx + 7) % 12]

def fifth_below(root):
    idx = PITCHES.index(root)
    return PITCHES[(idx - 7) % 12]

def relative_minor(root):
    idx = PITCHES.index(root)
    return PITCHES[(idx + 9) % 12]

def relative_major(root):
    idx = PITCHES.index(root)
    return PITCHES[(idx + 3) % 12]

def parse_chord(s):
    s = s.strip()
    if s.endswith("m"):
        return s[:-1], "minor"
    else:
        return s, "major"

def functional_role_in_major(chord_root, chord_quality, key_root):
    # Determine functional role of chord in a major key
    scale = {
        "I": key_root,
        "ii": PITCHES[(PITCHES.index(key_root) + 2) % 12],
        "iii": PITCHES[(PITCHES.index(key_root) + 4) % 12],
        "IV": PITCHES[(PITCHES.index(key_root) + 5) % 12],
        "V": PITCHES[(PITCHES.index(key_root) + 7) % 12],
        "vi": PITCHES[(PITCHES.index(key_root) + 9) % 12],
        "vii°": PITCHES[(PITCHES.index(key_root) + 11) % 12]
    }

    for role, note in scale.items():
        if note == chord_root:
            return role

    return "Other"

def functional_role_in_minor(chord_root, chord_quality, key_root):
    # Determine functional role of chord in a minor key
    scale = {
        "i": key_root,
        "ii°": PITCHES[(PITCHES.index(key_root) + 2) % 12],
        "III": PITCHES[(PITCHES.index(key_root) + 3) % 12],
        "iv": PITCHES[(PITCHES.index(key_root) + 5) % 12],
        "v": PITCHES[(PITCHES.index(key_root) + 7) % 12],
        "VI": PITCHES[(PITCHES.index(key_root) + 8) % 12],
        "VII": PITCHES[(PITCHES.index(key_root) + 10) % 12]
    }

    for role, note in scale.items():
        if note == chord_root:
            return role

    return "Other"

def main():
    print("Bayesian Major/Minor Key Detector")
    print("Enter simplified chords like: C, Cm, G, Gm, F, Fm")
    print("Type 'end' to finish.\n")

    major_score = 1.0
    minor_score = 1.0

    while True:
        user = input("Enter chord: ").strip()
        if user.lower() == "end":
            break

        chord_root, chord_quality = parse_chord(user)

        # For each possible major key
        for key in PITCHES:
            role = functional_role_in_major(chord_root, chord_quality, key)
            prob = MAJOR_PROBS.get(role, MAJOR_PROBS["Other"])
            major_score *= prob

        # For each possible minor key
        for key in PITCHES:
            role = functional_role_in_minor(chord_root, chord_quality, key)
            prob = MINOR_PROBS.get(role, MINOR_PROBS["Other"])
            minor_score *= prob

        total = major_score + minor_score
        print("\nP(major) =", major_score / total)
        print("P(minor) =", minor_score / total)

    total = major_score + minor_score
    print("\nFinal probabilities:")
    print("Major:", major_score / total)
    print("Minor:", minor_score / total)

if __name__ == "__main__":
    main()