from precice_config_graph import graph as g, xml_processing
from precice_config_graph.nodes import DataNode, ParticipantNode

from preciceconfigchecker.rules.missing_coupling import MissingCouplingSchemeRule as c
from preciceconfigchecker.rules.data_use_read_write import DataUseReadWriteRule as d
from tests.test_utils import assert_equal_violations, get_actual_violations, create_graph


def test_missing_coupling_scheme():
    graph = create_graph("tests/missing-coupling-scheme/precice-config.xml")

    violations_actual = get_actual_violations(graph)

    # Extract nodes from graph to build custom violations
    for node in graph.nodes():
        if isinstance(node, DataNode):
            if node.name == "Color":
                n_color = node
        if isinstance(node, ParticipantNode):
            if node.name == "Generator":
                n_generator = node
            elif node.name == "Propagator":
                n_propagator = node

    violations_expected = []

    v_missing_coupling_scheme = c.MissingCouplingSchemeViolation()
    violations_expected += [v_missing_coupling_scheme]

    v_data_not_exchanged = d.DataNotExchangedViolation(n_color, n_generator, n_propagator)
    violations_expected += [v_data_not_exchanged]

    assert_equal_violations("Missing-coupling-scheme test", violations_expected, violations_actual)
