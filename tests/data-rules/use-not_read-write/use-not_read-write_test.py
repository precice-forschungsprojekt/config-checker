from precice_config_graph.nodes import DataNode, MeshNode, ParticipantNode

from preciceconfigchecker.rules.data_use_read_write import DataUseReadWriteRule as d

from tests.test_utils import assert_equal_violations, get_actual_violations, create_graph


def test_data_not_use_not_read_not_write():
    graph = create_graph("tests/data-rules/use-not_read-write/precice-config.xml")

    violations_actual = get_actual_violations(graph)

    for node in graph.nodes:
        if isinstance(node, DataNode):
            if node.name == "ErrorColor":
                n_error_color = node
        if isinstance(node, MeshNode):
            if node.name == "Generator-Mesh":
                n_mesh = node
        if isinstance(node, ParticipantNode):
            if node.name == "Generator":
                n_generator = node

    violations_expected = []
    # ErrorColor gets used in Generator-Mesh, does not get read, gets written by participant Generator
    violations_expected += [d.DataUsedNotReadWrittenViolation(n_error_color, n_mesh, n_generator)]

    assert_equal_violations("Data used, not read, written-test", violations_actual, violations_expected)
