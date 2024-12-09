from rule import Rule, Severity
from violation import Problem
from typing import Callable, List


# Methods for checking rules.
# Methods must return a bool value!


# 3-tuples (rule, method for rule, arguments[] for method)
# Template: (Problem.DATA_NOT_USED, Severity.INFO), myfunc, [])
rules:tuple[Rule, Callable, tuple] = [
]

results:List[str] = []

def check_all_rules() -> None:
    for (rule, method, arguments) in rules:
        rule.check_with(method, arguments)
        if not rule.has_followed():
            result:str = rule.get_result()
            results.append(result)

def print_result() -> None:
    for result in results:
        print(result)
