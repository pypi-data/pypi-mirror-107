from unittest import TestLoader, TestSuite
from HtmlTestRunner import HTMLTestRunner

from PatternTest import PatternTest
from ConnectionTest import ConnectionTest
from FunctionTest import FunctionTest
from VariableScopeTest import VariableScopeTest
from AutonumTest import AutonumTest
from ErrorTest import ErrorTest
import coverage

pattern_tests = TestLoader().loadTestsFromTestCase(PatternTest)
variable_tests = TestLoader().loadTestsFromTestCase(VariableScopeTest)
connection_tests = TestLoader().loadTestsFromTestCase(ConnectionTest)
function_tests = TestLoader().loadTestsFromTestCase(FunctionTest)
autonumber_tests = TestLoader().loadTestsFromTestCase(AutonumTest)
error_tests = TestLoader().loadTestsFromTestCase(ErrorTest)

suite = TestSuite([pattern_tests, variable_tests, connection_tests, function_tests, autonumber_tests, error_tests])

runner = HTMLTestRunner(report_title="daspUML test results",
                        combine_reports=True,
                        output='/home/dominik/Documents/daspuml-language/test/results/',
                        report_name='test_results',
                        template='report_template.html',
                        add_timestamp=False)
runner.run(suite)

