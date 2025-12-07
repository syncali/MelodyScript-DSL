// Harry Potter Theme (Hedwig's Theme)
// Key: E Minor

int s = 250;   // Short (Eighth note)
int q = 375;   // Dotted Eighth (approx)
int l = 750;   // Long (Dotted Quarter)
int xl = 1000; // Extra Long

// Pickup note
play(B3, s);

// --- Section A ---
repeat(1) {
    // phrase 1: E G F#
    play(E4, l);
    play(G4, s);
    play(F#4, s);
    
    // phrase 2: E B A
    play(E4, l);
    play(B4, s);
    play(A4, xl);
    
    // phrase 3: F#
    play(F#4, l);
    
    // phrase 4: E G F#
    play(E4, l);
    play(G4, s);
    play(F#4, s);
    
    // phrase 5: D# F B
    play(D#4, l);
    play(F4, s);
    play(B3, xl);
}

rest(s);

// --- Section B ---
repeat(1) {
    play(B3, s);

    // phrase 6: E G F#
    play(E4, l);
    play(G4, s);
    play(F#4, s);
    
    // phrase 7: E B D C#
    play(E4, l);
    play(B4, s);
    play(D5, l);
    play(C#5, s);
    play(C5, l);
    
    // phrase 8: G# C B A#
    play(G#4, s);
    play(C5, l);
    play(B4, s);
    play(A#4, s);
    
    // phrase 9: Bb G E
    play(Bb4, l);
    play(G4, s);
    play(E4, l);
}