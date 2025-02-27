import contextlib
import io

from precice_config_graph import graph, xml_processing
from preciceconfigchecker.rule import rules
from preciceconfigchecker.rules_processing import check_all_rules
from preciceconfigchecker import color


def equals(a, b):
    if type(a) != type(b):
        return False
    return vars(a) == vars(b)


xml = xml_processing.parse_file("precice-config.xml")
graph = graph.get_graph(xml)

with contextlib.redirect_stdout(io.StringIO()):
    check_all_rules(graph, True)

# No violations are expected
violations_expected = []

violations_actual = []
for rule in rules:
    for violation in rule.violations:
        violations_actual.append(violation)

# Sort them so that violations of the same type are in the same order
violations_expected_s = sorted(violations_expected, key=lambda obj: type(obj).__name__)
violations_actual_s = sorted(violations_actual, key=lambda obj: type(obj).__name__)

assert len(violations_expected_s) == len(violations_actual_s), (
    f"[Simple-good test] Different number of expected- and actual violations.\n"
    f"   Number of expected violations: {len(violations_expected)},\n"
    f"   Number of actual violations: {len(violations_actual)}.")

for violation_e, violation_a in zip(violations_expected_s, violations_actual_s):
    assert equals(violation_e, violation_a), (
        "[Simple-good test] Expected- and actual violations do not match.\n"
        f"   Expected violation: {violation_e.format_explanation()}\n"
        f"   Actual violation: {violation_a.format_explanation()}")

print(f"[Simple-good test] {color.dyeing("Passed", color.green)}.")
