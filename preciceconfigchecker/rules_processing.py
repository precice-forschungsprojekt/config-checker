from networkx import Graph

import preciceconfigchecker.color as c
from preciceconfigchecker.rule import Rule, rules
# ALL RULES THAT SHOULD BE CHECKED NEED TO BE IMPORTED
# SOME IDE's MIGHT REMOVE THEM AS UNUSED IMPORTS
# noinspection PyUnresolvedReferences
from preciceconfigchecker.rules import missing_coupling, missing_exchange, data_use_read_write, compositional_coupling
from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation


def all_rules_satisfied(violations_by_rule: dict[Rule, list[Violation]]) -> bool:
    """
    Checks whether all rules are satisfied.

    Returns:
        bool: True, if all rules are satisfied.
    """
    return all(len(violations) == 0 for violations in violations_by_rule.values())


def check_all_rules(graph: Graph, debug: bool) -> dict[Rule, list[Violation]]:
    """
    Checks all rules for violations
    """
    print("")
    if debug:
        print("Checking rules...")

    violations_by_rule = {}

    for rule in rules:
        if debug or rule.severity != Severity.DEBUG:
            violations_by_rule[rule] = rule.check(graph)

    if debug:
        print("Rules checked.\n")
    return violations_by_rule


def print_all_results(violations_by_rule: dict[Rule, list[Violation]], debug: bool):
    """
    Prints all existing violations of all rules
    """
    if not all_rules_satisfied(violations_by_rule):
        print("The following issues were found:\n")
    for (rule, violations) in violations_by_rule.items():
        print_result(rule, violations, debug)

    def total_violations_by_severity(severity: Severity) -> int:
        return sum(len(violations) for (rule, violations) in violations_by_rule.items() if rule.severity == severity)

    total_num_errors = total_violations_by_severity(Severity.ERROR)
    total_num_warnings = total_violations_by_severity(Severity.WARNING)

    if total_num_errors != 0 or total_num_warnings != 0:
        error_str: str = Severity.ERROR.value + ("s" if total_num_errors != 1 else "")
        warning_str: str = Severity.WARNING.value + ("s" if total_num_errors != 1 else "")
        print(f"Your configuration file raised {total_num_errors} {error_str} "
              f"and {total_num_warnings} {warning_str}.")
        print("Please review your configuration file before continuing.")
    else:
        print("You are all set to start you simulation!")


def print_result(rule: Rule, violations: list[Violation], debug: bool):
    """
    If the rule has violations, these will be printed.
    If debug mode is enabled, more information is displayed.
    """
    if not debug and (rule.severity == Severity.DEBUG or len(violations) == 0):
        return
    if len(violations) == 0:
        print(f"[{Severity.DEBUG.value}]: '{c.dyeing(rule.__class__.__name__, c.purple)}' is satisfied.")
        return

    severity_info: str
    if debug and rule.severity != Severity.DEBUG:
        severity_info = f"[{rule.severity.value},{Severity.DEBUG.value}]: ({c.dyeing(rule.__class__.__name__, c.purple)})"
    elif debug and rule.severity == Severity.DEBUG:
        severity_info = f"[{Severity.DEBUG.value}]: ({c.dyeing(rule.__class__.__name__, c.purple)})"
    else:
        severity_info = f"[{rule.severity.value}]:"
    print(f"{severity_info} {rule.name}")

    for violation in violations:
        formatted_violation = violation.format()
        print(formatted_violation)

    print("")
