import os
import logging
import inspect

from command_line import compile_daspuml

logger = logging.getLogger(__name__)


def execute_source_code_and_verify_results(input_source_code, expected_output):
    try:
        with open("input.txt", 'w+') as fp:
            fp.write(input_source_code.lstrip())
        print(input_source_code.replace('\n', "<br />"))
        register = compile_daspuml("input.txt", f"{inspect.stack()[1].function}.png", "results/results_png")
        logger.info(input_source_code)
        logger.info('<img daspuml_compiler="output.png" alt="Girl in a jacket" width="500" height="600">')
        with open("output.txt", 'r') as fp:
            output = fp.read()
            assert output.strip() == expected_output.strip()
            fp.close()
        return register
    except BaseException as err:
        print_exception(err)
        raise err
    finally:
        os.remove("input.txt")
        if os.path.isfile("output.txt"):
            os.remove("output.txt")


def print_exception(err):
    print(f'<p style="color:red"> {err.__class__.__name__} {err}</p>')
