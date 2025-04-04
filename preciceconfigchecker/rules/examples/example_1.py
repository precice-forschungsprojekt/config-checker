from rule import Rule
from severity import Severity
from violation import Violation


class Rule_1(Rule):
    class MyViolation(Violation):
        def __init__(self, node_a: str, node_b: str, line: int) -> None:
            self.node_a = node_a
            self.node_b = node_b
            super().__init__(line)

        def format_explanation(self) -> str:
            return f"Something went wrong between {self.node_a} and {self.node_b}"

        def format_possible_solutions(self) -> list[str]:
            return [f"Delete {self.node_a}",
                    f"Delete {self.node_b}",
                    f"Connect {self.node_a} and {self.node_b}"
                    ]

    severity = Severity.WARNING
    name = "1st Example Rule"

    def check(self, graph) -> list[Violation]:
        #Find violations in the graph and return them.
        violations = [
            self.MyViolation("Node-A", "Node-B", 1)
        ]
        # ...
        violations.append(self.MyViolation("Node-C", "Node-D", 2))
        # ...
        violations.append(self.MyViolation("Node-E", "Node-F", 3))
        return violations