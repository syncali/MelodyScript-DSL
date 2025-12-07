int bpm = 120;
int beat = 500;
note key = C4;

repeat(4) {
    play(key, beat);
    key = key + 2;
}
