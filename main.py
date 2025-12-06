from pathlib import Path
import sys

from src.errors import CompilerError


def read_source(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise CompilerError(0, f"File not found: {path}")


def main():
    source_path = sys.argv[1] if len(sys.argv) > 1 else "input.ms"
    source = read_source(source_path)
    print(f"Read {len(source)} characters from {source_path}")


if __name__ == "__main__":
    try:
        main()
    except CompilerError as err:
        print(err)
        sys.exit(1)

