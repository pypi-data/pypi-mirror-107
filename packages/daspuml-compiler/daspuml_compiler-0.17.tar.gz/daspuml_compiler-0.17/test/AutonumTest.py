import unittest

from utilities import execute_source_code_and_verify_results
from exceptions import EmptyUmlGraphException


class AutonumTest(unittest.TestCase):

    def test_single_autonum_single_connection(self):
        input_source_code = '''
obj first
obj second
autonum
start first
first -> second :"word"

'''
        expected_output = '''
autonumber 
activate first
first->second: word

'''
        execute_source_code_and_verify_results(input_source_code, expected_output)

    def test_single_autonum_multiple_connections(self):
        input_source_code = '''
obj first
obj second
obj third
start first
start second
start third
autonum
ptr [first, second, third, first]; ["word","word","word"]:
pre->nxt:stp
end ptr

'''
        expected_output = '''
activate first
activate second
activate third
autonumber 
first->second: word
second->third: word
third->first: word

'''
        execute_source_code_and_verify_results(input_source_code, expected_output)

    def test_multiple_autonum_single_connections(self):
        input_source_code = '''
obj first
obj second
obj third
start first
start second
start third
first -> second :"word"
autonum
second -> third :"word"
autonum
third -> first :"word"

'''
        expected_output = '''
activate first
activate second
activate third
first->second: word
autonumber 
second->third: word
autonumber 
third->first: word

'''
        execute_source_code_and_verify_results(input_source_code, expected_output)

    def test_multiple_autonum_multiple_connections(self):
        input_source_code = '''
obj first
obj second
obj third
start first
start second
start third
fun test_fun
ptr [first, second, third]; ["word","word"]:
pre->nxt:stp
end ptr
end fun
call test_fun
autonum
call test_fun
autonum
call test_fun


'''
        expected_output = '''
activate first
activate second
activate third
first->second: word
second->third: word
autonumber 
first->second: word
second->third: word
autonumber 
first->second: word
second->third: word

'''
        execute_source_code_and_verify_results(input_source_code, expected_output)
