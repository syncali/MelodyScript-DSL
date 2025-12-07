int bpm = 150;
int beat = 400;
note key = A4;

if (bpm > 100) {
    play(key, beat);
    play(key + 4, beat);
} else {
    play(key, beat * 2);
}
