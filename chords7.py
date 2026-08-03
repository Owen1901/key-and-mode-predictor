# weighted_functional_major_minor_detector.py
# Implements your weighted functional scoring system:
# - User enters simplified chords (C, Cm, G, Gm, etc.)
# - Weighted scoring:
#     tonic = 1.0
#     dominant = 0.7
#     subdominant = 0.5
#     relative = 0.3
# - Probability distribution across 24 keys
# - Tie-handling: print all tied keys

PITCHES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

TONIC_W = 1.0
DOM_W = 0.8
SUB_W = 0.5
REL_W = 0.25

def fifth_above(root):
    idx = PITCHES.index(root)
    return PITCHES[(idx + 7) % 12]

def fifth_below(root):
    idx = PITCHES.index(root)
    return PITCHES[(idx - 7) % 12]

def relative_minor(root):
    idx = PITCHES.index(root)
    return PITCHES[(idx + 9) % 12]  # major → minor

def relative_major(root):
    idx = PITCHES.index(root)
    return PITCHES[(idx + 3) % 12]  # minor → major

def parse_chord(s):
    s = s.strip()
    if s.endswith("m"):
        root = s[:-1]
        quality = "minor"
    else:
        root = s
        quality = "major"

    if root not in PITCHES:
        return None

    return root, quality

def main():
    print("Weighted Functional Major/Minor Key Detector")
    print("Enter simplified chords like: C, Cm, G, Gm, F, Fm")
    print("Type 'end' to finish.\n")

    # 24 keys: 12 major + 12 minor
    scores = {root + " major": 0.0 for root in PITCHES}
    scores.update({root + " minor": 0.0 for root in PITCHES})

    while True:
        user = input("Enter chord: ").strip()
        if user.lower() == "end":
            break

        parsed = parse_chord(user)
        if parsed is None:
            print("Invalid chord.")
            continue

        root, quality = parsed

        if quality == "major":
            tonic = root + " major"
            subdom = fifth_below(root) + " major"
            dom = fifth_above(root) + " major"
            relmin = relative_minor(root) + " minor"

            scores[tonic] += TONIC_W
            scores[subdom] += SUB_W
            scores[dom] += DOM_W
            scores[relmin] += REL_W

        else:  # minor chord
            tonic = root + " minor"
            subdom = fifth_below(root) + " minor"
            dom = fifth_above(root) + " minor"
            relmaj = relative_major(root) + " major"

            scores[tonic] += TONIC_W
            scores[subdom] += SUB_W
            scores[dom] += DOM_W
            scores[relmaj] += REL_W

        # Print probabilities after each chord
        total = sum(scores.values())
        print("\nProbabilities:")
        for key in scores:
            print(f"{key}: {scores[key] / total:.4f}")

    # Final probabilities
    total = sum(scores.values())
    probs = {k: scores[k] / total for k in scores}

    max_prob = max(probs.values())
    tied = [k for k, p in probs.items() if abs(p - max_prob) < 1e-12]

    print("\nFinal tied keys:")
    for k in tied:
        print(k)

if __name__ == "__main__":
    main()