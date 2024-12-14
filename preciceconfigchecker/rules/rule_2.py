from typing import List
from rule import Rule
from violation import Violation
from severity import Severity

class Rule_2(Rule):
    class MyViolation(Violation):
        def __init__(self, node_a:str, node_b:str, node_c:str) -> None:
            self.node_a = node_a
            self.node_b = node_b
            self.node_c = node_c

        def format_explanation(self) -> str:
            return f"Something went wrong between {self.node_a}, {self.node_b} and {self.node_c}"
        
        def format_possible_solutions(self) -> List[str]:
            return [f"Delete {self.node_a}",
                    f"Delete {self.node_b}",
                    f"Delete {self.node_c}",
                    f"Connect {self.node_a} and {self.node_b}",
                    f"Connect {self.node_a} and {self.node_c}",
                    f"Connect {self.node_a} and {self.node_b} and {self.node_a} and {self.node_c}"
            ]
    def check(self) -> None:
        #Find violations in the graph and add them to the violations list in Rule.
        self.violations.append(self.MyViolation("Node-G", "Node-H", "Node-I"))
        self.violations.append(self.MyViolation("Node-J", "Node-K", "Node-L"))
    
Rule_2(Severity.WARNING, "No connection between three nodes")