import re

from src.errors import CompilerError
from src.tokens import TokenType, Token


note_pattern = re.compile(r"[A-G][#b]?[0-9]")
number_pattern = re.compile(r"[0-9]+")
identifier_pattern = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")

keyword_map = {
    "int": TokenType.INT_KW,
    "note": TokenType.NOTE_KW,
    "string": TokenType.STRING_KW,
    "repeat": TokenType.REPEAT_KW,
    "if": TokenType.IF_KW,
    "else": TokenType.ELSE_KW,
    "play": TokenType.PLAY_KW,
    "rest": TokenType.REST_KW,
}


symbol_map = {
    "=": TokenType.ASSIGN,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MULT,
    "/": TokenType.DIV,
    ">": TokenType.GT,
    "<": TokenType.LT,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    ",": TokenType.COMMA,
    ";": TokenType.SEMI,
}


def tokenize(source):
    tokens = []
    length = len(source)
    index = 0
    line = 1
    column = 1
    while index < length:
        ch = source[index]
        if ch == " " or ch == "\t":
            index += 1
            column += 1
            continue
        if ch == "\n":
            index += 1
            line += 1
            column = 1
            continue
        if ch == "/" and index + 1 < length and source[index + 1] == "/":
            while index < length and source[index] != "\n":
                index += 1
                column += 1
            continue
        if source.startswith("==", index):
            tokens.append(Token(TokenType.EQUALS, "==", line, column))
            index += 2
            column += 2
            continue
        if ch in symbol_map:
            token_type = symbol_map[ch]
            tokens.append(Token(token_type, ch, line, column))
            index += 1
            column += 1
            continue
        note_match = note_pattern.match(source, index)
        if note_match:
            value = note_match.group(0)
            tokens.append(Token(TokenType.NOTE_VAL, value, line, column))
            span = len(value)
            index += span
            column += span
            continue
        num_match = number_pattern.match(source, index)
        if num_match:
            value = num_match.group(0)
            tokens.append(Token(TokenType.NUM, value, line, column))
            span = len(value)
            index += span
            column += span
            continue
        id_match = identifier_pattern.match(source, index)
        if id_match:
            value = id_match.group(0)
            token_type = keyword_map.get(value, TokenType.ID)
            tokens.append(Token(token_type, value, line, column))
            span = len(value)
            index += span
            column += span
            continue
        raise CompilerError(line, f"Unexpected character: {ch}")
    tokens.append(Token(TokenType.EOF, "", line, column))
    return tokens
