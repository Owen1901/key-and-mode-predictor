# bayesian_major_minor_detector_clean.py
# Bayesian major/minor mode detector using Hooktheory chord probabilities.
# Cleaned of unused functions, unused parameters, and unused probability entries.

PITCHES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

# Hooktheory chord probabilities (major context)
MAJOR_PROBS = {
    "I": 0.18,
    "ii": 0.03,
    "iii": 0.03,   # using ii7's probability for iii (your original code never used ii7)
    "IV": 0.12,
    "V": 0.12,
    "vi": 0.07,
    "vii°": 0.03,  # your original code never had this, but functional_role_in_major returns it
    "Other": 0.46
}

# Hooktheory chord probabilities (minor context)
MINOR_PROBS = {
    "i": 0.18,
    "ii°": 0.03,
    "III": 0.06,
    "iv": 0.05,
    "v": 0.04,
    "VI": 0.10,
    "VII": 0.10,
    "Other": 0.46
}


def functional_role_in_major(chord_root, key_root):
    # Determine functional role of chord in a major key
    idx = PITCHES.index(key_root)
    scale = {
        "I": key_root,
        "ii": PITCHES[(idx + 2) % 12],
        "iii": PITCHES[(idx + 4) % 12],
        "IV": PITCHES[(idx + 5) % 12],
        "V": PITCHES[(idx + 7) % 12],
        "vi": PITCHES[(idx + 9) % 12],
        "vii°": PITCHES[(idx + 11) % 12]
    }

    for role, note in scale.items():
        if note == chord_root:
            return role

    return "Other"

def functional_role_in_minor(chord_root, key_root):
    # Determine functional role of chord in a minor key
    idx = PITCHES.index(key_root)
    scale = {
        "i": key_root,
        "ii°": PITCHES[(idx + 2) % 12],
        "III": PITCHES[(idx + 3) % 12],
        "iv": PITCHES[(idx + 5) % 12],
        "v": PITCHES[(idx + 7) % 12],
        "VI": PITCHES[(idx + 8) % 12],
        "VII": PITCHES[(idx + 10) % 12]
    }

    for role, note in scale.items():
        if note == chord_root:
            return role

    return "Other"

def main():
    print("Bayesian Major/Minor Key Detector (Clean Version)")
    print("Enter simplified chords like: C, Cm, G, Gm, F, Fm")
    print("Type 'end' to finish.\n")

    major_score = 1.0
    minor_score = 1.0

    while True:
        user = input("Enter chord: ").strip()
        if user.lower() == "end":
            break

        chord_root = user.strip()

        # Update major likelihood
        for key in PITCHES:
            role = functional_role_in_major(chord_root, key)
            major_score *= MAJOR_PROBS.get(role, MAJOR_PROBS["Other"])

        # Update minor likelihood
        for key in PITCHES:
            role = functional_role_in_minor(chord_root, key)
            minor_score *= MINOR_PROBS.get(role, MINOR_PROBS["Other"])

        total = major_score + minor_score
        print("\nP(major) =", major_score / total)
        print("P(minor) =", minor_score / total)

    total = major_score + minor_score
    print("\nFinal probabilities:")
    print("Major:", major_score / total)
    print("Minor:", minor_score / total)

if __name__ == "__main__":
    main()