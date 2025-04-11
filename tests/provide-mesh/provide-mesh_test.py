from precice_config_graph.nodes import ParticipantNode, MeshNode

from tests.test_utils import assert_equal_violations, get_actual_violations, create_graph
from preciceconfigchecker.rules.provide_mesh import ProvideMeshRule as pm


def test_simple_good():
    # tests/provide-mesh/
    graph = create_graph("tests/provide-mesh/precice-config.xml")

    violations_actual = get_actual_violations(graph)

    for node in graph.nodes:
        if isinstance(node, ParticipantNode):
            if node.name == "Generator":
                p_generator = node
            elif node.name == "Propagator":
                p_propagator = node
        elif isinstance(node, MeshNode):
            if node.name == "Forsaken-Mesh":
                m_forsaken = node
            elif node.name == "Popular-Mesh":
                m_popular = node

    violations_expected = [

        pm.UnclaimedMeshViolation(m_forsaken),

        pm.RepeatedlyClaimedMeshViolation([p_generator, p_propagator], m_popular)

    ]

    assert_equal_violations("Provide-mesh test", violations_expected, violations_actual)
