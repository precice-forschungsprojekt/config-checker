from typing import List
from rule import Rule
from severity import Severity

# Implementation of the rule classes and initialization of these objects
# Example 1
class Rule_1(Rule):
    def check_method(self) -> List[tuple[str, str]]:
        result:List[tuple[str, str]] = []
        result.append(("Node-A", "Node-B"))
        result.append(("Node-C", "Node-D"))
        result.append(("Node-E", "Node-F"))
        return result

    def format_explanation(self, node_a, node_b) -> str:
        return f"Something went wrong between {node_a} and {node_b}"
    
    def format_possible_solutions(self, node_a, node_b) -> List[str]:
        possible_solutions:List[str] = []
        possible_solutions.append(f"Delete {node_a}")
        possible_solutions.append(f"Delete {node_b}")
        possible_solutions.append(f"Connect {node_a} and {node_b}")
        return possible_solutions
    
Rule_1(Severity.INFO, "No connection between two nodes")

# Example 2
class Rule_2(Rule):
    def check_method(self) -> List[tuple[str, str, str]]:
        result:List[tuple[str, str, str]] = []
        result.append(("Node-G", "Node-H", "Node-I"))
        result.append(("Node-J", "Node-K", "Node-L"))
        return result

    def format_explanation(self, node_a, node_b, node_c) -> str:
        return f"Something went wrong between {node_a}, {node_b} and {node_c}"
    
    def format_possible_solutions(self, node_a, node_b, node_c) -> List[str]:
        possible_solutions:List[str] = []
        possible_solutions.append(f"Delete {node_a}")
        possible_solutions.append(f"Delete {node_b}")
        possible_solutions.append(f"Delete {node_c}")
        possible_solutions.append(f"Connect {node_a} and {node_b}")
        possible_solutions.append(f"Connect {node_a} and {node_c}")
        possible_solutions.append(f"Connect {node_a} and {node_b} and {node_a} and {node_c}")
        return possible_solutions
    
Rule_2(Severity.WARNING, "No connection between three nodes")

# Example 3
class Rule_3(Rule):
    def check_method(self) -> List[str]:
        result:List[str] = []
        result.append(("Node-M",))
        return result
    
    def format_explanation(self, node_a) -> str:
        return f"Something went wrong with {node_a}"
    
    def format_possible_solutions(self, node_a) -> List[str]:
        possible_solutions:List[str] = []
        possible_solutions.append(f"Delete {node_a}")
        return possible_solutions

Rule_3(Severity.ERROR, "A node is not connected")
