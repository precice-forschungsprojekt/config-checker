from typing import List
from rule import Rule
from severity import Severity

class Rule_2(Rule):
    def check(self) -> None:
        #Find violations in the graph and add them to the violations list in Rule.
        self.violations.append(("Node-G", "Node-H", "Node-I"))
        self.violations.append(("Node-J", "Node-K", "Node-L"))

    def format_explanation(self, node_a, node_b, node_c) -> str:
        return f"Something went wrong between {node_a}, {node_b} and {node_c}"
    
    def format_possible_solutions(self, node_a, node_b, node_c) -> List[str]:
        return [f"Delete {node_a}",
                f"Delete {node_b}",
                f"Delete {node_c}",
                f"Connect {node_a} and {node_b}",
                f"Connect {node_a} and {node_c}",
                f"Connect {node_a} and {node_b} and {node_a} and {node_c}"
        ]
    
Rule_2(Severity.WARNING, "No connection between three nodes")