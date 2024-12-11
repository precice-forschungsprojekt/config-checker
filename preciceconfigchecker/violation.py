from typing import List
from abc import ABC, abstractmethod


class Violation(ABC):
    numbers:int = 0 #static attribute: do not use 'self.numbers', use 'Violation.numbers'

    @property
    @abstractmethod
    def explanation(self) -> str: pass

    possible_solutions:List[str] = []

    @abstractmethod
    def __init__(self, args:tuple) -> None: pass
    
    def create_output(self) -> str:
        Violation.numbers += 1
        out:str = f"\n({Violation.numbers:3}.): " + self.explanation
        for possible_solution in self.possible_solutions:
            out += "\n\t- " + possible_solution
        return out