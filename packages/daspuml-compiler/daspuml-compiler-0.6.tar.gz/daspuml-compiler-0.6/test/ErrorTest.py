import unittest

from utilities import execute_source_code_and_verify_results
from exceptions import ObjectEndedException, ObjectNotStartedException, EmptyUmlGraphException, \
    NoCaseDeclarationInPatternException, ObjectNotDeclaredException, VariableNotDeclaredException, \
    CalledFunctionNotDeclaredException


class ErrorTest(unittest.TestCase):

    def test_starting_deactivated_object_raises_exception(self):
        input_source_code = '''
obj TestedObject
start TestedObject
end TestedObject
start TestedObject

'''
        expected_output = '''
'''
        self.assertRaises(ObjectEndedException, execute_source_code_and_verify_results, input_source_code,
                          expected_output)

    def test_ending_deactivated_object_raises_exception(self):
        input_source_code = '''
obj TestedObject
end TestedObject

'''
        expected_output = '''
'''
        self.assertRaises(ObjectNotStartedException, execute_source_code_and_verify_results, input_source_code,
                      expected_output)

    def test_code_generate_nothing_raises_exception(self):
        input_source_code = '''
obj TestedObject

'''
        expected_output = '''
'''
        self.assertRaises(EmptyUmlGraphException, execute_source_code_and_verify_results, input_source_code,
                      expected_output)

    def test_object_not_declarated_exception(self):
        input_source_code = '''
TestObject -> TestObject: "tested string"

'''
        expected_output = '''
'''
        self.assertRaises(ObjectNotDeclaredException, execute_source_code_and_verify_results,
                          input_source_code,
                          expected_output)

    def test_variable_not_declarated_exception(self):
        input_source_code = '''
ptr $var; ["test1", "test2", "test3"]:
pre -> nxt: stp
end ptr

'''
        expected_output = '''
'''
        self.assertRaises(VariableNotDeclaredException, execute_source_code_and_verify_results,
                          input_source_code,
                          expected_output)

    def test_function_not_declarated_exception(self):
        input_source_code = '''
call test_fun

'''
        expected_output = '''
'''
        self.assertRaises(CalledFunctionNotDeclaredException, execute_source_code_and_verify_results,
                          input_source_code,
                          expected_output)

    def test_pattern_uses_cases_without_caselist_exception(self):
        input_source_code = '''
obj TestedObject1
obj TestedObject2
start TestedObject1
ptr [TestedObject1, TestedObject2]; ["tested string"]:
case "test": pre->nxt: stp
end ptr

'''
        expected_output = '''
'''
        self.assertRaises(NoCaseDeclarationInPatternException, execute_source_code_and_verify_results, input_source_code,
                      expected_output)

