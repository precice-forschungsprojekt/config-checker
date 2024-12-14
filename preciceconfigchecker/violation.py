from abc import ABC, abstractmethod
from typing import List

class Violation(ABC):
    """
    Abstract Class 'Violation'. Creates a formatted string for its attributes.
    """

    counter:int = 0
    """Static Attribute: Do not use 'self.counter', use 'Violation.counter'"""

    @abstractmethod
    def __init__(self) -> None:
        """
        @abstractmethod: Initializes an 'Violation' object.

        Tip: When overwriting, it is recommended to pass on appropriate attributes. Later these attributes can be called with 'self.attribute'.
        """
        pass

    @abstractmethod
    def format_explanation(self) -> str:
        """
        @abstractmethod: Formats the explanation of 'Violation'.

        Returns:
            str: formatted explanation

        Tip: Use the attributes defined in '__init__()'.
        """
        pass

    @abstractmethod
    def format_possible_solutions(self) -> List[str]:
        """
        @abstractmethod: Formats multiple possible solutions of 'Violation'.

        Returns:
            List[str]: of formatted possible solutions
        
        Tip: Use the attributes defined in '__init__()'.
        """
        pass

    def format(self) -> str:
        """
        Formats the 'Violation' for its attributes.

        Returns:
            str: formatted 'Violation'
        """
        explanation:str = self.format_explanation()
        possible_solutions:List[str] = self.format_possible_solutions()
        Violation.counter += 1
        out:str = f"({Violation.counter:3}.): {explanation}"
        for possible_solution in possible_solutions:
                out += f"\n\t- {possible_solution}"
        return out