from precice_config_graph.nodes import DataNode

from preciceconfigchecker.rules.data_use_read_write import DataUseReadWriteRule as d

from tests.test_utils import assert_equal_violations, get_actual_violations, create_graph


def test_data_not_use_not_read_not_write():
    graph = create_graph("tests/data-rules/not_use-not_read-not_write/precice-config.xml")

    violations_actual = get_actual_violations(graph)

    for node in graph.nodes:
        if isinstance(node, DataNode):
            if node.name == "ErrorColor":
                n_error_color = node

    violations_expected = []
    # ErrorColor does not get used/read/written
    violations_expected += [d.DataNotUsedNotReadNotWrittenViolation(n_error_color)]

    assert_equal_violations("Data not used, not read, not written-test", violations_actual, violations_expected)
