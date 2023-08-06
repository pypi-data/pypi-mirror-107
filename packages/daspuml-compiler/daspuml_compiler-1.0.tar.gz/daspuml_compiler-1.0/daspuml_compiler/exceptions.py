class ObjectNotDeclaredException(BaseException):
    def __init__(self, notDeclaredObj, line):
        self.notDeclaredObj = notDeclaredObj
        self.line = line

    def __str__(self):
        return f"Line {self.line}. Object {self.notDeclaredObj} not found"


class VariableNotDeclaredException(BaseException):
    def __init__(self, notDeclaredVar, line):
        self.notDeclaredVar = notDeclaredVar
        self.line = line

    def __str__(self):
        return f"Line {self.line}. Variable {self.notDeclaredVar} not declared"


class CalledFunctionNotDeclaredException(BaseException):
    def __init__(self, notDeclaredFunction, line):
        self.notDeclaredFunction = notDeclaredFunction
        self.line = line

    def __str__(self):
        return f"Line {self.line}. Called function {self.notDeclaredFunction} not declared"


class EmptyUmlGraphException(BaseException):
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return f"Code generates nothing"


class ObjectNotStartedException(BaseException):
    def __init__(self, notStartedObj, line):
        self.notStartedObj = notStartedObj
        self.line = line

    def __str__(self):
        return f"Line {self.line}. Object {self.notStartedObj} not started"


class ObjectEndedException(BaseException):
    def __init__(self, notStartedObj, line):
        self.notStartedObj = notStartedObj
        self.line = line

    def __str__(self):
        return f"Line {self.line}. Object {self.notStartedObj} was ended previously"


class NoCaseDeclarationInPatternException(BaseException):
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return f"Line {self.line}. Pattern does not have cases list"
