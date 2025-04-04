from rule import Rule
from severity import Severity
from violation import Violation


class Rule_3(Rule):
    class MyViolation(Violation):
        def __init__(self, node_a: str) -> None:
            self.node_a = node_a

        def format_explanation(self) -> str:
            return f"Something went wrong with {self.node_a}"

        def format_possible_solutions(self) -> list[str]:
            return [f"Delete {self.node_a}"]

    severity = Severity.ERROR
    name = "3rd Example Rule"

    def check(self, graph) -> list[Violation]:
        #Find violations in the graph and return them.
        return [ self.MyViolation("Node-M") ]