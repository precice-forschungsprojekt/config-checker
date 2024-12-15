import sys
from precice_config_graph import graph, xml_processing
from pyprecice import Participant
from rule import check_all_rules, format_all_results, print_all_results
import rules.example_1
import rules.example_2
import rules.example_3

if __name__ == "__main__":
    path = sys.argv[1]

    print(f"Checking file at {path}")

    # Step 1: Use PreCICE itself to check for basic errors
    #TODO: Participant.check(...)

    # Step 2: Detect more issues through the use of a graph
    root = xml_processing.parse_file(path)
    graph.get_graph(root)
    check_all_rules()
    format_all_results()
    print_all_results()
