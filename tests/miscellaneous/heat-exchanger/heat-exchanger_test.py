from precice_config_graph.nodes import ParticipantNode, MeshNode, DataNode, CouplingSchemeNode

from preciceconfigchecker.rules.data_use_read_write import DataUseReadWriteRule as d
from preciceconfigchecker.rules.missing_exchange import MissingExchangeRule as m

from tests.test_utils import assert_equal_violations, get_actual_violations, create_graph


# Config file taken from https://github.com/precice/tutorials/blob/develop/heat-exchanger/precice-config.xml



def test_heat_exchanger():
    graph = create_graph("precice-config.xml")

    violations_actual = get_actual_violations(graph)

    for node in graph.nodes:
        if isinstance(node, ParticipantNode):
            if node.name == "Fluid-Outer":
                n_FO = node
            elif node.name == "Fluid-Inner":
                n_FI = node
        if isinstance(node, MeshNode):
            if node.name == "Fluid-Outer-to-Fluid-Inner":
                n_mesh_FO2FI = node
        if isinstance(node, DataNode):
            if node.name == "ErrorData":
                n_error_data = node
            elif node.name == "VeryValidData":
                n_valid_data = node
            elif node.name == "Sink-Temperature-Fluid-Outer":
                n_sink_temp = node
        if isinstance(node, CouplingSchemeNode):
            if node.first_participant.name == "Fluid-Outer" and node.second_participant.name == "Fluid-Inner":
                n_coupling_scheme = node

    violations_expected = []

    violations_expected += [d.DataNotUsedNotReadNotWrittenViolation(n_sink_temp)]
    violations_expected += [d.DataNotExchangedViolation(n_valid_data, n_FO, n_FI)]
    violations_expected += [d.DataUsedNotReadWrittenViolation(n_error_data, n_mesh_FO2FI, n_FI)]
    violations_expected += [m.MissingExchangeViolation(n_coupling_scheme)]

    # TODO: NO M2N between Fluid-Outer and Fluid-Inner:
    # violations_expected += [m2n.NoM2NConnectionViolation(n_FO, n_FI)

    # TODO: write-data ErrorData of Fluid-Inner on mesh FO2FI is not allowed: not provided, no direct-access
    # violations_expected += [np.NoWritePermissionViolation(n_error_data, n_FI, n_mesh_FO2FI)

    # TODO: read-data VeryValidData of Fluid-Inner on mesh FO2FI is not allowed: not provided, no direct access
    # violations_expected += [np.NoReadPermissionViolation(n_valid_data, n_FI, n_mesh_FO2FI)

    assert_equal_violations("Heat-Exchanger-test", violations_expected, violations_actual)
