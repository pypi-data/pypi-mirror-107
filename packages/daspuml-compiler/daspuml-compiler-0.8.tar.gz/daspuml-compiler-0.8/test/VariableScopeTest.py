import unittest

from utilities import execute_source_code_and_verify_results
from exceptions import VariableNotDeclaredException


class VariableScopeTest(unittest.TestCase):
    def test_not_existing_variable_in_main_scope(self):
        input_source_code = '''
ptr $var; ["a22222222222", "a222222222", "a2222222222", "a2222222222", "a2222222222"]:
watching  -> get_episode: stp
end ptr
'''
        expected_output = '''
'''
        self.assertRaises(VariableNotDeclaredException, execute_source_code_and_verify_results, input_source_code, expected_output)

    def test_not_existing_variable_in_local_scope(self):
        input_source_code = '''
fun fun_name
ptr $var; ["test1", "test2", "test3"]:
watching  -> get_episode: stp
end ptr
end fun

call fun_name
'''
        expected_output = '''
'''
        self.assertRaises(VariableNotDeclaredException, execute_source_code_and_verify_results, input_source_code, expected_output)

    def test_global_variable_in_local_scope(self):
        input_source_code = '''
obj aa
obj bb

start aa
start bb

$var = [aa, bb]

fun fun_name
ptr $var; ["test1"]:
pre  -> nxt: stp
end ptr
end fun

call fun_name
'''
        expected_output = '''
activate aa
activate bb
aa->bb: test1
'''
        execute_source_code_and_verify_results(input_source_code, expected_output)

    def test_local_variable_in_local_scope(self):
        input_source_code = '''
obj aa
obj bb
obj cc

start aa
start bb
start cc

$var = [aa, bb]

fun fun_name
$var = [aa, bb, cc]
ptr $var; ["test1", "test2"]:
pre  -> nxt: stp
end ptr
end fun

call fun_name
'''
        expected_output = '''
activate aa
activate bb
activate cc
aa->bb: test1
bb->cc: test2
'''
        execute_source_code_and_verify_results(input_source_code, expected_output)
