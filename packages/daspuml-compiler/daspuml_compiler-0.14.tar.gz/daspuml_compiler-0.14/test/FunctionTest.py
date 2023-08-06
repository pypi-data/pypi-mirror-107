import unittest

from utilities import execute_source_code_and_verify_results
from exceptions import CalledFunctionNotDeclaredException, EmptyUmlGraphException


class FunctionTest(unittest.TestCase):

    def test_function_declaration_with_variable(self):
        input_source_code = '''
fun fun_name
$var=[listing, watching, watching]
end fun

'''
        expected_output = '''
'''
        self.assertRaises(EmptyUmlGraphException, execute_source_code_and_verify_results, input_source_code,
                          expected_output)
        # register = execute_source_code_and_verify_results(input_source_code, expected_output)
        # self.assertIn('fun_name', register.variable_register)
        # self.assertIn('var', register.variable_register['fun_name'])

    def test_function_call_with_variable(self):
        input_source_code = '''
fun fun_name
$var=[listing, watching, watching]
end fun

call fun_name

'''
        expected_output = '''
'''
        self.assertRaises(EmptyUmlGraphException, execute_source_code_and_verify_results, input_source_code,
                          expected_output)
        # register = execute_source_code_and_verify_results(input_source_code, expected_output)
        # self.assertIn('fun_name', register.variable_register)
        # self.assertIn('var', register.variable_register['fun_name'])

    def test_function_declaration_with_connection(self):
        input_source_code = '''
obj aa
obj bb

fun fun_name
aa->bb: "label"
end fun

'''
        expected_output = '''
'''
        self.assertRaises(EmptyUmlGraphException, execute_source_code_and_verify_results, input_source_code,
                          expected_output)
        # register = execute_source_code_and_verify_results(input_source_code, expected_output)
        # print
        # self.assertIn('aa', register.object_register)
        # self.assertIn('bb', register.object_register)
        # self.assertIn('fun_name', register.variable_register)

    def test_function_call_with_connection(self):
        input_source_code = '''
obj aa
obj bb

start aa
start bb

fun fun_name
aa->bb: "label"
end fun

call fun_name

'''
        expected_output = '''
activate aa
activate bb
aa->bb: label
'''

        register = execute_source_code_and_verify_results(input_source_code, expected_output)
        self.assertIn('aa', register.object_register)
        self.assertIn('bb', register.object_register)
        self.assertIn('fun_name', register.variable_register)
        self.assertIn('fun_name', register.function_register)

    def test_function_declaration_with_pattern(self):
        input_source_code = '''
obj listing
obj watching
fun fun_name
ptr [listing, watching]; ["Odczytanie danych", "Zapisanie danych"]:
pre->nxt: stp
end ptr
end fun

'''
        expected_output = '''
'''
        self.assertRaises(EmptyUmlGraphException, execute_source_code_and_verify_results, input_source_code,
                          expected_output)
        # register = execute_source_code_and_verify_results(input_source_code, expected_output)
        # self.assertIn('listing', register.object_register)
        # self.assertIn('watching', register.object_register)
        # self.assertIn('fun_name', register.variable_register)

    def test_function_call_with_pattern(self):
        input_source_code = '''
obj listing
obj watching

start listing
start watching

fun fun_name
ptr [listing, watching]; ["Odczytanie danych"]:
listing->watching: stp
end ptr
end fun

call fun_name
'''
        expected_output = '''
activate listing
activate watching
listing->watching: Odczytanie danych
'''
        register = execute_source_code_and_verify_results(input_source_code, expected_output)
        self.assertIn('listing', register.object_register)
        self.assertIn('watching', register.object_register)
        self.assertIn('fun_name', register.variable_register)

    def test_call_not_declared_function(self):
        input_source_code = '''
call fun_name
'''
        expected_output = '''
'''
        self.assertRaises(CalledFunctionNotDeclaredException, execute_source_code_and_verify_results, input_source_code, expected_output)

