# bayesian_key_mode_detector.py
# Uses Hooktheory-style functional probabilities (transposition-invariant)
# to detect both key (12 majors + 12 minors) and mode (major vs minor).

PITCHES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

# GIVEN major
MAJOR_PROBS = {
    "I":   0.18,
    "IV":  0.12,
    "V":   0.12,
    "vi":  0.07,
    "IV":  0.12,
    "iv":  0.006,
    "iii": 0.03,
    "ii":  0.03,
    "ii7": 0.03,
    "I7":  0.02,
    "vi7": 0.02,
    "V7":  0.02,
    "IV7": 0.02,
    "I6":  0.02,
    "iii7":0.02,
    "v":   0.01
}

# GIVEN minor
MINOR_PROBS = {
    "i":   0.18,
    "VI":  0.10,
    "VII": 0.10,
    "III": 0.06,
    "iv":  0.05,
    "v":   0.04,
    "V":   0.03,
    "i7":  0.03,
    "VI7": 0.03,
    "V7":  0.02,
    "v7":  0.02,
    "IV":  0.01,
    "I":   0.01,
    "i6":  0.01,
    "VII7": 0.007
}

EPS = 1e-6  # tiny probability for unmapped roles

def pitch_index(p):
    return PITCHES.index(p)

def transpose(root, semitones):
    return PITCHES[(pitch_index(root) + semitones) % 12]

def parse_chord(s):
    s = s.strip()
    root = ""
    i = 0
    if i < len(s) and s[i].upper() in "ABCDEFG":
        root = s[i].upper()
        i += 1
        if i < len(s) and s[i] in "#b":
            root += s[i]
            i += 1
    else:
        return None

    qual = s[i:].lower()

    # classify quality
    if qual == "":
        q = "maj"
    elif qual == "m":
        q = "min"
    elif qual == "7":
        q = "7"
    elif qual == "m7":
        q = "m7"
    elif qual == "maj7":
        q = "7"
    elif qual == "6":
        q = "6"
    elif qual == "m6":
        q = "m6"
    else:
        q = "other"

    return root, q

def major_degree(root, key):
    # major scale degrees (semitones from key)
    intervals = {
        0: "I",
        2: "ii",
        4: "iii",
        5: "IV",
        7: "V",
        9: "vi",
        11:"vii"
    }
    diff = (pitch_index(root) - pitch_index(key)) % 12
    return intervals.get(diff, None)

def minor_degree(root, key):
    # natural minor degrees
    intervals = {
        0: "i",
        2: "ii",
        3: "III",
        5: "iv",
        7: "v",
        8: "VI",
        10:"VII"
    }
    diff = (pitch_index(root) - pitch_index(key)) % 12
    return intervals.get(diff, None)

def role_in_major(root, qual, key):
    deg = major_degree(root, key)
    if deg is None:
        return None

    # handle 7 and 6
    if qual == "7":
        if deg in ("I","V","IV","vi","iii","ii"):
            return deg + "7"
    if qual == "6":
        if deg == "I":
            return "I6"

    # minor qualities inside major (borrowed iv, v)
    if qual == "min":
        if deg == "IV":
            return "iv"
        if deg == "V":
            return "v"

    return deg

def role_in_minor(root, qual, key):
    deg = minor_degree(root, key)
    if deg is None:
        # borrowed IV or I major in minor
        diff = (pitch_index(root) - pitch_index(key)) % 12
        if diff == 5:  # IV
            return "IV"
        if diff == 0:  # I (major tonic in minor)
            return "I"
        return None

    if qual == "7":
        if deg in ("i","VI","V","v"):
            return deg + "7"
    if qual == "6":
        if deg == "i":
            return "i6"

    return deg

def likelihood_major(chords, key):
    score = 1.0
    for root, qual in chords:
        role = role_in_major(root, qual, key)
        if role is None:
            p = EPS
        else:
            p = MAJOR_PROBS.get(role, EPS)
        score *= p
    return score

def likelihood_minor(chords, key):
    score = 1.0
    for root, qual in chords:
        role = role_in_minor(root, qual, key)
        if role is None:
            p = EPS
        else:
            p = MINOR_PROBS.get(role, EPS)
        score *= p
    return score

def main():
    print("Bayesian Key + Mode Detector (Hooktheory-style functional probabilities)")
    print("Enter chords like: C, G, Am, F, Dm, C7, G7, Am7, C6, Cm, etc.")
    print("Type 'end' to finish.\n")

    chords = []
    while True:
        s = input("Enter chord: ").strip()
        if s.lower() == "end":
            break
        parsed = parse_chord(s)
        if parsed is None:
            print("Invalid chord.")
            continue
        chords.append(parsed)

    if not chords:
        print("No chords entered.")
        return

    # compute likelihoods for all 12 major and 12 minor keys
    major_likes = {k: likelihood_major(chords, k) for k in PITCHES}
    minor_likes = {k: likelihood_minor(chords, k) for k in PITCHES}

    sum_major = sum(major_likes.values())
    sum_minor = sum(minor_likes.values())

    # mode probabilities
    p_major_mode = sum_major / (sum_major + sum_minor)
    p_minor_mode = sum_minor / (sum_major + sum_minor)

    print("\nMode probabilities:")
    print(f"Major: {p_major_mode:.4f}")
    print(f"Minor: {p_minor_mode:.4f}")

    # normalize within each mode
    major_probs = {k: v / sum_major for k, v in major_likes.items()}
    minor_probs = {k: v / sum_minor for k, v in minor_likes.items()}

    print("\nMajor key probabilities:")
    for k in PITCHES:
        print(f"{k} major: {major_probs[k]:.4f}")

    print("\nMinor key probabilities:")
    for k in PITCHES:
        print(f"{k} minor: {minor_probs[k]:.4f}")

    best_major = max(major_probs.items(), key=lambda x: x[1])
    best_minor = max(minor_probs.items(), key=lambda x: x[1])

    print("\nMost likely major key:", f"{best_major[0]} major", f"({best_major[1]:.4f})")
    print("Most likely minor key:", f"{best_minor[0]} minor", f"({best_minor[1]:.4f})")

    if p_major_mode >= p_minor_mode:
        print("\nFinal verdict: major mode, key likely", f"{best_major[0]} major")
    else:
        print("\nFinal verdict: minor mode, key likely", f"{best_minor[0]} minor")

if __name__ == "__main__":
    main()
