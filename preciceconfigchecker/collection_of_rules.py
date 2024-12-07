from rule import Severity
from rule import Rule
from typing import List


# Methods for checking rules.
# Methods must return a bool value!
# just testing... ignore it!!!
def exists_edges(edges:List[int]):
    testList:List[int] = [1,2,3,4,5,6]
    for edge in edges:
        if not (testList.__contains__(edge)):
            return False
    return True

# just testing... ignore it!!!
def exists_nodes(nodes:List[int]):
    nodes.clear()
    return True

# just testing... ignore it!!!
def other_test(a, b, c):
    return (a + b) * c


class CollectionOfRules:
    # 3-tuples (rule, method for rule, arguments[] for method)
    # Template: (Rule("problem", Severity.INFO, "possible solutions"), myfunc, [])
    rules = [
        (Rule("Problem 1"), exists_edges, [[1,2,3]]),# just testing... ignore it!!!
        (Rule("Problem 2", Severity.INFO), exists_edges, [[4,5,6]]),# just testing... ignore it!!!
        (Rule("Problem 3", Severity.WARNING, "More testing!"), exists_edges, [[7,8,9]]),# just testing... ignore it!!!
        (Rule("Problem 4", Severity.INFO, "nothing!"), exists_nodes, [[10,33]]),# just testing... ignore it!!!
        (Rule("Problem 5", Severity.WARNING, "Just fix it!"), other_test, [4, 6, 100])# just testing... ignore it!!!
    ]

    results:List[str] = []
    
    def check_all_rules(self) -> None:
        rule:Rule
        for (rule, method, arguments) in self.rules:
            rule.check_with(method, arguments)
            if not rule.has_followed():
                result:str = rule.get_result()
                self.results.append(result)

    def print_result(self) -> None:
        for result in self.results:
            print(result)
