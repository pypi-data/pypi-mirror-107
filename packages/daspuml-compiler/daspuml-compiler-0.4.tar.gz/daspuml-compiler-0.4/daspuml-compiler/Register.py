from exceptions import VariableNotDeclaredException, ObjectNotDeclaredException, CalledFunctionNotDeclaredException


class Register:
    global_scope_name = 'start'
    
    def __init__(self):
        self.variable_register = {self.global_scope_name: {}}
        self.function_register = {}
        self.object_register = {}

    def get_variable(self, variable_name, scope_name):
        if scope_name is None:
            if variable_name in self.variable_register[self.global_scope_name]:
                return self.variable_register[self.global_scope_name][variable_name]
            else:
                raise VariableNotDeclaredException(variable_name)
        if variable_name in self.variable_register[scope_name]:
            return self.variable_register[scope_name][variable_name]
        elif variable_name in self.variable_register[self.global_scope_name]:
            return self.variable_register[self.global_scope_name][variable_name]
        else:
            raise VariableNotDeclaredException(variable_name)

    def get_object(self, object_name):
        if object_name in self.object_register:
            return self.object_register[object_name]
        else:
            raise ObjectNotDeclaredException(object_name)

    def get_function_to_call(self, function_name):
        if function_name in self.function_register:
            return self.function_register[function_name]
        else:
            raise CalledFunctionNotDeclaredException(function_name)
