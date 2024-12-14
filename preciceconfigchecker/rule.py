from abc import ABC, abstractmethod
from typing import List
from severity import Severity
from violation import Violation


class Rule(ABC):
    """
    Abstract Class 'Rule'. Checking a 'Rule' for violations and producing formatted output.
    """

    def __init__(self, severity:Severity, problem:str) -> None:
        """
        Initializes an Rule object.

        Args:
            severity (Severity): Type
            problem (str): Short explanation of what the rule is supposed to check in general.
        """
        self.severity = severity
        self.problem = problem
        self.violations:List[Violation] = []
        rules.append(self)

    @abstractmethod
    def check(self) -> None:
        """
        @abstractmethod: Defines how a 'Rule' should be checked

        Tip: Use 'self.violations.append(self.MyViolation(...))' to save the results directly. MyViolation should be an inner class of type Violation.
        """
        pass
    
    def satisfied(self) -> bool:
        """
        Shows when the 'Rule' is satisfied

        Returns:
            bool: TRUE if there are no violations after the check
        """
        return (self.violations.__len__() == 0)

    def print_result(self) -> None:
        """
        If the 'Rule' has violations, these will be printed.
        """
        if self.satisfied():
            return
        print(f"[{self.severity.value}]: {self.problem}")
        for violation in self.violations:
            formatted_violation = violation.format()
            print(formatted_violation)



# To handle all the rules

rules:List[Rule] = []
"""List of all initialized rules. Info: Each rule puts itself on this list when initialized."""

def check_all_rules() -> None:
    """
    Checks all rules for violations
    """
    for rule in rules:
        rule.check()

def print_all_results() -> None:
    """
    Prints all existing violations of all rules
    """
    for rule in rules:
        if not rule.satisfied():
            rule.print_result()