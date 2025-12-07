from pathlib import Path

def render_instructions(code):
    lines = ["instructions = ["]
    for quad in code:
        op = repr(quad.op)
        a1 = repr(quad.arg1)
        a2 = repr(quad.arg2)
        res = repr(quad.result)
        lines.append(f"    ({op}, {a1}, {a2}, {res}),")
    lines.append("]")
    return "\n".join(lines)


def generate(code, output_path="output.py"):
    body = render_instructions(code)
    runtime = """
# Initialize Pygame Mixer
# 44.1kHz, 16-bit signed, 2 channels (Stereo), 512 buffer size
# We use 2 channels because some Windows drivers force stereo, rejecting mono arrays.
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

label_positions = {}
for i, ins in enumerate(instructions):
    if ins[0] == 'label':
        label_positions[ins[1]] = i

env = {}
params = []
pc = 0


def value(x):
    if x is None:
        return None
    if isinstance(x, int):
        return x
    if isinstance(x, str) and x.lstrip('-').isdigit():
        return int(x)
    return env.get(x, 0)

def generate_tone(freq, duration_ms):
    sample_rate = 44100
    # Generate time points
    n_samples = int(sample_rate * (duration_ms / 1000.0))
    t = np.linspace(0, duration_ms / 1000.0, n_samples, False)
    
    # Generate Sine Wave
    # 4096 is the amplitude (volume)
    wave = np.sin(2 * np.pi * freq * t) * 4096
    wave = wave.astype(np.int16)
    
    # Create Stereo Array (Copy mono wave to both Left and Right channels)
    # This creates a 2D array [[L, R], [L, R], ...]
    return np.column_stack((wave, wave))

while pc < len(instructions):
    op, a1, a2, res = instructions[pc]
    
    if op == 'label':
        pc += 1
        continue
        
    if op == '=':
        env[res] = value(a1)

    elif op in ('+', '-', '*', '/'):
        v1 = value(a1)
        v2 = value(a2)
        if op == '+':
            env[res] = v1 + v2
        elif op == '-':
            env[res] = v1 - v2
        elif op == '*':
            env[res] = v1 * v2
        else:
            if v2 == 0: v2 = 1 # Safety
            env[res] = v1 // v2
    elif op in ('>', '<', '=='):
        v1 = value(a1)
        v2 = value(a2)
        if op == '>':
            env[res] = 1 if v1 > v2 else 0
        elif op == '<':
            env[res] = 1 if v1 < v2 else 0
        else:
            env[res] = 1 if v1 == v2 else 0
            
    elif op == 'PARAM':
        params.append(value(a1))
        
    elif op == 'CALL':
        if a1 == 'play':
            freq = params[-2]
            dur = params[-1]
            
            # Create and play sound
            if freq > 0:
                tone = generate_tone(freq, dur)
                sound = pygame.sndarray.make_sound(tone)
                sound.play()
            
            # Wait for duration (blocking program flow to keep rhythm)
            pygame.time.wait(int(dur))
            params.clear()
            
        elif a1 == 'rest':
            dur = params[-1]
            pygame.time.wait(int(dur))
            params.clear()
            
    elif op == 'jumpt':
        if value(a1) != 0:
            pc = label_positions[a2]
            continue

    elif op == 'jump':
        pc = label_positions[a1]
        continue
        
    pc += 1

pygame.quit()
"""
    content_lines = [
        "import pygame",
        "import numpy as np",
        "import time",
        body,
        runtime,
    ]
    Path(output_path).write_text("\n\n".join(content_lines), encoding="utf-8")
    return output_path