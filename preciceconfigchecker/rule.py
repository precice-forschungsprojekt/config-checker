from typing import List
from abc import ABC, abstractmethod
from violation import Violation
from severity import Severity


class Rule(ABC):
    @property
    @abstractmethod
    def problem(self) -> str: pass
    @property
    @abstractmethod
    def severity(self) -> Severity: pass

    violations:List[Violation] = []

    complete_output:str = ""

    @abstractmethod
    def check(self) -> None: pass

    def satisfied(self) -> bool:
        return (len(self.violations) == 0)

    def collect_output(self) -> None:
        if self.satisfied():
            return
        out:str = "[" + self.severity.value + "]: " + self.problem
        for violation in self.violations:
            out += violation.create_output()
        if (len(Rule.complete_output) > 0):
            out = "\n" + out
        Rule.complete_output += out