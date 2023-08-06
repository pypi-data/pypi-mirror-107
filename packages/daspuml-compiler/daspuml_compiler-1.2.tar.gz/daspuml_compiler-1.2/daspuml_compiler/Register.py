if __name__ is not None and "." in __name__:
    from .exceptions import VariableNotDeclaredException, ObjectNotDeclaredException, CalledFunctionNotDeclaredException
else:
    from exceptions import VariableNotDeclaredException, ObjectNotDeclaredException, CalledFunctionNotDeclaredException


class Register:
    global_scope_name = 'start'
    
    def __init__(self):
        self.variable_register = {self.global_scope_name: {}}
        self.function_register = {}
        self.object_register = {}

    def get_variable(self, variable_name, scope_name, codeLine):
        if scope_name is None:
            if variable_name in self.variable_register[self.global_scope_name]:
                return self.variable_register[self.global_scope_name][variable_name]
            else:
                raise VariableNotDeclaredException(variable_name, codeLine)
        if variable_name in self.variable_register[scope_name]:
            return self.variable_register[scope_name][variable_name]
        elif variable_name in self.variable_register[self.global_scope_name]:
            return self.variable_register[self.global_scope_name][variable_name]
        else:
            raise VariableNotDeclaredException(variable_name, codeLine)

    def get_object(self, object_name, codeLine):
        if object_name in self.object_register:
            return self.object_register[object_name]
        else:
            raise ObjectNotDeclaredException(object_name, codeLine)

    def get_function_to_call(self, function_name, codeLine):
        if function_name in self.function_register:
            return self.function_register[function_name]
        else:
            raise CalledFunctionNotDeclaredException(function_name, codeLine)
