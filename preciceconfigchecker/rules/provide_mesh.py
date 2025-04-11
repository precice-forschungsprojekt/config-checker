import networkx as nx
from networkx import Graph
from precice_config_graph.nodes import ParticipantNode, MeshNode

from preciceconfigchecker.rule import Rule
from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation


class ProvideMeshRule(Rule):
    name = "Provided mesh."

    class UnclaimedMeshViolation(Violation):
        """
            This class handles a mesh not being provided by any participant.
        """
        severity = Severity.ERROR

        def __init__(self, mesh: MeshNode):
            self.mesh = mesh

        def format_explanation(self) -> str:
            return f"The mesh {self.mesh.name} does not get provided by any participant."

        def format_possible_solutions(self) -> list[str]:
            return [f"Please let any participant provide the mesh {self.mesh.name}.",
                    "Otherwise, please remove it to improve readability."]

    class RepeatedlyClaimedMeshViolation(Violation):
        """
            This class handles a mesh being mentioned in a mapping, but multiple participant providing it.
        """

        severity = Severity.ERROR

        def __init__(self, participants: list[ParticipantNode], mesh: MeshNode):
            self.mesh = mesh
            participants_s = sorted(participants, key=lambda participant: participant.name)
            self.names = participants_s[0].name
            for i in range(1, len(participants_s) - 1):
                self.names += ", "
                self.names += participants_s[i].name
            # The last participant has to be connected with "and", the others with a comma.
            self.names += " and "
            # Name of last participant
            self.names += participants_s[-1].name

        def format_explanation(self) -> str:
            return f"The mesh {self.mesh.name} is provided by participants {self.names}."

        def format_possible_solutions(self) -> list[str]:
            return [f"Ensure that only one participant provides {self.mesh.name}."]

    def check(self, graph: Graph) -> list[Violation]:
        violations: list[Violation] = []
        meshes = nx.subgraph_view(graph, filter_node=filter_meshes)
        
        for mesh in meshes.nodes:
            participants = get_participants_of_mesh(graph, mesh)
            if len(participants) == 0:
                # Nobody provides this mesh
                violations.append(self.UnclaimedMeshViolation(mesh))
            elif len(participants) > 1:
                # Multiple participants provide this mesh
                violations.append(self.RepeatedlyClaimedMeshViolation(participants, mesh))

        return violations


def get_participants_of_mesh(graph: Graph, mesh: MeshNode) -> list[ParticipantNode]:
    """
        This method returns the participant(s) who provide(s) the given mesh.
        :param graph: The graph of the preCICE config.
        :param mesh: The mesh of which the participant is needed.
        :return: The participants who provide the mesh, if any.
    """
    participants: list[ParticipantNode] = []
    for node in graph.nodes:
        if isinstance(node, ParticipantNode):
            if mesh in node.provide_meshes:
                participants.append(node)
    # If participant does not exist, this will lead to a violation later
    return participants


def filter_meshes(node) -> bool:
    """
        This method filters mesh nodes.
        :param node: The node to check.
        :return: True, if the node is a mesh-node.
    """
    return isinstance(node, MeshNode)
