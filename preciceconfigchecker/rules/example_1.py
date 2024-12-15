from typing import List
from rule import Rule
from severity import Severity

class Rule_1(Rule):
    def check(self) -> None:
        #Find violations in the graph and add them to the violations list in Rule.
        self.violations.append(("Node-A", "Node-B"))
        self.violations.append(("Node-C", "Node-D"))
        self.violations.append(("Node-E", "Node-F"))

    def format_explanation(self, node_a, node_b) -> str:
        return f"Something went wrong between {node_a} and {node_b}"
    
    def format_possible_solutions(self, node_a, node_b) -> List[str]:
        return [f"Delete {node_a}",
                f"Delete {node_b}",
                f"Connect {node_a} and {node_b}"
        ]
    
Rule_1(Severity.INFO, "No connection between two nodes")