import unittest

from utilities import execute_source_code_and_verify_results
from exceptions import EmptyUmlGraphException


class ConnectionTest(unittest.TestCase):

    def test_correct_name_object_declaration(self):
        input_source_code = '''
obj aa
obj a1
obj a1a
obj a
'''
        expected_output = '''
'''
        self.assertRaises(EmptyUmlGraphException, execute_source_code_and_verify_results, input_source_code,
                          expected_output)
        # register = execute_source_code_and_verify_results(input_source_code, expected_output)
        # self.assertIn('aa', register.object_register)
        # self.assertIn('a1', register.object_register)
        # self.assertIn('a1a', register.object_register)
        # self.assertIn('a', register.object_register)

    def test_incorrect_names_object_declaration(self):
        input_source_code = ['obj 1', 'obj _']

        expected_output = '''
'''
        for incorrect_name in input_source_code:
            self.assertRaises(SyntaxError, execute_source_code_and_verify_results, incorrect_name, expected_output)

    def test_start_and_end_object(self):
        input_source_code = '''
obj aaa
start aaa
end aaa
'''

        expected_output = '''
activate aaa
deactivate aaa
'''
        register = execute_source_code_and_verify_results(input_source_code, expected_output)
        self.assertIn('aaa', register.object_register)

    def test_self_connection(self):
        input_source_code = '''
obj aaa
start aaa

aaa <- : "label_1"
aaa <.. : "label_2"
aaa <-- : "label_3"
'''

        expected_output = '''
activate aaa
aaa->aaa: label_1
aaa-->aaa: label_2
aaa-->aaa: label_3
'''
        execute_source_code_and_verify_results(input_source_code, expected_output)
