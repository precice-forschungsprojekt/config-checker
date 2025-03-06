from precice_config_graph import graph as g, xml_processing
from tests.test_utils import assert_equal_violations, get_actual_violations, create_graph


def test_simple_good():
    graph = create_graph("tests/simple-good/precice-config.xml")

    violations_actual = get_actual_violations(graph)

    # No violations are expected
    violations_expected = []

    assert_equal_violations("Simple-good test", violations_expected, violations_actual)
