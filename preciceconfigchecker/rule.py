from enum import Enum
from typing import List, Callable
from violation import Violation, Problem


class Severity(Enum):
    INFO = "Info"
    WARNING = "Warning"


class Rule:
    def __init__(self, problem:Problem, severity:Severity = Severity.INFO) -> None:
        self.problem = problem
        self.severity = severity
        self.violations:List[Violation] = []
        self.followed = False

    def check_with(self, check_method:Callable, args:tuple) -> None:
        result:List = check_method(*args)
        if (len(result) > 0):
            self.followed = False
            for data in result:
                self.violations.append(Violation(self.problem, data))
        else:
            self.followed = True

    def has_followed(self) -> bool:
        return self.followed

    def get_result(self) -> str:
        if self.has_followed():
            return ""
        out:str = "[" + self.severity.value + "]: " + self.problem.value
        for violation in self.violations:
            out += violation.get_output()
        return out