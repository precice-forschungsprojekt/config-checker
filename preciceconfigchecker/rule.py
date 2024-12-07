from enum import Enum


class Severity(Enum):
    INFO = "Info"
    WARNING = "Warning"


class Rule:
    numbers_not_followed:int = 0 #static attribute: do not use 'self.numbers_not_followed'

    def __init__(self, problem:str, severity:Severity = Severity.INFO, possible_solutions:str = "") -> None:
        self.problem = problem
        self.severity = severity
        self.possible_solutions = possible_solutions
        self.followed = False

    def check_with(self, check_method, args) -> None:
        result = check_method(*args)
        if type(result) is not bool: # Debug for new check_method
            print("[Error]: The passed method does not return a bool value! By Rule: " + self.problem)
        else:
            self.followed = result

    def has_followed(self) -> bool:
        return self.followed

    def get_result(self) -> str:
        if self.has_followed():
            return ""
        Rule.numbers_not_followed += 1
        out:str = f"[{Rule.numbers_not_followed:2}.]" + "[" + self.severity.value + "]: " + self.problem
        if (len(self.possible_solutions) > 0):
            out += "\n\t[Possible Solution]: " + self.possible_solutions
        return out