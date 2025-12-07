from src.errors import CompilerError


def is_int_literal(value):
    if value is None:
        return False
    if isinstance(value, int):
        return True
    if isinstance(value, str) and value.lstrip("-").isdigit():
        return True
    return False


def to_int(value):
    if isinstance(value, int):
        return value
    return int(value)


def constant_fold(code):
    new_code = []
    for quad in code:
        op, a1, a2, res = quad.op, quad.arg1, quad.arg2, quad.result
        if op in {"+", "-", "*", "/"}:
            if is_int_literal(a1) and is_int_literal(a2):
                v1 = to_int(a1)
                v2 = to_int(a2)
                if op == "+":
                    val = v1 + v2
                elif op == "-":
                    val = v1 - v2
                elif op == "*":
                    val = v1 * v2
                else:
                    if v2 == 0:
                        raise CompilerError(0, "Division by zero")
                    val = v1 // v2
                new_code.append(type(quad)("=", str(val), None, res))
            else:
                new_code.append(quad)
            continue
        if op in {">", "<", "=="}:
            if is_int_literal(a1) and is_int_literal(a2):
                v1 = to_int(a1)
                v2 = to_int(a2)
                if op == ">":
                    val = 1 if v1 > v2 else 0
                elif op == "<":
                    val = 1 if v1 < v2 else 0
                else:
                    val = 1 if v1 == v2 else 0
                new_code.append(type(quad)("=", str(val), None, res))
            else:
                new_code.append(quad)
            continue
        new_code.append(quad)
    return new_code


def dead_code_eliminate(code):
    new_code = []
    for quad in code:
        op, a1, a2, res = quad.op, quad.arg1, quad.arg2, quad.result
        if op == "jumpt" and is_int_literal(a1):
            val = to_int(a1)
            if val == 0:
                continue
            new_code.append(type(quad)("jump", a2, None, None))
            continue
        new_code.append(quad)
    return new_code


def optimize(code):
    folded = constant_fold(code)
    cleaned = dead_code_eliminate(folded)
    return cleaned
