from src.ast_nodes import AssignmentNode, BinOpNode, IdentifierNode, NoteNode, NumberNode, VarDeclNode
from src.errors import CompilerError
from src.tokens import TokenType


def is_add_op(token_type):
    return token_type in {TokenType.PLUS, TokenType.MINUS}


def is_mul_op(token_type):
    return token_type in {TokenType.MULT, TokenType.DIV}


type_tokens = {TokenType.INT_KW, TokenType.NOTE_KW, TokenType.STRING_KW}


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def current(self):
        return self.tokens[self.index]

    def advance(self):
        if self.index < len(self.tokens) - 1:
            self.index += 1
        return self.current()

    def expect(self, token_type):
        token = self.current()
        if token.type != token_type:
            raise CompilerError(token.line, f"Expected {token_type.name} but found {token.type.name}")
        self.advance()
        return token

    def parse_program(self):
        statements = []
        while self.current().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self.current()
        if token.type in type_tokens:
            return self.parse_declaration()
        if token.type == TokenType.ID:
            next_type = self.tokens[self.index + 1].type if self.index + 1 < len(self.tokens) else None
            if next_type == TokenType.ASSIGN:
                return self.parse_assignment()
        raise CompilerError(token.line, f"Unexpected token {token.type.name}")

    def parse_declaration(self):
        type_token = self.current()
        self.advance()
        name_token = self.expect(TokenType.ID)
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMI)
        return VarDeclNode(type_token.type, name_token.value, value)

    def parse_assignment(self):
        name_token = self.expect(TokenType.ID)
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMI)
        return AssignmentNode(name_token.value, value)

    def parse_expression(self):
        node = self.parse_term()
        while is_add_op(self.current().type):
            op = self.current().type
            self.advance()
            right = self.parse_term()
            node = BinOpNode(node, op, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while is_mul_op(self.current().type):
            op = self.current().type
            self.advance()
            right = self.parse_factor()
            node = BinOpNode(node, op, right)
        return node

    def parse_factor(self):
        token = self.current()
        if token.type == TokenType.NUM:
            self.advance()
            return NumberNode(int(token.value))
        if token.type == TokenType.ID:
            self.advance()
            return IdentifierNode(token.value)
        if token.type == TokenType.NOTE_VAL:
            self.advance()
            return NoteNode(token.value)
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        raise CompilerError(token.line, f"Unexpected token {token.type.name}")
