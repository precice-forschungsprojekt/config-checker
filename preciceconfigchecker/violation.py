from abc import ABC, abstractmethod
from typing import List

from preciceconfigchecker.severity import Severity
import preciceconfigchecker.color as c


class Violation(ABC):
    """
    Abstract Class 'Violation'. Creates a formatted string for its attributes.
    """

    line: int = None
    """Attribute: Do not use 'Violation.line', use 'self.line'"""

    @property
    @abstractmethod
    def severity(self) -> Severity:
        """@abstract property: Type"""
        pass

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

    def format(self, debug:bool) -> str:
        """
        Formats the 'Violation' for its attributes.
        If debug mode is enabled, violations with DEBUG severity are also formatted.

        Args:
            debug (bool): for debug mode.

        Returns:
            str: formatted 'Violation'
        """
        severity_info:str = f"[{self.severity.value}]: "
        class_name:str = f"({c.dyeing(self.__class__.__name__, c.purple)}) " if debug else ""
        existing_line: str = f"(Line {self.line}) " if self.line else ""
        explanation: str = self.format_explanation()
        possible_solutions: List[str] = self.format_possible_solutions()

        out: str = c.dyeing(" >>> ", c.cyan) + severity_info + class_name + existing_line + explanation
        for possible_solution in possible_solutions:
            out += c.dyeing("\n     ==> ", c.cyan) + possible_solution
        return out
