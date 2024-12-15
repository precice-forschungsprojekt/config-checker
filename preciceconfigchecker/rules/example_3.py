from typing import List
from rule import Rule
from severity import Severity

class Rule_3(Rule):
    def check(self) -> None:
        #Find violations in the graph and add them to the violations list in Rule.
        self.violations.append(("Node-M",))
    
    def format_explanation(self, node_a) -> str:
        return f"Something went wrong with {node_a}"
    
    def format_possible_solutions(self, node_a) -> List[str]:
        return [f"Delete {node_a}"
        ]

Rule_3(Severity.ERROR, "A node is not connected")