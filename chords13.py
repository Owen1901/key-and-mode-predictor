import math

import chords

PITCHES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

EPS = 1e-6

# -----------------------------
# PROBABILITY TABLES
# -----------------------------

MAJOR_PROBS = {
    "I":   0.18,
    "IV":  0.12,
    "V":   0.12,
    "vi":  0.07,
    "iii": 0.03,
    "ii":  0.03,
    "ii7": 0.03,

    "I7":     0.005,
    "Imaj7":  0.02,

    "vi7": 0.02,
    "V7":  0.02,

    "IV7":     0.001,
    "IVmaj7":  0.02,

    "I6":  0.02,
    "iii7":0.02,
    "v":   0.01,

    "bVIImaj7": 0.001,

    "V6":   0.01,
    "iv":  0.006,
    "V11":  0.005,

    "IVmaj9": 0.003,

    "bIII": 0.004,
    "I9":   0.003,
    "ii6":  0.002,
    "iii6": 0.002,
    "v7":   0.002,

    "bVImaj7": 0.002,

    "V9":   0.001,
    "iv6":  0.001,
    "vi9":  0.001
}

MINOR_PROBS = {
    "i":   0.18,
    "VI":  0.10,
    "VII": 0.10,
    "III": 0.06,
    "iv":  0.05,
    "v":   0.04,
    "V":   0.03,
    "i7":  0.03,

    "VI7":     0.001,
    "VImaj7":  0.03,

    "V7":  0.02,
    "v7":  0.02,
    "IV":  0.01,
    "I":   0.01,
    "i6":  0.01,

    "VII7":     0.005,
    "VIImaj7":  0.005
}

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

    "VIImaj7": 0.006,
    "VII7":    0.002,
    "Imaj7":   0.002,

    "v6":   0.002,
    "II":   0.005,
    "ii7":  0.007
}

DORIAN_PROBS = {
    "i":    0.19,
    "i7":   0.06,
    "III":  0.09,
    "IV":   0.12,
    "v":    0.04,
    "VII":  0.08,
    "I":    0.02,
    "i9":   0.01,
    "ii":   0.02,
    "ii7":  0.01,
    "VII6": 0.007,
    "II":   0.004,

    "IIImaj7": 0.009,

    "i6":   0.01,
    "IV7":  0.02,
    "IV9":  0.004,
    "iv7":  0.002,
    "ii6":  0.004,
    "iv":   0.002,
    "v9":   0.002,
    "v7":   0.01,
    "v11":  0.002,
    "III6": 0.003,

    "bVImaj7": 0.005,

    "bVI":  0.02,
    "IV6":  0.009,

    "VII7":     0.001,
    "VIImaj7":  0.005,

    "v6":   0.003
}

# -----------------------------
# PARSER
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

    if qual in ("", "maj"):
        q = "maj"
    elif qual == "m":
        q = "min"
    elif qual == "7":
        q = "7"
    elif qual == "maj7":
        q = "maj7"
    elif qual == "maj9":
        q = "maj9"
    elif qual == "9":
        q = "9"
    elif qual == "11":
        q = "11"
    elif qual == "6":
        q = "6"
    elif qual == "m7":
        q = "m7"
    elif qual == "m6":
        q = "m6"
    else:
        q = "other"

    return root, q

# -----------------------------
# ROLE MAPPERS
# -----------------------------

def pitch_index(p):
    return PITCHES.index(p)

# MAJOR
def role_in_major(root, qual, key):
    diff = (pitch_index(root) - pitch_index(key)) % 12

    base = {
        0:  "I",
        2:  "ii",
        4:  "iii",
        5:  "IV",
        7:  "V",
        9:  "vi",
        11: "vii"
    }

    borrowed = {
        10: "bVII",
        3:  "bIII",
        8:  "bVI"
    }

    if diff in base:
        deg = base[diff]
    elif diff in borrowed:
        deg = borrowed[diff]
    else:
        return None

    if qual == "maj7":
        return deg + "maj7"
    if qual == "maj9":
        return deg + "maj9"
    if qual == "7":
        return deg + "7"
    if qual == "9":
        return deg + "9"
    if qual == "11":
        return deg + "11"
    if qual == "6":
        return deg + "6"

    if qual == "min":
        if deg == "IV":
            return "iv"
        if deg == "V":
            return "v"

    return deg

# MINOR
def role_in_minor(root, qual, key):
    diff = (pitch_index(root) - pitch_index(key)) % 12

    base = {
        0:  "i",
        2:  "ii",
        3:  "III",
        5:  "iv",
        7:  "v",
        8:  "VI",
        10: "VII"
    }

    borrowed = {
        5: "IV",
        0: "I"
    }

    if diff in base:
        deg = base[diff]
    elif diff in borrowed:
        deg = borrowed[diff]
    else:
        return None

    if qual == "maj7":
        return deg + "maj7"
    if qual == "maj9":
        return deg + "maj9"
    if qual == "7":
        return deg + "7"
    if qual == "9":
        return deg + "9"
    if qual == "11":
        return deg + "11"
    if qual == "6":
        return deg + "6"

    if qual == "min":
        return deg

    return deg

# MIXOLYDIAN
def role_in_mixo(root, qual, key):
    diff = (pitch_index(root) - pitch_index(key)) % 12

    base = {
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

    if diff not in base:
        return None

    deg = base[diff]

    if qual == "maj7":
        return deg + "maj7"
    if qual == "maj9":
        return deg + "maj9"
    if qual == "7":
        return deg + "7"
    if qual == "9":
        return deg + "9"
    if qual == "11":
        return deg + "11"
    if qual == "6":
        return deg + "6"

    return deg

# DORIAN
def role_in_dorian(root, qual, key):
    diff = (pitch_index(root) - pitch_index(key)) % 12

    base = {
        0: "i",
        2: "ii",
        3: "III",
        5: "IV",
        7: "v",
        9: "VI",
        10:"VII",
        8: "bVI"
    }

    if diff not in base:
        return None

    deg = base[diff]

    if qual == "maj7":
        return deg + "maj7"
    if qual == "maj9":
        return deg + "maj9"
    if qual == "7":
        return deg + "7"
    if qual == "9":
        return deg + "9"
    if qual == "11":
        return deg + "11"
    if qual == "6":
        return deg + "6"

    return deg

# -----------------------------
# BORROWED‑CHORD SMOOTHING
# -----------------------------

BORROWED_TAGS = ["bIII","bVI","bVII","iv","v"]

def is_borrowed(role):
    if role is None:
        return False
    for tag in BORROWED_TAGS:
        if role.startswith(tag):
            return True
    return False

def smooth_prob(role, prob_table):
    return prob_table.get(role, EPS)

# -----------------------------
# CIRCLE‑OF‑FIFTHS PRIORS
# -----------------------------

CIRCLE_OF_FIFTHS = ["C","G","D","A","E","B","F#","C#","G#","D#","A#","F"]

def fifth_distance(key_root, center="C"):
    i_key = CIRCLE_OF_FIFTHS.index(key_root)
    i_center = CIRCLE_OF_FIFTHS.index(center)
    d = abs(i_key - i_center)
    return min(d, 12 - d)

def key_prior(key_root, mode):
    return 1.0

# -----------------------------
# CHORD WEIGHTING + CADENCE
# -----------------------------

def chord_weight(index, n_chords, role, prev_role):
    w = 1.0

    #if role in ("I","i","Imaj7","i7"):
        #w *= 1.5

    #if index == n_chords - 1:
        #w *= 1.5

    #if index == 0:
        #w *= 1.5

    #if prev_role is not None:
        #if prev_role.startswith("V") and role in ("I","i"):
            #w *= 2.0
        #if prev_role in ("V7","v7") and role in ("I","i"):
            #w *= 2.0
        #if prev_role.startswith("V") and role in ("vi","VI"):
            #w *= 1.5

    return w

# -----------------------------
# LOG‑LIKELIHOOD
# -----------------------------

def log_likelihood(chords, key_root, mode_name, role_func, prob_table):
    log_score = 0.0
    n = len(chords)
    prev_role = None

    for idx, (root, qual) in enumerate(chords):
        role = role_func(root, qual, key_root)
        p = smooth_prob(role, prob_table)
        w = chord_weight(idx, n, role, prev_role)
        log_score += w * math.log(p)
        prev_role = role

    prior = key_prior(key_root, mode_name)
    log_score += math.log(prior)

    return log_score

# -----------------------------
# NORMALIZATION
# -----------------------------

def normalize_logs(log_dict):
    max_log = max(log_dict.values())
    exps = {k: math.exp(v - max_log) for k, v in log_dict.items()}
    total = sum(exps.values())
    return {k: exps[k] / total for k in exps}

# -----------------------------
# MAIN
# -----------------------------

def main():
    print("Enter chords (C, G7, Am, Cmaj7, etc.). Type 'end' to finish.\n")

    chords = []
    while True:
        s = input("Chord: ").strip()
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

    major_logs = {k: log_likelihood(chords, k, "major", role_in_major, MAJOR_PROBS) for k in PITCHES}
    minor_logs = {k: log_likelihood(chords, k, "minor", role_in_minor, MINOR_PROBS) for k in PITCHES}
    mixo_logs  = {k: log_likelihood(chords, k, "mixolydian", role_in_mixo, MIXO_PROBS) for k in PITCHES}
    dorian_logs= {k: log_likelihood(chords, k, "dorian", role_in_dorian, DORIAN_PROBS) for k in PITCHES}

    major_probs = normalize_logs(major_logs)
    minor_probs = normalize_logs(minor_logs)
    mixo_probs  = normalize_logs(mixo_logs)
    dorian_probs= normalize_logs(dorian_logs)

    sum_major = sum(major_probs.values())
    sum_minor = sum(minor_probs.values())
    sum_mixo  = sum(mixo_probs.values())
    sum_dorian= sum(dorian_probs.values())

    mode_tot = sum_major + sum_minor + sum_mixo + sum_dorian

    p_major  = sum_major  / mode_tot
    p_minor  = sum_minor  / mode_tot
    p_mixo   = sum_mixo   / mode_tot
    p_dorian = sum_dorian / mode_tot

    print("\nMajor keys:")
    for k in PITCHES:
        print(f"{k} major: {major_probs[k]:.4f}")

    print("\nMinor keys:")
    for k in PITCHES:
        print(f"{k} minor: {minor_probs[k]:.4f}")

    print("\nMixolydian keys:")
    for k in PITCHES:
        print(f"{k} mixolydian: {mixo_probs[k]:.4f}")

    print("\nDorian keys:")
    for k in PITCHES:
        print(f"{k} dorian: {dorian_probs[k]:.4f}")

    best_major = max(major_probs.items(), key=lambda x: x[1])
    best_minor = max(minor_probs.items(), key=lambda x: x[1])
    best_mixo  = max(mixo_probs.items(),  key=lambda x: x[1])
    best_dorian= max(dorian_probs.items(), key=lambda x: x[1])

    print("\nMost likely major key:", f"{best_major[0]} major ({best_major[1]:.4f})")
    print("Most likely minor key:", f"{best_minor[0]} minor ({best_minor[1]:.4f})")
    print("Most likely mixolydian key:", f"{best_mixo[0]} mixolydian ({best_mixo[1]:.4f})")
    print("Most likely dorian key:", f"{best_dorian[0]} dorian ({best_dorian[1]:.4f})")

    mode_scores = {
    "major": p_major,
    "minor": p_minor,
    "mixolydian": p_mixo,
    "dorian": p_dorian
    }

    # --- Determine top mode(s) ---
    max_mode_prob = max(mode_scores.values())
    TOL = 1e-6
    top_modes = [m for m, v in mode_scores.items() if abs(v - max_mode_prob) < TOL]


    # --- If tie: choose mode whose best key has highest probability ---
    if len(top_modes) > 1:
        key_strength = {}

        if "major" in top_modes:
            key_strength["major"] = best_major[1]
        if "minor" in top_modes:
            key_strength["minor"] = best_minor[1]
        if "mixolydian" in top_modes:
            key_strength["mixolydian"] = best_mixo[1]
        if "dorian" in top_modes:
            key_strength["dorian"] = best_dorian[1]

        final_mode = max(key_strength.items(), key=lambda x: x[1])[0]

    else:
        final_mode = top_modes[0]

    # --- FUNCTIONAL ROLE PRINTOUT ---
    def print_roles(chords, key_root, role_func):
        print("\nFunctional roles for winning key:")
        for root, qual in chords:
            role = role_func(root, qual, key_root)
            print(f"{root}{qual}: {role}")

    # --- FINAL VERDICT ---
    
    # --- Combine all keys into one dictionary ---
    all_keys = {}

    for k in PITCHES:
        all_keys[("major", k)] = major_probs[k]
        all_keys[("minor", k)] = minor_probs[k]
        all_keys[("mixolydian", k)] = mixo_probs[k]
        all_keys[("dorian", k)] = dorian_probs[k]

    # --- Pick the single strongest key across all modes ---
    (final_mode, final_key), final_prob = max(all_keys.items(), key=lambda x: x[1])

    print("\nFinal verdict:", f"{final_key} {final_mode} ({final_prob:.4f})")

    # --- Functional roles for the winning key ---
    def print_roles(chords, key_root, role_func):
        print("\nFunctional roles for winning key:")
        for root, qual in chords:
            role = role_func(root, qual, key_root)
            print(f"{root}{qual}: {role}")

    role_funcs = {
        "major": role_in_major,
        "minor": role_in_minor,
        "mixolydian": role_in_mixo,
        "dorian": role_in_dorian
    }

    print_roles(chords, final_key, role_funcs[final_mode])


if __name__ == "__main__":
    main()