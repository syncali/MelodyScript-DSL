from src.ast_nodes import (
    AssignmentNode, BinOpNode, BlockNode, CompareNode, FunctionCallNode,
    IdentifierNode, IfNode, NoteNode, NumberNode, ProgramNode, RepeatNode,
    RestNode, VarDeclNode
)
from src.errors import CompilerError
from src.tokens import TokenType


def is_add_op(token_type):
    return token_type in {TokenType.PLUS, TokenType.MINUS}


def is_mul_op(token_type):
    return token_type in {TokenType.MULT, TokenType.DIV}


def is_compare_op(token_type):
    return token_type in {TokenType.GT, TokenType.LT, TokenType.EQUALS}


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
        return ProgramNode(statements)

    def parse_statement(self):
        token = self.current()
        
        if token.type in type_tokens:
            return self.parse_declaration()
        
        if token.type == TokenType.ID:
            next_type = self.tokens[self.index + 1].type if self.index + 1 < len(self.tokens) else None
            if next_type == TokenType.ASSIGN:
                return self.parse_assignment()
        
        if token.type == TokenType.REPEAT_KW:
            return self.parse_repeat()
        
        if token.type == TokenType.IF_KW:
            return self.parse_if()
        
        if token.type == TokenType.PLAY_KW:
            return self.parse_function_call("play")
        
        if token.type == TokenType.REST_KW:
            return self.parse_function_call("rest")
        
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

    def parse_function_call(self, func_name):
        if func_name == "play":
            self.expect(TokenType.PLAY_KW)
        elif func_name == "rest":
            self.expect(TokenType.REST_KW)
        
        self.expect(TokenType.LPAREN)
        args = []
        
        if self.current().type != TokenType.RPAREN:
            args.append(self.parse_expression())
            while self.current().type == TokenType.COMMA:
                self.advance()
                args.append(self.parse_expression())
        
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMI)
        return FunctionCallNode(func_name, args)

    def parse_repeat(self):
        self.expect(TokenType.REPEAT_KW)
        self.expect(TokenType.LPAREN)
        times = self.parse_expression()
        self.expect(TokenType.RPAREN)
        block = self.parse_block()
        return RepeatNode(times, block)

    def parse_if(self):
        self.expect(TokenType.IF_KW)
        self.expect(TokenType.LPAREN)
        condition = self.parse_boolean_expression()
        self.expect(TokenType.RPAREN)
        then_block = self.parse_block()
        
        else_block = None
        if self.current().type == TokenType.ELSE_KW:
            self.advance()
            else_block = self.parse_block()
        
        return IfNode(condition, then_block, else_block)

    def parse_block(self):
        self.expect(TokenType.LBRACE)
        statements = []
        while self.current().type != TokenType.RBRACE:
            statements.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        return BlockNode(statements)

    def parse_boolean_expression(self):
        left = self.parse_expression()
        if is_compare_op(self.current().type):
            op = self.current().type
            self.advance()
            right = self.parse_expression()
            return CompareNode(left, op, right)
        raise CompilerError(self.current().line, f"Expected comparison operator")

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
