// Interstellar - Cornfield Chase (Main Theme)
// Hans Zimmer

int t = 180; 

repeat(4) {
    // Chord 1: A Minor (Root A)
    // Pattern: Bass A -> E A E A...
    repeat(2) {
        play(A3, t);
        play(E4, t);
        play(A4, t);
        play(E4, t);
        play(A3, t);
        play(E4, t);
        play(A4, t);
        play(E4, t);
    }

    // Chord 2: F Major (Root F)
    // Pattern: Bass F -> E A E A... (creating F Maj7 sound)
    repeat(2) {
        play(F3, t);
        play(E4, t);
        play(A4, t);
        play(E4, t);
        play(F3, t);
        play(E4, t);
        play(A4, t);
        play(E4, t);
    }

    // Chord 3: D Minor (Root D)
    // Pattern: Bass D -> E A E A... (creating Dm9 sound)
    repeat(2) {
        play(D3, t);
        play(E4, t);
        play(A4, t);
        play(E4, t);
        play(D3, t);
        play(E4, t);
        play(A4, t);
        play(E4, t);
    }

    // Chord 4: E Major (Root E)
    // Pattern: Bass E -> E B E B... (Resolution)
    repeat(2) {
        play(E3, t);
        play(E4, t);
        play(B4, t);
        play(E4, t);
        play(E3, t);
        play(E4, t);
        play(B4, t);
        play(E4, t);
    }
}

// Final Chord to finish
play(A3, 800);