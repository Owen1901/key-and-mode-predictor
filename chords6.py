# functional_major_minor_detector.py
# Implements EXACTLY your new idea:
# - User enters simplified chords (C, Cm, G, Gm, etc.)
# - Uniform weights
# - Major chord → C, F, G major + A minor
# - Minor chord → Cm, Fm, Gm + Eb major (relative major)
# - Probability distribution across 24 keys
# - Tie-handling: print all tied keys

PITCHES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

def fifth_above(root):
    idx = PITCHES.index(root)
    return PITCHES[(idx + 7) % 12]

def fifth_below(root):
    idx = PITCHES.index(root)
    return PITCHES[(idx - 7) % 12]

def relative_minor(root):
    idx = PITCHES.index(root)
    return PITCHES[(idx + 9) % 12]  # major → minor: down a minor third

def relative_major(root):
    idx = PITCHES.index(root)
    return PITCHES[(idx + 3) % 12]  # minor → major: up a minor third

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
    print("Functional Major/Minor Key Detector")
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

            scores[tonic] += 1
            scores[subdom] += 1
            scores[dom] += 1
            scores[relmin] += 1

        else:  # minor chord
            tonic = root + " minor"
            subdom = fifth_below(root) + " minor"
            dom = fifth_above(root) + " minor"
            relmaj = relative_major(root) + " major"

            scores[tonic] += 1
            scores[subdom] += 1
            scores[dom] += 1
            scores[relmaj] += 1

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