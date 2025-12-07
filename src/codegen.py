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
    runtime = """label_positions = {}
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
            winsound.Beep(int(freq), int(dur))
            params.clear()
        elif a1 == 'rest':
            dur = params[-1]
            time.sleep(int(dur) / 1000)
            params.clear()
    elif op == 'jumpt':
        if value(a1) != 0:
            pc = label_positions[a2]
            continue
    elif op == 'jump':
        pc = label_positions[a1]
        continue
    pc += 1
"""
    content_lines = [
        "import winsound",
        "import time",
        body,
        runtime,
    ]
    Path(output_path).write_text("\n\n".join(content_lines), encoding="utf-8")
    return output_path
