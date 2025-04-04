from typing import List

import networkx as nx
from networkx import Graph
from precice_config_graph.nodes import ParticipantNode

from preciceconfigchecker.rule import Rule
from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation


class DisjointSimulationsRule(Rule):
    severity = Severity.WARNING
    name = "Couplings must not be disjoint"

    class DisjointSimulationsViolation(Violation):
        participant_sets: frozenset[frozenset[str]]

        def __init__(self, participant_sets: frozenset[frozenset[str]]):
            super()
            assert (len(participant_sets) > 1)
            self.participant_sets = participant_sets

        def format_explanation(self) -> str:
            explanation = f"There are {len(self.participant_sets)} simulations that do not interact with each other. "

            def format_set(set: frozenset[str]) -> str:
                return ", ".join(sorted(set))

            if len(self.participant_sets) == 2:
                [participants_a, participants_b] = list(self.participant_sets)

                participants_a_label = "Participants" if len(participants_a) > 1 else "Participant"
                do_str = "do" if len(participants_a) > 1 else "does"
                participants_b_label = "participants" if len(participants_b) > 1 else "participant"

                explanation += f"{participants_a_label} {format_set(participants_a)} {do_str} not communicate with {participants_b_label} {format_set(participants_b)}."
            else:
                explanation += f"Disjoint groups:"
                for component in self.participant_sets:
                    explanation += f"\n- {format_set(component)}"

            return explanation

        def format_possible_solutions(self) -> List[str]:
            return [
                "Consider splitting up the simulation into multiple configurations to improve maintainability of each simulation.",
                "Add some data to be exchanged between these simulations.",
            ]

    def check(self, graph: Graph) -> list[Violation]:
        def is_participant(node: ParticipantNode) -> bool:
            return isinstance(node, ParticipantNode)

        def has_participant(component) -> bool:
            return any(is_participant(node) for node in component)

        components_with_participant = list(filter(has_participant, nx.connected_components(graph)))

        if len(components_with_participant) > 1:
            participant_sets = frozenset([
                frozenset([participant.name for participant in filter(is_participant, component)])
                for component in components_with_participant
            ])

            return [self.DisjointSimulationsViolation(participant_sets)]
        else:
            return []
