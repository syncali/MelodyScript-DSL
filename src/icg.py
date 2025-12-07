from src.ast_nodes import (
    AssignmentNode, BinOpNode, BlockNode, CompareNode, FunctionCallNode,
    IdentifierNode, IfNode, NoteNode, NumberNode, ProgramNode, RepeatNode,
    RestNode, VarDeclNode
)
from src.errors import CompilerError
from src.tokens import TokenType


NOTE_FREQS = {
    "C0": 16, "C#0": 17, "Db0": 17, "D0": 18, "D#0": 19, "Eb0": 19,
    "E0": 21, "F0": 22, "F#0": 23, "Gb0": 23, "G0": 25, "G#0": 26,
    "Ab0": 26, "A0": 27, "A#0": 29, "Bb0": 29, "B0": 31,
    
    "C1": 33, "C#1": 35, "Db1": 35, "D1": 37, "D#1": 39, "Eb1": 39,
    "E1": 41, "F1": 44, "F#1": 46, "Gb1": 46, "G1": 49, "G#1": 52,
    "Ab1": 52, "A1": 55, "A#1": 58, "Bb1": 58, "B1": 62,
    
    "C2": 65, "C#2": 69, "Db2": 69, "D2": 73, "D#2": 78, "Eb2": 78,
    "E2": 82, "F2": 87, "F#2": 93, "Gb2": 93, "G2": 98, "G#2": 104,
    "Ab2": 104, "A2": 110, "A#2": 117, "Bb2": 117, "B2": 123,
    
    "C3": 131, "C#3": 139, "Db3": 139, "D3": 147, "D#3": 156, "Eb3": 156,
    "E3": 165, "F3": 175, "F#3": 185, "Gb3": 185, "G3": 196, "G#3": 208,
    "Ab3": 208, "A3": 220, "A#3": 233, "Bb3": 233, "B3": 247,
    
    "C4": 262, "C#4": 277, "Db4": 277, "D4": 294, "D#4": 311, "Eb4": 311,
    "E4": 330, "F4": 349, "F#4": 370, "Gb4": 370, "G4": 392, "G#4": 415,
    "Ab4": 415, "A4": 440, "A#4": 466, "Bb4": 466, "B4": 494,
    
    "C5": 523, "C#5": 554, "Db5": 554, "D5": 587, "D#5": 622, "Eb5": 622,
    "E5": 659, "F5": 698, "F#5": 740, "Gb5": 740, "G5": 784, "G#5": 831,
    "Ab5": 831, "A5": 880, "A#5": 932, "Bb5": 932, "B5": 988,
    
    "C6": 1047, "C#6": 1109, "Db6": 1109, "D6": 1175, "D#6": 1245, "Eb6": 1245,
    "E6": 1319, "F6": 1397, "F#6": 1480, "Gb6": 1480, "G6": 1568, "G#6": 1661,
    "Ab6": 1661, "A6": 1760, "A#6": 1865, "Bb6": 1865, "B6": 1976,
    
    "C7": 2093, "C#7": 2217, "Db7": 2217, "D7": 2349, "D#7": 2489, "Eb7": 2489,
    "E7": 2637, "F7": 2794, "F#7": 2960, "Gb7": 2960, "G7": 3136, "G#7": 3322,
    "Ab7": 3322, "A7": 3520, "A#7": 3729, "Bb7": 3729, "B7": 3951,
    
    "C8": 4186, "C#8": 4435, "Db8": 4435, "D8": 4699, "D#8": 4978, "Eb8": 4978,
    "E8": 5274, "F8": 5588, "F#8": 5920, "Gb8": 5920, "G8": 6272, "G#8": 6645,
    "Ab8": 6645, "A8": 7040, "A#8": 7459, "Bb8": 7459, "B8": 7902,
}


class Quadruple:
    
    def __init__(self, op, arg1, arg2, result):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
    
    def __repr__(self):
        return f"({self.op}, {self.arg1}, {self.arg2}, {self.result})"


class ICGenerator:
    
    def __init__(self):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"
    
    def new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"
    
    def emit(self, op, arg1=None, arg2=None, result=None):
        self.code.append(Quadruple(op, arg1, arg2, result))
    
    def generate(self, program):
        self.visit(program)
        return self.code
    
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
        value_result = self.visit(node.value)
        
        self.emit('=', value_result, None, node.name)
    
    def visit_AssignmentNode(self, node):
        value_result = self.visit(node.value)
        self.emit('=', value_result, None, node.name)
    
    def visit_NumberNode(self, node):
        return str(node.value)
    
    def visit_NoteNode(self, node):
        note_name = node.name
        if note_name not in NOTE_FREQS:
            raise CompilerError(0, f"Unknown note: {node.name}")
        
        frequency = NOTE_FREQS[note_name]
        return str(frequency)
    
    def visit_IdentifierNode(self, node):
        return node.name
    
    def visit_BinOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        result = self.new_temp()
        
        op_map = {
            TokenType.PLUS: '+',
            TokenType.MINUS: '-',
            TokenType.MULT: '*',
            TokenType.DIV: '/',
        }
        
        op = op_map.get(node.operator)
        if not op:
            raise CompilerError(0, "Unsupported binary operator")
        self.emit(op, left, right, result)
        return result
    
    def visit_CompareNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        result = self.new_temp()
        
        op_map = {
            TokenType.GT: '>',
            TokenType.LT: '<',
            TokenType.EQUALS: '==',
        }
        
        op = op_map.get(node.operator)
        if not op:
            raise CompilerError(0, "Unsupported compare operator")
        self.emit(op, left, right, result)
        return result
    
    def visit_FunctionCallNode(self, node):
        if node.name == "play":
            note = self.visit(node.args[0])
            duration = self.visit(node.args[1])
            
            self.emit('PARAM', note, None, None)
            self.emit('PARAM', duration, None, None)
            self.emit('CALL', 'play', '2', None)
        
        elif node.name == "rest":
            duration = self.visit(node.args[0])
            
            self.emit('PARAM', duration, None, None)
            self.emit('CALL', 'rest', '1', None)
    
    def visit_RepeatNode(self, node):
        times = self.visit(node.times)
        
        loop_counter = self.new_temp()
        self.emit('=', '0', None, loop_counter)
        
        loop_start = self.new_label()
        loop_body = self.new_label()
        loop_end = self.new_label()
        
        self.emit('label', loop_start, None, None)
        
        condition = self.new_temp()
        self.emit('<', loop_counter, times, condition)
        self.emit('jumpt', condition, loop_body, None)
        self.emit('jump', loop_end, None, None)
        
        self.emit('label', loop_body, None, None)
        self.visit(node.block)
        
        next_val = self.new_temp()
        self.emit('+', loop_counter, '1', next_val)
        self.emit('=', next_val, None, loop_counter)
        
        self.emit('jump', loop_start, None, None)
        
        self.emit('label', loop_end, None, None)
    
    def visit_IfNode(self, node):
        condition = self.visit(node.condition)
        
        then_label = self.new_label()
        else_label = self.new_label() if node.else_block else None
        end_label = self.new_label()
        
        self.emit('jumpt', condition, then_label, None)
        
        if node.else_block:
            self.emit('jump', else_label, None, None)
        else:
            self.emit('jump', end_label, None, None)
        
        self.emit('label', then_label, None, None)
        self.visit(node.then_block)
        self.emit('jump', end_label, None, None)
        
        if node.else_block:
            self.emit('label', else_label, None, None)
            self.visit(node.else_block)
            self.emit('jump', end_label, None, None)
        
        self.emit('label', end_label, None, None)
    
    def visit_BlockNode(self, node):
        for statement in node.statements:
            self.visit(statement)
