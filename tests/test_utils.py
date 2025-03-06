import contextlib
import io

from networkx import Graph
from precice_config_graph import xml_processing, graph as g

from preciceconfigchecker.rule import rules
from preciceconfigchecker.rules_processing import check_all_rules
from preciceconfigchecker.violation import Violation
from preciceconfigchecker import color


# Helper functions for test files

def equals(a, b) -> bool:
    """
        This function tests if two objects have equal values.
        :param a: The first object.
        :param b: The second object.
        :return: True, if the objects are equal, else False.
    """
    if type(a) != type(b):
        return False
    return vars(a) == vars(b)


def assert_equal_violations(test_name: str, violations_expected: list[Violation],
                            violations_actual: list[Violation]) -> None:
    """
        This function asserts that lists containing expected and actual violations are equal.
        :param test_name: The name of the test which causes the violations.
        :param violations_expected: The expected list of violations.
        :param violations_actual: The actual list of violations.
        :return: AssertionError, if the violations are not equal
    """
    # Sort them so that violations of the same type are in the same order
    violations_expected_s = sorted(violations_expected, key=lambda obj: type(obj).__name__)
    violations_actual_s = sorted(violations_actual, key=lambda obj: type(obj).__name__)

    assert len(violations_actual_s) == len(violations_expected_s), (
        f"[{test_name}] Different number of expected- and actual violations.\n"
        f"   Number of expected violations: {len(violations_expected)},\n"
        f"   Number of actual violations: {len(violations_actual)}.")

    for violation_e, violation_a in zip(violations_expected_s, violations_actual_s):
        assert equals(violation_a, violation_e), (
            f"[{test_name}] Expected- and actual violations do not match.\n"
            f"   Expected violation: {violation_e.format_explanation()}\n"
            f"   Actual violation: {violation_a.format_explanation()}")
    # Only gets reached if no AssertionError gets raised
    print(f"\n[{test_name}] {color.dyeing("Passed", color.green)}.")


def get_actual_violations(graph: Graph) -> list[Violation]:
    """
        This function returns a list containing all violations found by our checker of a given graph,
         representing a precice-config file.
        :param graph: The graph to check.
        :return: The violations found.
    """
    violations_actual = []
    # To suppress terminal messages
    with contextlib.redirect_stdout(io.StringIO()):
        # Debug=True might find additional violations, if they are of the severity "debug".
        violations_by_rule = check_all_rules(graph, True)

    for rule in rules:
        violations_actual += violations_by_rule[rule]

    return violations_actual


def create_graph(path: str) -> Graph:
    """
        This function creates a graph from a precice-config.xml file.
        :param path: The path to the precice-config.xml file.
        :return: The graph created.
    """
    xml = xml_processing.parse_file(path)
    graph = g.get_graph(xml)
    return graph
