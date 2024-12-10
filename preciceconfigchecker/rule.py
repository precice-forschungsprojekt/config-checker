from typing import List, Callable
from violation import Violation, Problem
from severity import Severity


class Rule:
    def __init__(self, problem:Problem, severity:Severity = Severity.INFO) -> None:
        self.problem = problem
        self.severity = severity
        self.violations:List[Violation] = []

    def check_with(self, check_method:Callable, args:tuple) -> None:
        result:List = check_method(*args)
        for data in result:
            violation = Violation(self.problem, data)
            self.violations.append(violation)

    def has_followed(self) -> bool:
        return (len(self.violations) == 0)

    def get_result(self) -> str:
        if self.has_followed():
            return ""
        out:str = "[" + self.severity.value + "]: " + self.problem.value
        for violation in self.violations:
            out += violation.get_output()
        return out