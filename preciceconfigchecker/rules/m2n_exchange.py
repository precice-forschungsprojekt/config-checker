import networkx as nx
from networkx import Graph
from precice_config_graph.nodes import ParticipantNode, M2NNode
from preciceconfigchecker.rule import Rule
from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation


class M2NExchangeRule(Rule):
    name = "M2N Exchange Rule."
    severity = Severity.ERROR

    class MissingM2NEchangeViolation(Violation):
        """
            This class handles a participant not being part of an M2N exchange.
        """

        def __init__(self, participant: ParticipantNode):
            self.participant = participant

        def format_explanation(self) -> str:
            return f"Participant {self.participant.name} is not part of an M2N exchange."

        def format_possible_solutions(self) -> list[str]:
            return [
                f"Please create an M2N exchange between participant {self.participant.name} and another participant.",
                f"Otherwise, please remove participant {self.participant.name} to improve readability."]

    class DuplicateM2NExchangeViolation(Violation):
        """
            This class handles two participants having more than one M2N exchange between them.
        """

        def __init__(self, davik_kang: ParticipantNode, calo_nord: ParticipantNode):
            self.participant1 = davik_kang
            self.participant2 = calo_nord

        def format_explanation(self) -> str:
            return (f"There is more than one M2N exchange between participant {self.participant1.name} and "
                    f"participant {self.participant2.name}.")

        def format_possible_solutions(self) -> list[str]:
            return [f"Please remove duplicate M2N exchanges between participant {self.participant1.name} and "
                    f"participant {self.participant2.name}."]

    def check(self, graph: Graph) -> list[Violation]:
        violations: list[Violation] = []
        m2ns: list[M2NNode] = []
        participants: list[ParticipantNode] = []
        m2n_participants: list[ParticipantNode] = []

        for node in graph.nodes:
            # Collect all participants and all M2N nodes
            if isinstance(node, M2NNode):
                m2ns.append(node)
            elif isinstance(node, ParticipantNode):
                participants.append(node)

        for m2n in m2ns:
            # Collect all participants mentioned in M2N nodes
            m2n_participants.append(m2n.acceptor)
            m2n_participants.append(m2n.connector)
            m2n_participants = list(set(m2n_participants))

        # Check every participant if it gets mentioned in an M2N exchange
        for participant in participants:
            if participant not in m2n_participants:
                violations.append(self.MissingM2NEchangeViolation(participant))
                # Remove this participant to make the following calculations easier
                participants.remove(participant)

        # Check every M2N for duplicates
        for m2n in m2ns:
            m2n_acceptor: ParticipantNode = m2n.acceptor
            m2n_connector: ParticipantNode = m2n.connector
            for k2l in m2ns:
                if m2n != k2l:
                    k2l_acceptor: ParticipantNode = k2l.acceptor
                    k2l_connector: ParticipantNode = k2l.connector
                    # Duplicates with same connector and same acceptor participants
                    if (m2n_acceptor == k2l_acceptor and m2n_connector == k2l_connector
                            and not self.contains_violation(violations, m2n_acceptor, m2n_connector)):
                        violations.append(self.DuplicateM2NExchangeViolation(m2n_acceptor, m2n_connector))
                    # Check for duplicates "in the other direction":
                    # This can be removed if acceptor / connector roles do matter in the future.
                    elif (m2n_acceptor == k2l_connector and m2n_connector == k2l_acceptor
                          and not self.contains_violation(violations, m2n_acceptor, m2n_connector)):
                        violations.append(self.DuplicateM2NExchangeViolation(m2n_acceptor, m2n_connector))

        return violations

    # Helper functions
    def contains_violation(self, violations: list[Violation], participant1: ParticipantNode,
                           participant2: ParticipantNode) -> bool:
        """
            This function tests whether there already exists a DuplicateM2NExchangeViolation between two participants.
            :param violations: The list of violations.
            :param participant1: The first participant.
            :param participant2: The second participant.
            :return: True, if there already exists a DuplicateM2NExchangeViolation between the two participants.
        """
        for violation in violations:
            if isinstance(violation, self.DuplicateM2NExchangeViolation):
                # Check if any DuplicateM2NExchangeViolation contains these two participants
                if violation.participant1 == participant1 and violation.participant2 == participant2:
                    return True
                elif violation.participant1 == participant2 and violation.participant2 == participant1:
                    return True
        return False


M2NExchangeRule()
