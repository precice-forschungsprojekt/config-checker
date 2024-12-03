from rule import Severity
from rule import Rule
from typing import List


# methods for checking rules
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
    # rule, method for rule, arguments for method
    rules = [
        [Rule("test"), exists_edges, [[1,2,3]]],# just testing... ignore it!!!
        [Rule("You can do that!", Severity.INFO), exists_edges, [[4,5,6]]],# just testing... ignore it!!!
        [Rule("That's a big problem!", Severity.WARNING, "More testing!"), exists_edges, [[7,8,9]]],# just testing... ignore it!!!
        [Rule("Just testing with true output", Severity.INFO, "nothing!"), exists_nodes, [[10,33]]],# just testing... ignore it!!!
        [Rule("Incorrect return value", Severity.WARNING), other_test, [4, 6, 100]]
    ]

    results:List[str] = []
    
    def check_all_rules(self) -> None:
        for r in self.rules:
            rule:Rule = r[0]
            method = r[1]
            arguments = r[2]
            rule.check_with(method, arguments)
            result:str = rule.get_result()
            if (len(result) > 0):
                self.results.append(result)

    def print_result(self) -> None:
        for result in self.results:
            print(result)
