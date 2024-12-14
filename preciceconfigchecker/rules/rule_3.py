from typing import List
from rule import Rule
from violation import Violation
from severity import Severity

class Rule_3(Rule):
    class MyViolation(Violation):
        def __init__(self, node_a:str) -> None:
            self.node_a = node_a

        def format_explanation(self) -> str:
            return f"Something went wrong with {self.node_a}"
        
        def format_possible_solutions(self) -> List[str]:
            return [f"Delete {self.node_a}"
            ]

    def check(self) -> None:
        #Find violations in the graph and add them to the violations list in Rule.
        self.violations.append(self.MyViolation("Node-M"))
    
Rule_3(Severity.ERROR, "A node is not connected")