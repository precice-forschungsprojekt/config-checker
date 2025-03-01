import networkx as nx
from networkx import Graph
from precice_config_graph.nodes import DataNode, MeshNode, ReadDataNode, WriteDataNode, WatchPointNode, ExportNode, \
    WatchIntegralNode, ParticipantNode, ExchangeNode, ActionNode
from preciceconfigchecker.rule import Rule
from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation


class DataUseReadWriteRule(Rule):
    name = "Utilization of data."
    # These are oversights, but do not necessarily cause the simulation to malfunction.
    severity = Severity.WARNING

    class DataNotUsedNotReadNotWrittenViolation(Violation):
        """
            This violation handles nobody using, reading or writing a data node.
        """

        def __init__(self, data_node: DataNode):
            self.data_node = data_node

        def format_explanation(self) -> str:
            return f"Data {self.data_node.name} is declared but never used, read or written."

        def format_possible_solutions(self) -> list[str]:
            return [f"Consider using {self.data_node.name} in a mesh and have participants read and write it.",
                    "Otherwise please remove it to improve readability."]

    class DataUsedNotReadNotWrittenViolation(Violation):
        """
            This violation handles someone using a data node, but nobody is reading and writing said data node.
        """

        def __init__(self, data_node: DataNode, mesh: MeshNode):
            self.data_node = data_node
            self.mesh = mesh

        def format_explanation(self) -> str:
            return f"Data {self.data_node.name} gets used in mesh {self.mesh.name}, but nobody is reading or writing it."

        def format_possible_solutions(self) -> list[str]:
            return [f"Consider having a participant read data {self.data_node.name}.",
                    f"Consider having a participant write data {self.data_node.name}.",
                    "Otherwise please remove it to improve readability."]

    class DataUsedNotReadWrittenViolation(Violation):
        """
            This class handles someone using and writing a data node, but nobody reading said data node.
        """

        def __init__(self, data_node: DataNode, mesh: MeshNode, writer: ParticipantNode):
            self.data_node = data_node
            self.mesh = mesh
            self.writer = writer

        def format_explanation(self) -> str:
            return (
                f"Data {self.data_node.name} is used in mesh {self.mesh.name} and participant {self.writer.name} "
                f"is writing it, but nobody is reading it.")

        def format_possible_solutions(self) -> list[str]:
            return [f"Consider having a participant read data {self.data_node.name}.",
                    f"Consider exporting data {self.data_node.name} by a participant.",
                    f"Consider using watchpoints or watch-integrals to keep track of data {self.data_node.name}.",
                    "Otherwise please remove it to improve readability."]

    class DataUsedReadNotWrittenViolation(Violation):
        """
            This class handles a mesh using and someone reading a data node, but nobody writing said data node.
        """

        def __init__(self, data_node: DataNode, mesh: MeshNode, reader: ParticipantNode):
            self.data_node = data_node
            self.mesh = mesh
            self.reader = reader

        def format_explanation(self) -> str:
            return (f"Data {self.data_node.name} is being used in mesh {self.mesh.name} and participant "
                    f"{self.reader.name} is reading it, but nobody is writing it.")

        def format_possible_solutions(self) -> list[str]:
            return [f"Consider having a participant write {self.data_node.name}.",
                    "Otherwise please remove it to improve readability."]

    class DataNotExchangedViolation(Violation):
        """
            This class handles data being used in a mesh, read and written by different participants,
            but not being exchanged between them.
        """

        def __init__(self, data_node: DataNode, writer: ParticipantNode, reader: ParticipantNode):
            self.data_node = data_node
            self.writer = writer
            self.reader = reader

        def format_explanation(self) -> str:
            return (f"Data {self.data_node.name} gets written by {self.writer.name} and read by {self.reader.name}, "
                    f"but not exchanged between them.")

        def format_possible_solutions(self) -> list[str]:
            return [f"Please exchange {self.data_node.name} in a coupling-scheme between participants "
                    f"{self.writer.name} and {self.reader.name}"]

    def check(self, graph: Graph) -> list[Violation]:
        violations: list[Violation] = []

        g1 = nx.subgraph_view(graph, filter_node=filter_use_read_write_data)
        for data_node in g1.nodes:
            # We only need to test data nodes here
            if isinstance(data_node, DataNode):
                use_data: bool = False
                read_data: bool = False
                write_data: bool = False
                meshes: list[MeshNode] = []
                writers: list[ParticipantNode] = []
                readers: list[ParticipantNode] = []

                # Check all neighbors of the data node for use-, reader- and writer-nodes
                for neighbor in g1.neighbors(data_node):
                    # Check if data gets used by a mesh
                    if isinstance(neighbor, MeshNode):
                        use_data = True
                        meshes += [neighbor]
                        mesh_neighbors = g1.neighbors(neighbor)
                        # Check if mesh gets observed by export, action, watchpoint or watch-integral.
                        # These types of reader nodes do not read the data itself, but only "read" the mesh and all of
                        # its used data.
                        # They are thus less important than a read-data node (which represents a participant),
                        # so only check them if no read-data node has been found.
                        for mesh_neighbor in mesh_neighbors:
                            if isinstance(mesh_neighbor, ExportNode) and not read_data:
                                read_data = True
                                readers += [mesh_neighbor.participant]
                            elif isinstance(mesh_neighbor, WatchPointNode) and not read_data:
                                read_data = True
                                readers += [mesh_neighbor.participant]
                            elif isinstance(mesh_neighbor, WatchIntegralNode) and not read_data:
                                read_data = True
                                readers += [mesh_neighbor.participant]
                            elif isinstance(mesh_neighbor, ActionNode):
                                # Check if action reads or writes data (corresponds to source or target data)
                                # Check all source-data nodes if they correspond to the current data node
                                for source in mesh_neighbor.source_data:
                                    if source == data_node:
                                        read_data = True
                                        # Use the participant associated with the action
                                        readers += [mesh_neighbor.participant]
                                # Check if the target data corresponds to the current data node
                                if mesh_neighbor.target_data == data_node:
                                    write_data = True
                                    # Use the participant associated with the action
                                    writers += [mesh_neighbor.participant]

                    # Check if data gets read by a participant
                    elif isinstance(neighbor, ReadDataNode):
                        read_data = True
                        readers += [neighbor.participant]
                    # Check if data gets written by a participant
                    elif isinstance(neighbor, WriteDataNode):
                        write_data = True
                        writers += [neighbor.participant]

                # Add violations according to use/read/write
                if use_data and read_data and write_data:
                    # Check if there exists a path from writer to reader or if they are the same
                    data_flow_edges = []
                    # Build a graph from participants involved in exchanges of data node
                    exchanges = [node for node in graph.nodes
                                 if isinstance(node, ExchangeNode) and node.data == data_node]
                    for exchange in exchanges:
                        data_flow_edges += [(exchange.from_participant, exchange.to_participant)]
                    data_flow_graph = nx.DiGraph()
                    data_flow_graph.add_edges_from(data_flow_edges)
                    # Check if data gets read and written by the same participant.
                    # If so, then no exchange is needed.
                    # Otherwise, an exchange is needed.
                    for writer in writers:
                        for reader in readers:
                            # If they are the same, then everything is fine.
                            if reader == writer:
                                continue
                            # Otherwise, there needs to be an exchange of data between them.
                            else:
                                if writer not in data_flow_graph or reader not in data_flow_graph:
                                    # One of writer/reader is not connected through an exchange involving data_node
                                    violations.append(self.DataNotExchangedViolation(data_node, writer, reader))
                                else:
                                    # Both writer/reader are connected with an exchange involving data_node
                                    # Check if there exists a path between them
                                    path = nx.has_path(data_flow_graph, writer, reader)
                                    if not path:
                                        violations.append(self.DataNotExchangedViolation(data_node, writer, reader))

                elif use_data and read_data and not write_data:
                    for mesh in meshes:
                        for reader in readers:
                            violations.append(self.DataUsedReadNotWrittenViolation(data_node, mesh, reader))
                elif use_data and not read_data and write_data:
                    for mesh in meshes:
                        for writer in writers:
                            violations.append(self.DataUsedNotReadWrittenViolation(data_node, mesh, writer))
                elif use_data and not read_data and not write_data:
                    for mesh in meshes:
                        violations.append(self.DataUsedNotReadNotWrittenViolation(data_node, mesh))

                elif not use_data and read_data and write_data:
                    # This case gets handled by precice-tools check
                    continue
                elif not use_data and read_data and not write_data:
                    # This case gets handled by precice-tools check
                    continue
                elif not use_data and not read_data and write_data:
                    # This case gets handled by precice-tools check
                    continue
                elif not use_data and not read_data and not write_data:
                    violations.append(self.DataNotUsedNotReadNotWrittenViolation(data_node))
        return violations


# Initialize a rule object to add it to the rules-array.
DataUseReadWriteRule()


def filter_use_read_write_data(node) -> bool:
    """
    This method filters nodes, that could potentially use data, read data or write data.

    A mesh is the only node that can "use" data.

    A read-data node, export, watchpoint, watch-integral or action are considered to "read" data.

    A write-data- or action-node is considered to "write" data.

    Args:
         node: The node to check.

    Returns:
        True, if the node is a data-, read-/write-, action- or mesh node.
    """
    return (isinstance(node, DataNode) or
            isinstance(node, MeshNode) or
            isinstance(node, ReadDataNode) or
            isinstance(node, ExportNode) or
            isinstance(node, WatchPointNode) or
            isinstance(node, WatchIntegralNode) or
            isinstance(node, WriteDataNode) or
            isinstance(node, ActionNode))


def filter_data_exchange(node) -> bool:
    return (isinstance(node, DataNode) or
            isinstance(node, ExchangeNode))
