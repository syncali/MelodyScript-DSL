class CompilerError(Exception):
    def __init__(self, line, message):
        super().__init__(message)
        self.line = line
        self.message = message

    def __str__(self):
        if self.line:
            return f"Error on line {self.line}: {self.message}"
        return self.message
