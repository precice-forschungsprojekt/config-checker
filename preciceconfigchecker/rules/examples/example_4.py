from typing import List

from rule import Rule
from severity import Severity
from violation import Violation

class Rule_4(Rule):
    class MyViolation(Violation):
        def __init__(self, node_a:str) -> None:
            self.node_a = node_a

        def format_explanation(self) -> str:
            return f"Something went wrong with {self.node_a}"
        
        def format_possible_solutions(self) -> List[str]:
            return [f"Delete {self.node_a}"
            ]

    severity = Severity.ERROR
    problem = "A node is not connected"

    def check(self, graph) -> None:
        #Find violations in the graph and add them to the violations list in Rule.
        pass
    
Rule_4()