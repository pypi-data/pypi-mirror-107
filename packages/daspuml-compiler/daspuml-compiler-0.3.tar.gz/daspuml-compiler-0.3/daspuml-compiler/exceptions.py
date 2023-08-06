class ObjectNotDeclaredException(BaseException):
    def __init__(self, notDeclaredObj):
        self.notDeclaredObj = notDeclaredObj

    def __str__(self):
        return f"Object {self.notDeclaredObj} not found"


class VariableNotDeclaredException(BaseException):
    def __init__(self, notDeclaredVar):
        self.notDeclaredVar = notDeclaredVar

    def __str__(self):
        return f"Variable {self.notDeclaredVar} not declared"


class CalledFunctionNotDeclaredException(BaseException):
    def __init__(self, notDeclaredFunction):
        self.notDeclaredFunction = notDeclaredFunction

    def __str__(self):
        return f"Called function {self.notDeclaredFunction} not declared"


class EmptyUmlGraphException(BaseException):
    def __str__(self):
        return f"Code generates nothing"


class ObjectNotStartedException(BaseException):
    def __init__(self, notStartedObj):
        self.notStartedObj = notStartedObj

    def __str__(self):
        return f"Object {self.notStartedObj} not started"


class ObjectEndedException(BaseException):
    def __init__(self, notStartedObj):
        self.notStartedObj = notStartedObj

    def __str__(self):
        return f"Object {self.notStartedObj} was ended previously"


class NoCaseDeclarationInPatternException(BaseException):
    def __str__(self):
        return f"Pattern does not have cases list"
