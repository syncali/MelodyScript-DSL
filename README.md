# MelodyScript-DSL

A domain-specific language (DSL) compiler for algorithmic music composition. MelodyScript allows you to write code that generates music, combining procedural programming with music theory primitives.

## Project Overview

MelodyScript is a complete compiler implementation demonstrating all six phases of compilation:

1. **Lexical Analysis** - Tokenizes source code using regex patterns
2. **Syntax Analysis** - Recursive descent parser builds an AST
3. **Semantic Analysis** - Symbol table and type checking
4. **Intermediate Code Generation** - Produces 3-address code (TAC)
5. **Optimization** - Constant folding and dead code elimination
6. **Code Generation** - Transpiles to executable Python using `winsound`

## Language Features

### Data Types

- `int` - For numbers, durations (ms), BPM, loop counters
- `note` - Musical pitch (e.g., `C4`, `F#5`, `Bb3`)
- `string` - For metadata (not fully implemented)

### Built-in Functions

- `play(note, duration)` - Play a note for specified milliseconds
- `rest(duration)` - Pause for specified milliseconds

### Control Structures

- `repeat(n) { ... }` - Loop n times
- `if (condition) { ... } else { ... }` - Conditional execution

### Operators

- Arithmetic: `+`, `-`, `*`, `/`
- Comparison: `>`, `<`, `==`
- Note transposition: `note + int` shifts pitch (adds to frequency)

## Project Structure

```
MelodyScript-DSL/
├── main.py              # CLI entry point
├── grammar.txt          # EBNF grammar specification
├── src/
│   ├── tokens.py        # Token types and Token class
│   ├── lexer.py         # Tokenizer (Phase 1)
│   ├── ast_nodes.py     # AST node definitions
│   ├── parser.py        # Recursive descent parser (Phase 2)
│   ├── semantic.py      # Symbol table & type checking (Phase 3)
│   ├── icg.py           # Intermediate code generator (Phase 4)
│   ├── optimizer.py     # Constant folding & DCE (Phase 5)
│   ├── codegen.py       # Python code generator (Phase 6)
│   └── errors.py        # CompilerError class
└── examples/
    ├── simple.ms        # Basic note sequence
    ├── loop.ms          # Repeat loop example
    └── conditional.ms   # If/else example
```

## Requirements

- Python 3.7+
- Windows OS (uses `winsound` for audio)

## Usage

### Basic Compilation

```bash
python main.py <source_file.ms>
```

This generates `output.py` in the current directory.

### Specify Output File

```bash
python main.py <source_file.ms> --output <output_file.py>
```

### Compile and Run

```bash
python main.py <source_file.ms> --run
```

This compiles the source and immediately executes the generated Python to play the music.

## Example Programs

### Simple Scale (examples/simple.ms)

```c
int bpm = 120;
int beat = 500;
note key = C4;

play(key, beat);
play(D4, beat);
play(E4, beat);
play(F4, beat);
```

### Loop Example (examples/loop.ms)

```c
int bpm = 120;
int beat = 500;
note key = C4;

repeat(4) {
    play(key, beat);
    key = key + 2;
}
```

### Conditional Example (examples/conditional.ms)

```c
int bpm = 150;
int beat = 400;
note key = A4;

if (bpm > 100) {
    play(key, beat);
    play(key + 4, beat);
} else {
    play(key, beat * 2);
}
```

## Running the Examples

```bash
# Play simple scale
python main.py examples/simple.ms --run

# Play loop example
python main.py examples/loop.ms --run

# Play conditional example
python main.py examples/conditional.ms --run
```

## Compilation Phases Explained

### Phase 1: Lexical Analysis (src/lexer.py)

Converts source text into tokens using regex patterns:

- Keywords: `int`, `note`, `string`, `repeat`, `if`, `else`, `play`, `rest`
- Literals: Numbers (`[0-9]+`), Notes (`[A-G][#b]?[0-9]`)
- Operators and punctuation

### Phase 2: Syntax Analysis (src/parser.py)

Recursive descent parser validates grammar and builds AST:

- Expression parsing with operator precedence
- Statement parsing (declarations, assignments, function calls)
- Control flow parsing (if/else, repeat loops)

### Phase 3: Semantic Analysis (src/semantic.py)

Validates program logic:

- Symbol table tracks variable declarations and types
- Type checking ensures type safety
- Scope management for blocks

### Phase 4: Intermediate Code Generation (src/icg.py)

Converts AST to 3-address code (quadruples):

- Format: `(operator, arg1, arg2, result)`
- Note literals converted to frequencies
- Labels and jumps for control flow

### Phase 5: Optimization (src/optimizer.py)

Improves generated code:

- Constant folding: Pre-calculates `60000 / 120` → `500`
- Dead code elimination: Removes unreachable code

### Phase 6: Code Generation (src/codegen.py)

Produces executable Python:

- Emits TAC as data structure
- Runtime interpreter executes instructions
- Uses `winsound.Beep()` for audio output

## Note Frequency Reference

| Note | Frequency (Hz) |
| ---- | -------------- |
| C4   | 262            |
| D4   | 294            |
| E4   | 330            |
| F4   | 349            |
| G4   | 392            |
| A4   | 440            |
| B4   | 494            |
| C5   | 523            |

Supports octaves 0-8 with sharps (#) and flats (b).

## License

MIT License - See LICENSE file for details.
