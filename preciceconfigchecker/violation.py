from abc import ABC, abstractmethod
from typing import List

import preciceconfigchecker.color as c


class Violation(ABC):
    """
    Abstract Class 'Violation'. Creates a formatted string for its attributes.
    """

    line: int = None
    """Attribute: Do not use 'Violation.line', use 'self.line'"""

    @abstractmethod
    def __init__(self, line: int) -> None:
        """
        @abstractmethod: Initializes a 'Violation' object.

        Args:
            line (int): The line in the config.xml file of the violation.

        Hint: When overwriting, it is recommended to pass on appropriate attributes.
        Later, these attributes can be called with 'self.attribute'.
        """
        self.line = line

    @abstractmethod
    def format_explanation(self) -> str:
        """
        @abstractmethod: Formats the explanation of 'Violation'.

        Returns:
            str: formatted explanation

        Hint: Use the attributes defined in '__init__()'.
        """
        pass

    @abstractmethod
    def format_possible_solutions(self) -> List[str]:
        """
        @abstractmethod: Formats multiple possible solutions of 'Violation'.

        Returns:
            List[str]: of formatted possible solutions
        
        Hint: Use the attributes defined in '__init__()'.
        """
        pass

    def format(self) -> str:
        """
        Formats the 'Violation' for its attributes.

        Returns:
            str: formatted 'Violation'
        """
        # indent additional lines of the explanation to be aligned with first row after ">>> " is added
        explanation: str = self.format_explanation().replace("\n", "\n     ")
        possible_solutions: List[str] = self.format_possible_solutions()
        existing_line: str = f"(Line {self.line}) " if self.line else ""
        out: str = c.dyeing(" >>> ", c.cyan) + existing_line + explanation
        for possible_solution in possible_solutions:
            out += c.dyeing("\n     ==> ", c.cyan) + possible_solution
        return out
