from networkx.classes import Graph
from precice_config_graph.nodes import ParticipantNode, MeshNode, MappingNode, Direction, MappingConstraint, \
    MappingMethod, CouplingSchemeNode, MultiCouplingSchemeNode, CouplingSchemeType, ExchangeNode, M2NNode, \
    WriteDataNode, \
    ReadDataNode
from preciceconfigchecker.rule_utils import rule_error_message
from preciceconfigchecker.rule import Rule
from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation


class MappingRule(Rule):
    name = "Mapping rules."

    class SameParticipantMappingViolation(Violation):
        """
            This class handles a mapping between two meshes of the same participant being specified.
        """
        severity = Severity.ERROR

        def __init__(self, participant: ParticipantNode, mesh: MeshNode, direction: Direction):
            self.participant = participant
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"

        def format_explanation(self) -> str:
            out: str = (f"The participant {self.participant.name} is specifying a {self.direction.value}-mapping "
                        f"{self.connecting_word} mesh {self.mesh.name}, which is his own mesh.")
            out += f"The mapping is from participant {self.participant.name} to participant {self.participant.name}."
            return out

        def format_possible_solutions(self) -> list[str]:
            return [f"Please change the {self.connecting_word}-mesh to a mesh by a different participant.",
                    "Otherwise, please remove the mapping to improve readability."]

    class IncorrectExchangeMappingViolation(Violation):
        """
            This class handles two participants specifying a mapping between them, but only an incorrect exchange
            alongside it, i.e., no exchange on the mesh indicated by the mapping.
        """
        severity = Severity.ERROR

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"

        def format_explanation(self) -> str:
            out: str = (f"The participant {self.parent.name} is specifying a {self.direction.value}-mapping "
                        f"{self.connecting_word} participant {self.stranger.name}, but the exchange in the coupling-"
                        f"scheme between them is incorrect.")
            out += (
                f"\nFor a {self.direction.value}-mapping, the mesh {self.mesh.name} should be used to exchange "
                f"data and the participant specifying the {self.connecting_word}-mesh should be the "
                f"{self.connecting_word}-participant in the exchange.")
            return out

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            # In a 'read' mapping, the 'from' mesh is by Stranger => Stranger should be from-participant in exchange.
            if self.direction == Direction.READ:
                out += [f"Add an exchange from participant {self.stranger.name} to participant {self.parent.name}, "
                        f"which uses participant {self.stranger.name}'s mesh {self.mesh.name} to the coupling-scheme "
                        f"between them."]
            # In a 'write' mapping, the 'to' mesh is by Stranger => Stranger should be to-participant in exchange.
            elif self.direction == Direction.WRITE:
                out += [f"Add an exchange from participant {self.parent.name} to participant {self.stranger.name}, "
                        f"which uses participant {self.stranger.name}'s mesh {self.mesh.name}, to the coupling-scheme "
                        f"between them."]
            return out

    class MissingExchangeMappingViolation(Violation):
        """
            This class handles two participants specifying a mapping between them, but no exchange alongside it,
            i.e., no exchange between the two.
        """
        severity = Severity.ERROR

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"

        def format_explanation(self) -> str:
            out: str = (f"The participant {self.parent.name} is specifying a {self.direction.value}-mapping "
                        f"{self.connecting_word} participant {self.stranger.name}'s mesh {self.mesh.name}, "
                        f"but there is no exchange for it in the coupling-scheme between them.")
            out += (f"\nFor a {self.direction.value}-mapping, the mesh {self.mesh.name} should be used to "
                    f"exchange data.")
            return out

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            # In a 'read' mapping, the 'from' mesh is by Stranger => Stranger should be from-participant in exchange.
            if self.direction == Direction.READ:
                out += [f"Add an exchange from participant {self.stranger.name} to participant {self.parent.name}, "
                        f"which uses participant {self.stranger.name}'s mesh {self.mesh.name} to the coupling-scheme "
                        f"between them."]
            # In a 'write' mapping, the 'to' mesh is by Stranger => Stranger should be to-participant in exchange.
            elif self.direction == Direction.WRITE:
                out += [f"Add an exchange from participant {self.parent.name} to participant {self.stranger.name}, "
                        f"which uses participant {self.stranger.name}'s mesh {self.mesh.name} to the coupling-scheme "
                        f"between them."]
            return out

    class MissingCouplingSchemeMappingViolation(Violation):
        """
            This class handles two participants specifying a mapping between them, but no coupling-scheme alongside it,
            i.e., no coupling-scheme exists between the two to exchange data.
        """
        severity = Severity.ERROR

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"

        def format_explanation(self) -> str:
            return (f"The participant {self.parent.name} is specifying a {self.direction.value}-mapping "
                    f"{self.connecting_word} participant {self.stranger.name}, but there does not exist a "
                    f"coupling-scheme between them.")

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            out += [f"Create a coupling-scheme between participants {self.parent.name} and {self.stranger.name} with an"
                    f"exchange to exchange data between them."]
            out += ["Otherwise, please remove the mapping to improve readability."]
            return out

    class MissingM2NMappingViolation(Violation):
        """
            This class handles two participants specifying a mapping between them, but no m2n-exchange alongside it,
            i.e., no m2n-exchange exists between the two to exchange data.
        """
        severity = Severity.ERROR

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"

        def format_explanation(self) -> str:
            return (f"The participant {self.parent.name} is specifying a {self.direction.value}-mapping "
                    f"{self.connecting_word} participant {self.stranger.name}, but there does not exist an "
                    f"m2n-exchange between them.")

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            out += [f"Create an m2n-exchange between participants {self.parent.name} and {self.stranger.name}"
                    f" to exchange data between them."]
            out += ["Otherwise, please remove the mapping to improve readability."]
            return out

    class ParallelCouplingMappingFormatViolation(Violation):
        """
            This class handles a mapping being specified by two participants which are running in parallel,
            i.e., they are both in the same parallel-coupling-scheme. For such participants, only the mapping
            formats read-consistent and write-conservative are allowed.
        """
        severity = Severity.ERROR

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode,
                     mesh_parent: MeshNode, mesh_stranger, direction: Direction, constraint: MappingConstraint):
            self.parent = parent
            self.stranger = stranger
            self.mesh_parent = mesh_parent
            self.mesh_stranger = mesh_stranger
            self.direction = direction
            self.constraint = constraint

        def format_explanation(self) -> str:
            out: str = f"The participants {self.parent.name} and {self.stranger.name} are executing in parallel."
            out += (
                f"\nThe {self.direction.value}-mapping specified by participant {self.parent.name} on meshes "
                f"{self.mesh_parent.name} and {self.mesh_stranger.name} with constraint=\"{self.constraint.value}\" "
                f"is is invalid.")
            out += (
                "\nFor parallel participants, only mappings of the form read-consistent and write-conservative are "
                "allowed.")
            return out

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            # Mapping format is "almost" correct
            if self.direction == Direction.READ and self.constraint == MappingConstraint.CONSERVATIVE:
                out += [
                    f"Consider changing either the direction of the mapping between participants {self.parent.name} and "
                    f"{self.stranger.name} to direction=\"write\" or the constraint of the mapping to constraint="
                    f"\"consistent\"."]
                out += [f"The effect of a read-conservative mapping can be achieved by moving the mapping from "
                        f"participant {self.parent.name} to participant {self.stranger.name} and changing its direction "
                        f"to \"write\"."]
                out += [f"When moving the mapping, remember to update the <exchange .../> tag in the participants "
                        f"coupling-scheme."]
            elif self.direction == Direction.WRITE and self.constraint == MappingConstraint.CONSISTENT:
                out += [
                    f"Consider changing either the direction of the mapping between participants {self.parent.name} and "
                    f"{self.stranger.name} to direction=\"read\" or the constraint of the mapping to constraint="
                    f"\"conservative\"."]
                out += [f"The effect of a write-consistent mapping can be achieved by moving the mapping from "
                        f"participant {self.parent.name} to participant {self.stranger.name} and changing its direction "
                        f"to \"read\"."]
                out += [f"When moving the mapping, remember to update the <exchange .../> tag in the participants "
                        f"coupling-scheme."]
            # Generic answers for arbitrary constraints
            elif self.direction == Direction.READ:
                out += [f"Consider changing the constraint of the mapping between participants {self.parent.name} and "
                        f"{self.stranger.name} from \"{self.constraint.value}\" to \"consistent\"."]
            elif self.direction == Direction.WRITE:
                out += [f"Consider changing the constraint of the mapping between participants {self.parent.name} and "
                        f"{self.stranger.name} from \"{self.constraint.value}\" to \"conservative\"."]
            return out

    class MappingDirectionViolation(Violation):
        """
            This class handles a mapping being specified by two participants, but the to- and from-meshes not being
            according to the specified mapping direction.
        """
        severity = Severity.ERROR

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode,
                     mesh_parent: MeshNode, mesh_stranger: MeshNode, direction: Direction):
            self.parent = parent
            self.stranger = stranger
            self.mesh_parent = mesh_parent
            self.mesh_stranger = mesh_stranger
            self.direction = direction
            if self.direction == Direction.READ:
                # X reads "from" Y
                self.connecting_word = "from"
                self.inverse_connector = "to"
                self.inverse_direction = Direction.WRITE
            elif self.direction == Direction.WRITE:
                # X writes "to" Y
                self.connecting_word = "to"
                self.inverse_connector = "from"
                self.inverse_direction = Direction.READ

        def format_explanation(self) -> str:
            out: str = (f"The {self.direction.value}-mapping of participant {self.parent.name} and mesh "
                        f"{self.mesh_parent.name} {self.connecting_word} participant {self.stranger.name} and "
                        f"mesh {self.mesh_stranger.name} is in the wrong direction.")
            out += (f"\nIn {self.direction.value}-mappings, the {self.inverse_connector}=\"mesh\" has to be on a "
                    f"mesh that the participant provides.")
            return out

        def format_possible_solutions(self) -> list[str]:
            sol: list[str] = []
            sol += [
                f"Either change direction=\"{self.direction.value}\" to direction=\"{self.inverse_direction.value}\""
                f", or swap meshes {self.mesh_parent.name} and {self.mesh_stranger.name}."]
            sol += [f"Move the mapping from participant {self.parent.name} to participant "
                    f"{self.stranger.name}, change its direction and remember to switch the mesh used in the "
                    f"<exchange .../> tag in their coupling scheme."]
            sol += ["Otherwise, please remove it to improve readability."]
            return sol

    class MappingMissingDataProcessingViolation(Violation):
        """
            This class handles a "regular" mapping being specified by a participant, but no corresponding
            read- or write-data element being specified.
        """
        severity = Severity.ERROR

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh_parent: MeshNode,
                     mesh_stranger: MeshNode, direction: Direction):
            self.parent = parent
            self.stranger = stranger
            self.mesh_parent = mesh_parent
            self.mesh_stranger = mesh_stranger
            self.direction = direction
            if self.direction == Direction.READ:
                self.connecting_word = "from"
                self.inverse_connector = "to"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"
                self.inverse_connector = "from"

        def format_explanation(self) -> str:
            return (f"Participant {self.parent.name} is specifying a {self.direction.value}-mapping "
                    f"{self.connecting_word} participant {self.stranger.name}'s mesh {self.mesh_stranger.name} "
                    f"{self.inverse_connector} participant {self.parent.name}'s mesh {self.mesh_parent.name}, but does "
                    f"not define a corresponding {self.direction.value}-data element on mesh {self.mesh_parent.name}.")

        def format_possible_solutions(self) -> list[str]:
            return [f"Please add a {self.direction.value}-data element to participant {self.parent.name}, which uses "
                    f"mesh {self.mesh_parent.name} by participant {self.parent.name}.",
                    "Otherwise, please remove the mapping to improve readability."]

    class JustInTimeMappingApiAccessViolation(Violation):
        """
            This class handles a participant (parent) specifying a just-in-time mapping with another participant
            (stranger), but the parent not having permission to read from/write to Stranger's mesh, i.e., Parent does
            not receive the mesh with api-access=true.
        """
        severity = Severity.ERROR

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            self.connecting_word: str = ""
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"

        def format_explanation(self) -> str:
            return (f"The participant {self.parent.name} is specifying a just-in-time {self.direction.value}-"
                    f"mapping {self.connecting_word} participant {self.stranger.name}'s mesh {self.mesh.name}, but "
                    f"does not have access to it.")

        def format_possible_solutions(self) -> list[str]:
            return [f"Let participant {self.parent.name} receive mesh {self.mesh.name} from participant "
                    f"{self.stranger.name} with the attribute api-access=\"true\".",
                    f"Map the values from mesh {self.mesh.name} to a mesh by participant {self.parent.name}, before"
                    f" {self.direction.value}ing them.",
                    "Otherwise, please remove it to improve readability."]

    class JustInTimeMappingFormatViolation(Violation):
        """
            This class handles a just-in-time mapping being specified between two participants. For such mappings,
            only the formats read-consistent and write-conservative are allowed.
        """
        severity = Severity.ERROR

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode,
                     direction: Direction,
                     constraint: MappingConstraint):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            self.connecting_word: str = ""
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"
            self.constraint = constraint

        def format_explanation(self) -> str:
            out: str = (
                f"The just-in-time {self.direction.value}-mapping of participant {self.parent.name} {self.connecting_word} "
                f"participant {self.stranger.name}'s mesh {self.mesh.name} is in direction="
                f"\"{self.direction.value}\" and has constraint=\"{self.constraint.value}\", which is invalid.")
            out += (
                "\nCurrently, only just-in-time mappings of the form read-consistent and write-conservative are "
                "supported.")
            return out

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            # Mapping format is "almost" correct
            if self.direction == Direction.READ and self.constraint == MappingConstraint.CONSERVATIVE:
                out += [
                    f"Consider changing either the direction of the mapping between participants {self.parent.name} and "
                    f"{self.stranger.name} to direction=\"write\" or the constraint of the mapping to constraint="
                    f"\"consistent\"."]
                out += [f"The effect of a read-conservative mapping can be achieved by moving the mapping from "
                        f"participant {self.parent.name} to participant {self.stranger.name} and changing its direction "
                        f"to \"write\"."]
                out += [f"When moving the mapping, remember to update the <exchange .../> tag in the participants "
                        f"coupling-scheme."]
            elif self.direction == Direction.WRITE and self.constraint == MappingConstraint.CONSISTENT:
                out += [
                    f"Consider changing either the direction of the mapping between participants {self.parent.name} and "
                    f"{self.stranger.name} to direction=\"read\" or the constraint of the mapping to constraint="
                    f"\"conservative\"."]
                out += [f"The effect of a write-consistent mapping can be achieved by moving the mapping from "
                        f"participant {self.parent.name} to participant {self.stranger.name} and changing its direction "
                        f"to \"read\"."]
                out += [f"When moving the mapping, remember to update the <exchange .../> tag in the participants "
                        f"coupling-scheme."]
            # Generic answers for arbitrary constraints
            elif self.direction == Direction.READ:
                out += [f"Consider changing the constraint of the mapping between participants {self.parent.name} and "
                        f"{self.stranger.name} from \"{self.constraint.value}\" to \"consistent\"."]
            elif self.direction == Direction.WRITE:
                out += [f"Consider changing the constraint of the mapping between participants {self.parent.name} and "
                        f"{self.stranger.name} from \"{self.constraint.value}\" to \"conservative\"."]
            return out

    class JustInTimeMappingDirectionViolation(Violation):
        """
            This class handles a just-in-time mapping being specified between two participants, but the to- or from-mesh
            not being according to the specified mapping direction.
        """
        severity = Severity.ERROR

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                # X reads "from" Y
                self.connecting_word = "from"
                self.inverse_direction = Direction.WRITE
            elif self.direction == Direction.WRITE:
                # X writes "to" Y
                self.connecting_word = "to"
                self.inverse_direction = Direction.READ

        def format_explanation(self) -> str:
            out: str = (f"The just-in-time {self.direction.value}-mapping of participant {self.parent.name} "
                        f"{self.connecting_word} participant {self.stranger.name} and mesh {self.mesh.name} is in "
                        f"the wrong direction.")
            out += (
                f"\nIn just-in-time{self.direction.value}-mappings, the {self.connecting_word}=\"mesh\" has to "
                f"be on a stranger participants mesh.")
            return out

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            out += [f"Change direction=\"{self.direction.value}\" to direction=\"{self.inverse_direction.value}\"."]
            out += [f"Move the mapping from participant {self.parent.name} to participant "
                    f"{self.stranger.name} and change its direction and remember to switch the mesh used in the "
                    f"<exchange .../> tag in their coupling scheme."]
            out += [f"Otherwise, change the {self.connecting_word}-mesh to a mesh by participant {self.stranger.name}."]
            return out

    class JustInTimeMappingFormatDirectionViolation(Violation):
        """
            This class handles a just-in-time mapping being specified between two participants, but the to- or from-mesh
            not being according to the specified mapping direction and the format not being either read-consistent or
            write-conservative.
        """
        severity = Severity.ERROR

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction,
                     constraint: MappingConstraint):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                self.connecting_word = "from"
                self.inverse_direction = Direction.WRITE
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"
                self.inverse_direction = Direction.READ
            self.constraint = constraint

        def format_explanation(self) -> str:
            out: str = (
                f"The just-in-time {self.direction.value}-mapping with constraint \"{self.constraint.value}\" between "
                f"participant {self.parent.name} and participant {self.stranger.name}'s mesh {self.mesh.name} has an "
                f"invalid format and is in the wrong direction.")
            out += (
                f"\nCurrently, only the formats \"write-conservative\" and \"read-consistent\" are implemented for "
                f"just-in-time mappings.")
            out += (
                f"\nIn just-in-time {self.direction.value}-mappings, the {self.connecting_word}=\"mesh\" has to "
                f"be on a stranger participants mesh.")
            return out

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            out += [f"Change direction=\"{self.direction.value}\" to direction=\"{self.inverse_direction.value}\"."]
            out += [f"Move the mapping from participant {self.parent.name} to participant "
                    f"{self.stranger.name}, change its direction and remember to switch the mesh used in the "
                    f"<exchange .../> tag in their coupling scheme."]
            if self.direction == Direction.WRITE:
                out += [f"Please update the constraint of the mapping between participants {self.parent.name} and "
                        f"{self.stranger.name} from \"{self.constraint.value}\" to \"conservative\"."]
            elif self.direction == Direction.READ:
                out += [f"Please update the constraint of the mapping between participants {self.parent.name} and "
                        f"{self.stranger.name} from \"{self.constraint.value}\" to \"consistent\"."]
            out += [f"Otherwise, change the {self.connecting_word}-mesh to a mesh by participant {self.stranger.name}."]
            return out

    class JustInTimeMappingMethodViolation(Violation):
        """
            This class handles a just-in-time mapping being specified between two participants,
            but its mapping-method is incorrect.
            Currently, for just-time-mappings, only the mapping-methods nearest-neighbor, rbf-pum-direct and rbf are
            supported.
        """
        severity = Severity.ERROR

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction,
                     method: MappingMethod):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"
            self.method = method

        def format_explanation(self) -> str:
            out: str = (
                f"The just-in-time {self.direction.value}-mapping of participant {self.parent.name} {self.connecting_word} "
                f"{self.stranger.name}'s mesh {self.mesh.name} has mapping-method \"{self.method.value}\", which is invalid.")
            out += (
                "\nCurrently, only just-in-time mappings with methods \"nearest-neighbor\", \"rbf-pum-direct\" and "
                "\"rbf\" are supported.")
            return out

        def format_possible_solutions(self) -> list[str]:
            return [f"Please change the method of the mapping from \"{self.method.value}\" to one of the methods "
                    f"\"nearest-neighbor\", \"rbf-pum-direct\" or \"rbf\"."]

    class JustInTimeMappingMissingDataProcessingViolation(Violation):
        """
            This class handles a just-time-mapping being specified by a participant, but no corresponding
            read- or write-data element being specified.
        """
        severity = Severity.ERROR

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"

        def format_explanation(self) -> str:
            return (f"Participant {self.parent.name} is specifying a just-in-time {self.direction.value}-mapping "
                    f"{self.connecting_word} participant {self.stranger.name}'s mesh {self.mesh.name}, but does not "
                    f"define a corresponding {self.direction.value}-data element on mesh {self.mesh.name}.")

        def format_possible_solutions(self) -> list[str]:
            return [f"Please add a {self.direction.value}-data element to participant {self.parent.name}, which uses "
                    f"mesh {self.mesh.name} by participant {self.stranger.name}.",
                    "Otherwise, please remove the mapping to improve readability."]

    def check(self, graph: Graph) -> list[Violation]:
        violations: list[Violation] = []

        m2ns: list[M2NNode] = filter_m2n_nodes(graph)
        couplings: list[CouplingSchemeNode | MultiCouplingSchemeNode] = filter_coupling_nodes(graph)
        parallel_couplings: list[CouplingSchemeNode | MultiCouplingSchemeNode] = filter_parallel_coupling_nodes(graph)

        mappings: list[MappingNode] = filter_mapping_nodes(graph)
        for mapping in mappings:
            method: MappingMethod = mapping.method
            direction: Direction = mapping.direction
            constraint: MappingConstraint = mapping.constraint
            participant_parent: ParticipantNode = mapping.parent_participant
            # Initialize to avoid keeping value for multiple iterations (mappings)
            mesh_parent: MeshNode = None
            mesh_stranger: MeshNode = None

            # Determine which tags exist and thus which meshes belong to which participant
            if mapping.just_in_time:
                # Either 'to' or 'from' tag does not exist in JIT mappings
                if mapping.from_mesh and not mapping.to_mesh:
                    mesh_stranger = mapping.from_mesh
                elif not mapping.from_mesh and mapping.to_mesh:
                    mesh_stranger = mapping.to_mesh
                else:
                    rule_error_message("Mapping must have attribute \"to\" or \"from\"")

            # "regular" mappings
            else:
                if mapping.from_mesh in participant_parent.provide_meshes:
                    mesh_parent = mapping.from_mesh
                    mesh_stranger = mapping.to_mesh
                elif mapping.to_mesh in participant_parent.provide_meshes:
                    mesh_parent = mapping.to_mesh
                    mesh_stranger = mapping.from_mesh
                else:
                    rule_error_message("One mesh in mapping must be provided by parent participant")

            # These violations are the same for both JIT and regular mappings
            participant_strangers = get_participants_of_mesh(graph, mesh_stranger)

            if len(participant_strangers) == 0:
                # This mapping is broken
                # mesh_stranger is not provided by any participant
                # Gets handled in provide_mesh.py
                continue

            if len(participant_strangers) > 1:
                # This mapping is broken
                # mesh_stranger gets claimed by more than one participant
                # Gets handled in provide_mesh.py
                continue

            # There is only one participant claiming the mesh
            participant_stranger = participant_strangers[0]

            if participant_parent == participant_stranger:
                # This mapping is broken
                # The mapping is between meshes of the same participant
                violations.append(
                    self.SameParticipantMappingViolation(participant_parent, mesh_stranger, direction))
                continue

            # Check JIT mapping specific violations
            if mapping.just_in_time:
                # Only the methods nearest-neighbor, rbf-pum-direct and rbf are supported
                supported_methods = [MappingMethod.NEAREST_NEIGHBOR, MappingMethod.RBF_PUM_DIRECT, MappingMethod.RBF]
                if method not in supported_methods:
                    violations.append(
                        self.JustInTimeMappingMethodViolation(participant_parent, participant_stranger, mesh_stranger,
                                                              direction, method))

                # Only read-consistent and write-conservative are supported
                if direction == Direction.READ:
                    # For a read-mapping, the 'from' mesh needs to be defined
                    if mapping.from_mesh:
                        # Correct direction
                        # For a JIT-read-mapping, the constraint has to be consistent
                        if constraint != MappingConstraint.CONSISTENT:
                            # Correct direction, but wrong constraint
                            violations.append(
                                self.JustInTimeMappingFormatViolation(participant_parent, participant_stranger,
                                                                      mesh_stranger, direction, constraint))
                    else:
                        # Wrong direction
                        if constraint == MappingConstraint.CONSISTENT:
                            # Correct format
                            violations.append(
                                self.JustInTimeMappingDirectionViolation(participant_parent, participant_stranger,
                                                                         mesh_stranger, direction))
                        else:
                            # Wrong format and wrong direction
                            violations.append(
                                self.JustInTimeMappingFormatDirectionViolation(participant_parent, participant_stranger,
                                                                               mesh_stranger, direction, constraint))
                elif direction == Direction.WRITE:
                    # For a write-mapping, the 'to' mesh needs to be defined
                    if mapping.to_mesh:
                        # Correct direction
                        # For a JIT-write-mapping, the constraint has to be conservative
                        if constraint != MappingConstraint.CONSERVATIVE:
                            # Correct direction, but wrong constraint
                            violations.append(
                                self.JustInTimeMappingFormatViolation(participant_parent, participant_stranger,
                                                                      mesh_stranger, direction, constraint))
                    else:
                        # Wrong direction
                        if constraint == MappingConstraint.CONSERVATIVE:
                            # Correct format
                            violations.append(
                                self.JustInTimeMappingDirectionViolation(participant_parent, participant_stranger,
                                                                         mesh_stranger, direction))
                        else:
                            # Wrong format and wrong direction
                            violations.append(
                                self.JustInTimeMappingFormatDirectionViolation(participant_parent, participant_stranger,
                                                                               mesh_stranger, direction, constraint))

                # Check if participant receives mesh with api-access="true"
                receive_meshes = mapping.parent_participant.receive_meshes
                for receive_mesh in receive_meshes:
                    if receive_mesh.mesh == mesh_stranger:
                        # If api-access != true, then participant does not have permission to read from/write to it
                        if not receive_mesh.api_access:
                            violations.append(
                                self.JustInTimeMappingApiAccessViolation(participant_parent, participant_stranger,
                                                                         mesh_stranger, direction))
                if direction == Direction.WRITE:
                    write_datas: list[WriteDataNode] = participant_parent.write_data
                    if len(write_datas) == 0:
                        violations.append(
                            self.JustInTimeMappingMissingDataProcessingViolation(participant_parent,
                                                                                 participant_stranger,
                                                                                 mesh_stranger, direction))
                    if len(write_datas) > 0 and not any(
                            data_processing_belongs_to_mapping(write_data, mesh_stranger) for write_data in
                            write_datas):
                        # Data gets mapped but not written
                        violations.append(
                            self.JustInTimeMappingMissingDataProcessingViolation(participant_parent,
                                                                                 participant_stranger,
                                                                                 mesh_stranger, direction))
                elif direction == Direction.READ:
                    read_datas: list[ReadDataNode] = participant_parent.read_data
                    if len(read_datas) == 0:
                        violations.append(
                            self.JustInTimeMappingMissingDataProcessingViolation(participant_parent,
                                                                                 participant_stranger,
                                                                                 mesh_stranger, direction))
                    if len(read_datas) > 0 and not any(
                            data_processing_belongs_to_mapping(read_data, mesh_stranger) for read_data in read_datas):
                        # Data gets mapped, but not read
                        violations.append(
                            self.JustInTimeMappingMissingDataProcessingViolation(participant_parent,
                                                                                 participant_stranger,
                                                                                 mesh_stranger, direction))
            # Only regular mappings here
            else:
                if direction == Direction.READ:
                    # In a read-mapping, the 'to'-mesh has to be by the parent, the 'from'-mesh by Stranger
                    if not mesh_parent == mapping.to_mesh:
                        violations.append(
                            self.MappingDirectionViolation(participant_parent, participant_stranger, mesh_parent,
                                                           mesh_stranger, direction))
                elif direction == Direction.WRITE:
                    # In a write-mapping, the 'from'-mesh has to be by the parent, the 'to'-mesh by stranger
                    if not mesh_parent == mapping.from_mesh:
                        violations.append(
                            self.MappingDirectionViolation(participant_parent, participant_stranger, mesh_parent,
                                                           mesh_stranger, direction))

                # Check if there is a corresponding read-/write-data element for the mapping
                if direction == Direction.WRITE:
                    write_datas: list[WriteDataNode] = participant_parent.write_data
                    if len(write_datas) == 0:
                        # In a write-mapping, Parent has to write the data
                        violations.append(
                            self.MappingMissingDataProcessingViolation(participant_parent, participant_stranger,
                                                                       mesh_parent, mesh_stranger, direction))
                    # In a write-mapping, Parent should write to their own mesh
                    if len(write_datas) > 0 and not any(
                            data_processing_belongs_to_mapping(write_data, mesh_parent) for write_data in write_datas):
                        violations.append(
                            self.MappingMissingDataProcessingViolation(participant_parent, participant_stranger,
                                                                       mesh_parent, mesh_stranger, direction))
                elif direction == Direction.READ:
                    read_datas: list[ReadDataNode] = participant_parent.read_data
                    if len(read_datas) == 0:
                        # In a read mapping, Parent should read data
                        violations.append(
                            self.MappingMissingDataProcessingViolation(participant_parent, participant_stranger,
                                                                       mesh_parent, mesh_stranger, direction))
                    # In a read-mapping, Parent should read from their own mesh
                    if len(read_datas) > 0 and not any(
                            data_processing_belongs_to_mapping(read_data, mesh_parent) for read_data in read_datas):
                        violations.append(
                            self.MappingMissingDataProcessingViolation(participant_parent, participant_stranger,
                                                                       mesh_parent, mesh_stranger, direction))

            # Both JIT and regular mappings share these violations
            # Check for correct m2n between mapping participants
            m2n = get_m2n_of_participants(m2ns, participant_parent, participant_stranger)
            if not m2n:
                violations.append(
                    self.MissingM2NMappingViolation(participant_parent, participant_stranger,
                                                    mesh_stranger, direction))

            # Check if mapping-participants also have a coupling scheme and then also an exchange
            coupling = get_coupling_scheme_of_mapping(couplings, participant_parent, participant_stranger)
            if not coupling:
                # Participants try to map data, but there exists no coupling scheme between them
                violations.append(
                    self.MissingCouplingSchemeMappingViolation(participant_parent, participant_stranger,
                                                               mesh_stranger, direction))
                # Continue with the next mapping; this one cannot cause more violations
                continue

            # Regular mappings between parallel participants have to be either read-consistent or write-conservative
            if not mapping.just_in_time:
                # Check if the coupling-scheme between the participants is parallel
                if coupling in parallel_couplings:
                    # Now, check whether it has the correct format: Only read-consistent and write-conservative are
                    #  allowed for parallel couplings
                    if direction == Direction.READ:
                        if not constraint == MappingConstraint.CONSISTENT:
                            violations.append(
                                self.ParallelCouplingMappingFormatViolation(participant_parent,
                                                                            participant_stranger, mesh_parent,
                                                                            mesh_stranger, direction, constraint))
                    elif direction == Direction.WRITE:
                        if not constraint == MappingConstraint.CONSERVATIVE:
                            violations.append(
                                self.ParallelCouplingMappingFormatViolation(participant_parent,
                                                                            participant_stranger, mesh_parent,
                                                                            mesh_stranger, direction, constraint))
            # Both JIT and regular mappings
            exchanges = get_exchange_of_participants(participant_parent, participant_stranger, coupling)
            if not exchanges:
                # Participants try to map data, and there exists a coupling-scheme between them, but not any exchanges
                violations.append(
                    self.MissingExchangeMappingViolation(participant_parent, participant_stranger, mesh_stranger,
                                                         direction))
                # Continue with the next mapping; this one cannot cause more violations
                continue
            # Check if any exchange of the participants coupling-scheme is “correct”, i.e., on the strangers mesh
            if not any(exchange_belongs_to_mapping(exchange, direction, participant_stranger, mesh_stranger) for
                       exchange in exchanges):
                # No correct exchange, i.e., using correct mesh
                violations.append(
                    self.IncorrectExchangeMappingViolation(participant_parent, participant_stranger, mesh_stranger,
                                                           direction))

        return violations


# Helper functions
def get_m2n_of_participants(m2ns: list[M2NNode], participant_a: ParticipantNode,
                            participant_b: ParticipantNode) -> M2NNode | None:
    """
        This function returns the m2n-node connecting two participants if one exists.
        :param m2ns: All m2n nodes that get searched.
        :param participant_a: The first participant for which the m2n node is needed.
        :param participant_b: The other participant.
        :return: The m2n node between the given participants if it exists, None otherwise.
    """
    for m2n in m2ns:
        if m2n.acceptor == participant_a and m2n.connector == participant_b:
            return m2n
        elif m2n.acceptor == participant_b and m2n.connector == participant_a:
            return m2n
    return None


def data_processing_belongs_to_mapping(data_processing: WriteDataNode | ReadDataNode, mesh: MeshNode) -> bool:
    """
        This function evaluates whether the given data-processing node is valid for a mapping,
        defined by the given mesh.
        It is assumed that the data_processing node is specified by the parent of the mapping,
        and that the mesh is the mesh that would be expected in a correct data_processing.
        :param data_processing: The data-processing node, either a write-data node or a read-data node.
        :param mesh: The mesh that would be expected in a correct data_processing.
        :return: True, if the data-processing node is valid for the mapping, False otherwise.
    """
    return mesh == data_processing.mesh


def exchange_belongs_to_mapping(exchange: ExchangeNode, direction: Direction, participant_stranger: ParticipantNode,
                                mesh_stranger: MeshNode) -> bool:
    """
        Evaluates whether the given exchange is correct for mapping corresponding to the given (stranger) participant,
        his mesh and the direction.

        It is known that the exchange belongs to both participants of the mapping and the given participant is NOT the
        parent of the mapping. Then, participant_stranger, mesh_stranger and direction should be enough to identify
        whether the exchange belongs to the mapping or not.
        :param exchange: The exchange to check.
        :param direction: The direction of the mapping to check.
        :param participant_stranger: The participant which is needed to check whether the exchange belongs to the mapping
        :return: True if the exchange is in the correct direction and uses the correct mesh, False otherwise.
    """
    ex_dir: bool = False
    ex_mesh: bool = False
    if direction == Direction.READ:
        # In a read-mapping, Stranger should correspond to the exchange's from-participant
        if participant_stranger == exchange.from_participant:
            ex_dir = True
            # Otherwise, the direction is false
    elif direction == Direction.WRITE:
        # In a write-mapping, Stranger should correspond to the exchange's to-participant
        if participant_stranger == exchange.to_participant:
            ex_dir = True
            # Otherwise, the direction is false
    # In a mapping, Stranger's mesh should be used
    if mesh_stranger == exchange.mesh:
        ex_mesh = True
        # Otherwise, the mesh used is incorrect
    return ex_dir and ex_mesh


def get_participants_of_mesh(graph: Graph, mesh: MeshNode) -> list[ParticipantNode]:
    """
        This method returns the participant who owns the given mesh.
        :param graph: The graph of the preCICE config.
        :param mesh: The mesh of which the participant is needed.
        :return: The participant who owns the mesh.
    """
    participants: list[ParticipantNode] = []
    for node in graph.nodes:
        if isinstance(node, ParticipantNode):
            if mesh in node.provide_meshes:
                participants.append(node)
    # If participant does not exist, this will lead to a violation later
    return participants


def get_coupling_scheme_of_mapping(couplings: list[CouplingSchemeNode | MultiCouplingSchemeNode],
                                   participant_a: ParticipantNode, participant_b: ParticipantNode,
                                   ) -> CouplingSchemeNode | MultiCouplingSchemeNode | None:
    """
        This method returns the coupling scheme between the given participants.
        :param couplings: All couplings of the preCICE config.
        :param participant_a: One of the participants for which the coupling scheme is needed.
        :param participant_b: The other participant.
        :return:The coupling scheme between the participants; None if there is no coupling-scheme between the participants.
    """
    for coupling in couplings:
        if isinstance(coupling, CouplingSchemeNode):
            if ((participant_a == coupling.first_participant and participant_b == coupling.second_participant) or
                    (participant_b == coupling.first_participant and participant_a == coupling.second_participant)):
                return coupling
        elif isinstance(coupling, MultiCouplingSchemeNode):
            if participant_a in coupling.participants and participant_b in coupling.participants:
                return coupling
    return None


def get_exchange_of_participants(participant_a: ParticipantNode, participant_b: ParticipantNode,
                                 coupling: CouplingSchemeNode | MultiCouplingSchemeNode) -> list[ExchangeNode] | None:
    """
        This method returns the exchange nodes between the given participants in the given coupling-scheme if any exist.
        :param participant_a: One of the participants for which the exchange is needed.
        :param participant_b: The other participant.
        :param coupling: The coupling-scheme between the participants, in which the exchange should exist.
        :return: A list of exchange nodes between the two participants, if any exist, else None.
    """
    exchange_nodes: list[ExchangeNode] = []
    # Both coupling-scheme nodes and multi-coupling-scheme-nodes have the same attribute 'exchanges'
    for exchange in coupling.exchanges:
        if ((participant_a == exchange.to_participant and participant_b == exchange.from_participant) or
                (participant_b == exchange.to_participant and participant_a == exchange.from_participant)):
            exchange_nodes.append(exchange)
    return exchange_nodes if exchange_nodes else None


def filter_mapping_nodes(graph: Graph) -> list[MappingNode]:
    """
        This function returns all mapping nodes of the given graph.
        :param graph:The graph to check.
        :return: All mapping nodes of the graph.
    """
    mappings: list[MappingNode] = []
    for node in graph.nodes:
        if isinstance(node, MappingNode):
            mappings.append(node)
    return mappings


def filter_coupling_nodes(graph: Graph) -> list[CouplingSchemeNode | MultiCouplingSchemeNode]:
    """
        This function returns all coupling-scheme nodes of the given graph.
        :param graph:The graph to check.
        :return: All (multi-)coupling-scheme nodes of the graph.
    """
    couplings: list[CouplingSchemeNode | MultiCouplingSchemeNode] = []
    for node in graph.nodes:
        if isinstance(node, CouplingSchemeNode) or isinstance(node, MultiCouplingSchemeNode):
            couplings.append(node)
    return couplings


def filter_parallel_coupling_nodes(graph: Graph) -> list[CouplingSchemeNode | MultiCouplingSchemeNode]:
    """
        This function returns all parallel coupling-scheme nodes of the given graph.
        :param graph:The graph to check.
        :return: All coupling-scheme-nodes of the graph, which are either of type multi or ...-parallel.
    """
    couplings: list[CouplingSchemeNode | MultiCouplingSchemeNode] = []
    for node in graph.nodes:
        if isinstance(node, CouplingSchemeNode):
            if node.type in [CouplingSchemeType.PARALLEL_EXPLICIT, CouplingSchemeType.PARALLEL_IMPLICIT]:
                couplings.append(node)
        elif isinstance(node, MultiCouplingSchemeNode):
            couplings.append(node)
    return couplings


def filter_m2n_nodes(graph: Graph) -> list[M2NNode]:
    """
        This function returns all m2n nodes of the given graph.
        :param graph:The graph to check.
        :return: All m2n nodes of the graph.
    """
    m2ns: list[M2NNode] = []
    for node in graph.nodes:
        if isinstance(node, M2NNode):
            m2ns.append(node)
    return m2ns
