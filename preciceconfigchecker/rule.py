from abc import ABC, abstractmethod
from typing import List
from severity import Severity


class Rule(ABC):
    """
    Abstract Class 'Rule'. Checking a 'Rule' for violations and producing formatted output.
    """

    numbers:int = 0
    """Static Attribute: Do not use 'self.numbers', use 'Rule.numbers'"""

    def __init__(self, severity:Severity, problem:str) -> None:
        """
        Initializes an Rule object.

        Args:
            severity (Severity): Type
            problem (str): Short explanation of what the rule is supposed to check in general.
        """
        self.severity = severity
        self.problem = problem
        self.rule:str
        self.formatted_violations:List[str] = []
        self.violations:List[tuple] = []
        rules.append(self)

    @abstractmethod
    def check_method(self) -> List[tuple]:
        """
        @abstractmethod: Defines how a 'Rule' should be checked

        Returns:
            List[tuple]: of all violations where the 'Rule' was not satisfied.

        Tip: When overwriting, define the type of the tuple for easier use.
        Tip: If the tuple only has one argument, put a comma ( , ) after it so that it is recognized as a tuple. Python specific!
        """
        pass

    @abstractmethod
    def format_explanation(self, data:tuple) -> str:
        """
        @abstractmethod: Formats the explanation of a violation

        Args:
            data (tuple): to use for formatting

        Returns:
            str: formatted

        Tip: When overwriting, multiple arguments can be passed directly, rather than a tuple of arguments.
        Tip: Define the abstract 'check_method' beforehand. Define the types of the tuple there and use these types for the arguments here.
        """
        pass
    
    @abstractmethod
    def format_possible_solutions(self, data:tuple) -> List[str]:
        """
        @abstractmethod: Formats multiple possible solutions to a violation

        Args:
            data (tuple): to use for formatting

        Returns:
            List[str]: of formatted possible solutions

        Tip: When overwriting, multiple arguments can be passed directly, rather than a tuple of arguments.
        Tip: Define the abstract 'check_method' beforehand. Define the types of the tuple there and use these types for the arguments here.
        """
        pass
    
    def satisfied(self) -> bool:
        """
        Shows when the 'Rule' is satisfied

        Returns:
            bool: TRUE if there are no violations after the check
        """
        return (len(self.violations) == 0)
    
    def can_print(self) -> bool:
        """
        Shows if the 'Rule' can print formatted violations

        Returns:
            bool: TRUE if formatted violations are available
        """
        return (len(self.formatted_violations) > 0)
    
    def check(self) -> None:
        """
        Runs the abstract 'check_method' and saves the violations
        """
        self.violations = self.check_method()

    def format_result(self) -> None:
        """
        If the 'Rule' is not satisfied, an output is formatted
        """
        if self.satisfied():
            return
        self.rule = f"[{self.severity.value}]: {self.problem}"
        for data in self.violations:
            explanation:str = self.format_explanation(*data)
            possible_solutions:List[str] = self.format_possible_solutions(*data)
            Rule.numbers += 1
            violation:str = f"({Rule.numbers:3}.): {explanation}"
            for possible_solution in possible_solutions:
                violation += f"\n\t- {possible_solution}"
            self.formatted_violations.append(violation)

    def print_result(self) -> None:
        """
        If the 'Rule' has formatted output, it will be printed
        """
        if not self.can_print():
            return
        print(self.rule)
        for violation in self.formatted_violations:
            print(violation)



# To handle all the rules

rules:List[Rule] = []
"""List of all initialized rules"""

def check_all_rules() -> None:
    """
    Checks all rules for violations
    """
    for rule in rules:
        rule.check()

def format_all_results() -> None:
    """
    Formats the existing violations for all rules
    """
    for rule in rules:
        if not rule.satisfied():
            rule.format_result()

def print_all_results() -> None:
    """
    Prints all existing formatted violations of all rules
    """
    for rule in rules:
        if rule.can_print():
            rule.print_result()