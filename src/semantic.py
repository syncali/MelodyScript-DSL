from src.ast_nodes import (
    AssignmentNode, BinOpNode, BlockNode, CompareNode, FunctionCallNode,
    IdentifierNode, IfNode, NoteNode, NumberNode, ProgramNode,
    RepeatNode, RestNode, VarDeclNode
)
from src.errors import CompilerError
from src.tokens import TokenType


class SymbolTable:
    
    def __init__(self):
        self.scopes = [{}] 
    
    def push_scope(self):
        self.scopes.append({})
    
    def pop_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
    
    def declare(self, name, type_name):
        current_scope = self.scopes[-1]
        if name in current_scope:
            raise CompilerError(0, f"Variable '{name}' already declared in this scope")
        current_scope[name] = type_name
    
    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise CompilerError(0, f"Variable '{name}' not declared")
    
    def is_declared(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return True
        return False


class SemanticAnalyzer:
    
    def __init__(self):
        self.symbol_table = SymbolTable()
    
    def analyze(self, program):
        self.visit(program)
        return program
    
    def visit(self, node):
        method_name = f"visit_{node.__class__.__name__}"
        method = getattr(self, method_name, None)
        if method is None:
            raise CompilerError(0, f"No visit method for {node.__class__.__name__}")
        return method(node)
    
    def visit_ProgramNode(self, node):
        for statement in node.statements:
            self.visit(statement)
    
    def visit_VarDeclNode(self, node):
        type_map = {
            TokenType.INT_KW: "int",
            TokenType.NOTE_KW: "note",
            TokenType.STRING_KW: "string"
        }
        type_name = type_map.get(node.var_type)
        
        if not type_name:
            raise CompilerError(0, f"Unknown type: {node.var_type}")
        
        expr_type = self.visit(node.value)
        
        if type_name != expr_type:
            raise CompilerError(0, f"Type mismatch: expected {type_name}, got {expr_type}")
        
        self.symbol_table.declare(node.name, type_name)
    
    def visit_AssignmentNode(self, node):
        if not self.symbol_table.is_declared(node.name):
            raise CompilerError(0, f"Variable '{node.name}' not declared")
        
        var_type = self.symbol_table.lookup(node.name)
        expr_type = self.visit(node.value)
        
        if var_type != expr_type:
            raise CompilerError(0, f"Type mismatch in assignment to '{node.name}': expected {var_type}, got {expr_type}")
    
    def visit_NumberNode(self, node):
        return "int"
    
    def visit_NoteNode(self, node):
        return "note"
    
    def visit_IdentifierNode(self, node):
        if not self.symbol_table.is_declared(node.name):
            raise CompilerError(0, f"Variable '{node.name}' not declared")
        return self.symbol_table.lookup(node.name)
    
    def visit_BinOpNode(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        if node.operator in {TokenType.PLUS, TokenType.MINUS, TokenType.MULT, TokenType.DIV}:
            if left_type == "int" and right_type == "int":
                return "int"
            elif left_type == "note" and right_type == "int" and node.operator in {TokenType.PLUS, TokenType.MINUS}:
                return "note"
            else:
                raise CompilerError(0, f"Type mismatch in operation: {left_type} {node.operator.name} {right_type}")
        
        return left_type
    
    def visit_CompareNode(self, node):
        self.visit(node.left)
        self.visit(node.right)
        return "int"
    
    def visit_FunctionCallNode(self, node):
        if node.name == "play":
            if len(node.args) != 2:
                raise CompilerError(0, f"play() expects 2 arguments, got {len(node.args)}")
            
            note_type = self.visit(node.args[0])
            duration_type = self.visit(node.args[1])
            
            if note_type != "note":
                raise CompilerError(0, f"play() first argument must be note, got {note_type}")
            if duration_type != "int":
                raise CompilerError(0, f"play() second argument must be int, got {duration_type}")
        
        elif node.name == "rest":
            if len(node.args) != 1:
                raise CompilerError(0, f"rest() expects 1 argument, got {len(node.args)}")
            
            duration_type = self.visit(node.args[0])
            if duration_type != "int":
                raise CompilerError(0, f"rest() argument must be int, got {duration_type}")
        
        else:
            raise CompilerError(0, f"Unknown function: {node.name}")
    
    def visit_RepeatNode(self, node):
        times_type = self.visit(node.times)
        if times_type != "int":
            raise CompilerError(0, f"repeat() expects int, got {times_type}")
        
        self.symbol_table.push_scope()
        self.visit(node.block)
        self.symbol_table.pop_scope()
    
    def visit_IfNode(self, node):
        self.visit(node.condition)
        
        self.symbol_table.push_scope()
        self.visit(node.then_block)
        self.symbol_table.pop_scope()
        
        if node.else_block:
            self.symbol_table.push_scope()
            self.visit(node.else_block)
            self.symbol_table.pop_scope()
    
    def visit_BlockNode(self, node):
        for statement in node.statements:
            self.visit(statement)
