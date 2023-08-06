import unittest

from utilities import execute_source_code_and_verify_results


class PatternTest(unittest.TestCase):
    def test_single_connection(self):
        input_source_code = '''
obj watching
obj listing

start watching
start listing

ptr [listing, watching]; ["Odczytanie danych", "Zapisanie danych"]:
pre->nxt: stp
end ptr
'''
        expected_output = '''
activate watching
activate listing
listing->watching: Odczytanie danych
'''
        execute_source_code_and_verify_results(input_source_code, expected_output)

    def test_multiple_connection(self):
        input_source_code = '''
obj watching
obj listing

start watching
start listing

ptr [listing, watching, listing]; ["Odczytanie danych", "Zapisanie danych"]:
pre->nxt: stp
end ptr
'''
        expected_output = '''
activate watching
activate listing
listing->watching: Odczytanie danych
watching->listing: Zapisanie danych
'''
        execute_source_code_and_verify_results(input_source_code, expected_output)

    def test_case_pattern(self):
        input_source_code = '''
obj listing
obj watching
obj get_episode

start listing
start watching
start  get_episode

$var=[listing, watching, watching, watching]

ptr [listing, watching, get_episode]; ["case 1", "case 2"]; ["a", "b"]:
   pre  -> nxt: "no case"
   case "a" : pre  -> nxt: stp
   case "b" : nxt  -> pre: stp
end ptr
'''
        expected_output = '''
activate listing
activate watching
activate get_episode
listing->watching: "no case"
listing->watching: case 1
watching->get_episode: "no case"
get_episode->watching: case 2
'''
        execute_source_code_and_verify_results(input_source_code, expected_output)

    def test_multiple_self_connection(self):
        input_source_code = '''
obj watching
obj listing

start watching
start listing

ptr [listing, watching, listing]; ["Odczytanie danych", "Zapisanie danych"]:
pre<-: stp
pre<--: stp
pre<..: stp
end ptr
'''
        expected_output = '''
activate watching
activate listing
listing->listing: Odczytanie danych
listing-->listing: Odczytanie danych
listing-->listing: Odczytanie danych
watching->watching: Zapisanie danych
watching-->watching: Zapisanie danych
watching-->watching: Zapisanie danych
'''
        execute_source_code_and_verify_results(input_source_code, expected_output)

