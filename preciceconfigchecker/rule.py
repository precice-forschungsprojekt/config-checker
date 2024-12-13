from abc import ABC, abstractmethod
from typing import List
from severity import Severity


class Rule(ABC):
    numbers:int = 0 #static attribute: do not use 'self.numbers', use 'Rule.numbers'

    def __init__(self, severity:Severity, problem:str) -> None:
        self.severity = severity
        self.problem = problem
        self.rule:str
        self.violations:List[str] = []
        self.result:List[tuple] = []

    @abstractmethod
    def check_method(self) -> List[tuple]:
        pass

    @abstractmethod
    def format_explanation(self, *data) -> str:
        pass
    
    @abstractmethod
    def format_possible_solutions(self, *data) -> List[str]:
        pass
    
    def satisfied(self) -> bool:
        return (len(self.result) == 0)
    
    def can_print(self) -> bool:
        return (len(self.violations) > 0)
    
    def check(self) -> None:
        self.result = self.check_method()

    def format_result(self) -> None:
        if self.satisfied():
            return
        self.rule = f"[{self.severity.value}]: {self.problem}"
        for data in self.result:
            explanation:str = self.format_explanation(*data)
            possible_solutions:List[str] = self.format_possible_solutions(*data)
            Rule.numbers += 1
            violation:str = f"({Rule.numbers:3}.): {explanation}"
            for possible_solution in possible_solutions:
                violation += f"\n\t- {possible_solution}"
            self.violations.append(violation)

    def print_result(self) -> None:
        if not self.can_print():
            return
        print(self.rule)
        for violation in self.violations:
            print(violation)