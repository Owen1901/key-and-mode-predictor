# bayesian_key_mode_detector_full.py
# Major, Minor, Mixolydian Bayesian key + mode detector
# Using transposition-invariant Hooktheory-style functional probabilities.

PITCHES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

# -----------------------------
# GIVEN major (corrected)
# -----------------------------
MAJOR_PROBS = {
    "I":   0.18,
    "IV":  0.12,
    "V":   0.12,
    "vi":  0.07,
    "iii": 0.03,
    "ii":  0.03,
    "ii7": 0.03,
    "I7":  0.02,
    "vi7": 0.02,
    "V7":  0.02,
    "IV7": 0.02,
    "I6":  0.02,
    "iii7":0.02,
    "v":   0.01,
    "iv":  0.006   # corrected
}

# -----------------------------
# GIVEN minor
# -----------------------------
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
    "i6":  0.01
}

# -----------------------------
# GIVEN mixolydian
# -----------------------------
MIXO_PROBS = {
    "I":    0.26,
    "I7":   0.03,
    "bIII": 0.03,
    "IV":   0.11,
    "v":    0.03,
    "VII":  0.14,
    "I11":  0.01,
    "ii":   0.02,
    "I6":   0.01,
    "V":    0.02,
    "v7":   0.01,
    "bVI":  0.02,
    "vi":   0.02,
    "IV6":  0.01,
    "vi7":  0.008,
    "VII7": 0.006,
    "v6":   0.002,
    "II":   0.005,
    "ii7":  0.007
}

EPS = 1e-6

def pitch_index(p):
    return PITCHES.index(p)

def transpose(root, semitones):
    return PITCHES[(pitch_index(root) + semitones) % 12]

# -----------------------------
# Parsing chord roots + qualities
# -----------------------------
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

# -----------------------------
# Functional roles: major
# -----------------------------
def major_degree(root, key):
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

def role_in_major(root, qual, key):
    deg = major_degree(root, key)
    if deg is None:
        return None

    if qual == "7":
        return deg + "7"
    if qual == "6" and deg == "I":
        return "I6"

    if qual == "min":
        if deg == "IV":
            return "iv"
        if deg == "V":
            return "v"

    return deg

# -----------------------------
# Functional roles: minor
# -----------------------------
def minor_degree(root, key):
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

def role_in_minor(root, qual, key):
    deg = minor_degree(root, key)
    if deg is None:
        diff = (pitch_index(root) - pitch_index(key)) % 12
        if diff == 5:
            return "IV"
        if diff == 0:
            return "I"
        return None

    if qual == "7":
        return deg + "7"
    if qual == "6" and deg == "i":
        return "i6"

    return deg

# -----------------------------
# Functional roles: mixolydian
# -----------------------------
def mixo_degree(root, key):
    intervals = {
        0: "I",
        2: "ii",
        4: "iii",
        5: "IV",
        7: "V",
        9: "vi",
        10:"VII",
        3: "bIII",
        8: "bVI"
    }
    diff = (pitch_index(root) - pitch_index(key)) % 12
    return intervals.get(diff, None)

def role_in_mixo(root, qual, key):
    deg = mixo_degree(root, key)
    if deg is None:
        return None

    if qual == "7":
        return deg + "7"
    if qual == "6":
        if deg == "I":
            return "I6"
        if deg == "v":
            return "v6"

    return deg

# -----------------------------
# Likelihood functions
# -----------------------------
def likelihood(chords, key, role_func, prob_table):
    score = 1.0
    for root, qual in chords:
        role = role_func(root, qual, key)
        p = prob_table.get(role, EPS)
        score *= p
    return score

# -----------------------------
# Main
# -----------------------------
def main():
    print("Bayesian Key + Mode Detector (Major, Minor, Mixolydian)")
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

    major_likes = {k: likelihood(chords, k, role_in_major, MAJOR_PROBS) for k in PITCHES}
    minor_likes = {k: likelihood(chords, k, role_in_minor, MINOR_PROBS) for k in PITCHES}
    mixo_likes  = {k: likelihood(chords, k, role_in_mixo,  MIXO_PROBS)  for k in PITCHES}

    sum_major = sum(major_likes.values())
    sum_minor = sum(minor_likes.values())
    sum_mixo  = sum(mixo_likes.values())

    total = sum_major + sum_minor + sum_mixo

    print("\nMode probabilities:")
    print(f"Major:      {sum_major/total:.4f}")
    print(f"Minor:      {sum_minor/total:.4f}")
    print(f"Mixolydian: {sum_mixo/total:.4f}")

    major_probs = {k: major_likes[k]/sum_major for k in PITCHES}
    minor_probs = {k: minor_likes[k]/sum_minor for k in PITCHES}
    mixo_probs  = {k: mixo_likes[k]/sum_mixo  for k in PITCHES}

    print("\nMajor key probabilities:")
    for k in PITCHES:
        print(f"{k} major: {major_probs[k]:.4f}")

    print("\nMinor key probabilities:")
    for k in PITCHES:
        print(f"{k} minor: {minor_probs[k]:.4f}")

    print("\nMixolydian key probabilities:")
    for k in PITCHES:
        print(f"{k} mixolydian: {mixo_probs[k]:.4f}")

    best_major = max(major_probs.items(), key=lambda x: x[1])
    best_minor = max(minor_probs.items(), key=lambda x: x[1])
    best_mixo  = max(mixo_probs.items(),  key=lambda x: x[1])

    print("\nMost likely major key:", f"{best_major[0]} major ({best_major[1]:.4f})")
    print("Most likely minor key:", f"{best_minor[0]} minor ({best_minor[1]:.4f})")
    print("Most likely mixolydian key:", f"{best_mixo[0]} mixolydian ({best_mixo[1]:.4f})")

    mode_scores = {
        "major": sum_major,
        "minor": sum_minor,
        "mixolydian": sum_mixo
    }
    final_mode = max(mode_scores.items(), key=lambda x: x[1])[0]

    if final_mode == "major":
        print("\nFinal verdict:", f"{best_major[0]} major")
    elif final_mode == "minor":
        print("\nFinal verdict:", f"{best_minor[0]} minor")
    else:
        print("\nFinal verdict:", f"{best_mixo[0]} mixolydian")

if __name__ == "__main__":
    main()