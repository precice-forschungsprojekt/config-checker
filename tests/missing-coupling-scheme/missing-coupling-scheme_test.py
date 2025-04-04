from precice_config_graph.nodes import DataNode, ParticipantNode, MeshNode, Direction

from preciceconfigchecker.rules.missing_coupling import MissingCouplingSchemeRule as c
from preciceconfigchecker.rules.mapping import MappingRule as m
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
        elif isinstance(node, ParticipantNode):
            if node.name == "Generator":
                p_generator = node
            elif node.name == "Propagator":
                p_propagator = node
        elif isinstance(node, MeshNode):
            if node.name == "Propagator-Mesh":
                m_propagator = node
            elif node.name == "Generator-Mesh":
                m_generator = node

    violations_expected = []

    v_missing_coupling_scheme = c.MissingCouplingSchemeViolation()
    violations_expected += [v_missing_coupling_scheme]

    v_data_not_exchanged = d.DataNotExchangedViolation(n_color, p_generator, p_propagator)
    violations_expected += [v_data_not_exchanged]

    violations_expected += [
        m.MissingCouplingSchemeMappingViolation(p_propagator, p_generator, m_generator, Direction.READ)]

    assert_equal_violations("Missing-coupling-scheme test", violations_expected, violations_actual)
