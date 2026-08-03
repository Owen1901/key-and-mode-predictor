# key-and-mode-predictor
A Python tool that analyzes chord progressions and estimates the most likely key and mode using probability data from HookTheory, Bayesian inference, and computational music‑theory rules.
This program answers the question "Given a set of chords, what key and mode does this progression most likely belong to?"

What makes this project unique:

1. Order‑independent harmonic analysis
   
Most chord‑analysis tools depend heavily on the order of the chords (e.g., ii–V–I vs. I–V–ii). This tool is different: The output depends only on which chords you enter and how many times you enter them, not the order you enter them.
This makes the analysis more stable, more objective, and more focused on harmonic content rather than voice‑leading or functional syntax.

2. Probabilities sourced from HookTheory

The likelihood tables for each mode (major, minor, dorian, phrygian, mixolydian, lydian, locrian) are derived from HookTheory’s TheoryTab database, which aggregates chord‑usage statistics from thousands of real songs.

3. Two powerful modes of operation

A) Interactive Key/Mode Detection

Run interactive_main() and then enter chords one at a time, like:

C
Fm
G#
D#m
Gsus2/E

After each chord, the program updates the posterior probability of all 84 possible keys/modes, including:

C major
A minor
D dorian
F lydian
B locrian
etc.

At the end, it prints:

the full probability distribution
the most likely key/mode
four visualizations (probability bars, parent‑major histograms, negative log‑loss plots)

This gives a rich picture of how your progression “leans” harmonically.

B) Grid Search for Optimal Chord Progressions

Run best_chords_main().

This performs a full grid search over many possible chord combinations to find the progression that maximizes a chosen objective function.

For example, edit the arguments of "target_keys" in the execution of the "grid_search_best_n" function to be ("C major","A minor") and the program will find
which chord progression sounds most like both C major and A minor.

The algorithm:

builds all possible chords
enforces unique pitch classes
computes log‑posterior probabilities
multiplies the probabilities of two target keys
returns the progression that maximizes the product

This is essentially a music‑theory optimization problem powered by Bayesian inference.

