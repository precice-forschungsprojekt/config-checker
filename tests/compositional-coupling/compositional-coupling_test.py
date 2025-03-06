from precice_config_graph.nodes import ParticipantNode

from preciceconfigchecker.rules.compositional_coupling import CompositionalCouplingRule as c

from tests.test_utils import assert_equal_violations, get_actual_violations, create_graph


def test_missing_coupling_scheme():
    graph = create_graph("tests/compositional-coupling/precice-config.xml")

    violations_actual = get_actual_violations(graph)

    # Extract nodes from graph to build custom violations
    for node in graph.nodes():
        if isinstance(node, ParticipantNode):
            if node.name == "Generator":
                n_generator = node
            elif node.name == "Propagator":
                n_propagator = node
            elif node.name == "Alligator":
                n_alligator = node

    violations_expected = []
    violations_expected += [c.CompositionalDeadlockViolation([n_generator, n_propagator, n_alligator])]

    assert_equal_violations("Compositional-coupling test", violations_expected, violations_actual)
