import argparse
import os
import sys
from pathlib import Path

from src.codegen import generate
from src.errors import CompilerError
from src.icg import ICGenerator
from src.lexer import tokenize
from src.optimizer import optimize
from src.parser import Parser
from src.semantic import SemanticAnalyzer


def read_source(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise CompilerError(0, f"File not found: {path}")


def run_pipeline(source_path, output_path, run_flag):
    source = read_source(source_path)
    tokens = tokenize(source)
    parser = Parser(tokens)
    program = parser.parse_program()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(program)
    icg = ICGenerator()
    code = icg.generate(program)
    optimized = optimize(code)
    generate(optimized, output_path)
    if run_flag:
        os.system(f"python {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", nargs="?", default="input.ms")
    parser.add_argument("--output", default="output.py")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    run_pipeline(args.source, args.output, args.run)


if __name__ == "__main__":
    try:
        main()
    except CompilerError as err:
        print(err)
        sys.exit(1)

