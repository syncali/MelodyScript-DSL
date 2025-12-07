// Pirates of the Caribbean (He's a Pirate)
// Key: D Minor

// Define timing (tempo is fast)
int t = 140;       // Eighth note (fast pulse)
int q = 280;       // Quarter note
int d = 420;       // Dotted quarter (long)

// Main Theme Loop
repeat(2) {
    
    // --- Phrase 1 ---
    // "Da-da dun-dun-dun-dun..."
    play(A3, t); play(C4, t);
    
    play(D4, q); play(D4, t); play(D4, t); play(E4, t);
    play(F4, q); play(F4, t); play(F4, t); play(G4, t);
    play(E4, q); play(E4, t); play(D4, t); play(C4, t);
    play(D4, q); play(D4, t); // Hold/Link
    
    // --- Phrase 2 ---
    // Similar to Phrase 1
    play(A3, t); play(C4, t);
    
    play(D4, q); play(D4, t); play(D4, t); play(E4, t);
    play(F4, q); play(F4, t); play(F4, t); play(G4, t);
    play(E4, q); play(E4, t); play(D4, t); play(C4, t);
    play(D4, q); play(D4, t); // Hold/Link

    // --- Phrase 3 ---
    // Climbs up: "Dun-dun-dun-dun..."
    play(A3, t); play(C4, t);
    
    play(D4, q); play(D4, t); play(D4, t); play(F4, t);
    play(G4, q); play(G4, t); play(G4, t); play(A4, t);
    play(Bb4, q); play(Bb4, t); play(A4, t); play(G4, t);
    play(A4, d); play(D4, t); // Hold with link to next
    
    // --- Phrase 4 ---
    // Resolution
    play(D4, t); play(E4, t);
    play(F4, q); play(F4, t); play(G4, t); play(A4, t);
    play(D4, q); play(D4, t); play(F4, t); play(E4, t);
    play(F4, q); play(D4, t); play(E4, q);
    
    // Short pause before loop repeats
    rest(q);
}