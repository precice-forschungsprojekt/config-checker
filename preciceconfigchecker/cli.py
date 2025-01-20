import argparse
import sys

from severity import Severity
import color as c

from precice_config_graph import graph, xml_processing

from rule import check_all_rules, print_all_results

# ALL RULES THAT SHOULD BE CHECKED NEED TO BE IMPORTED
# SOME IDE's MIGHT REMOVE THEM AS UNUSED IMPORTS
from rules import missing_coupling
from rules import data_use_read_write

path:str = None
debug:bool = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage='%(prog)s', description='Checks a PreCICE config.xml file for logical errors.')
    parser.add_argument('src', type=argparse.FileType('r'), help='Path of the config.xml source file.')
    parser.add_argument('-d', '--debug', action='store_true', help='Enables debug mode')
    args = parser.parse_args()

    if args.debug:
        debug = args.debug
        print(f"[{Severity.DEBUG.value}]: Debug mode enabled")
    if args.src.name.endswith('.xml'):
        path = args.src.name
        print(f"Checking file at '{c.dyeing(path, c.cyan)}'")
    else:
        sys.exit(f"[{Severity.ERROR.value}]: '{c.dyeing(args.src.name, c.cyan)}' is not an xml file")

    # Step 1: Use preCICE itself to check for basic errors
    # TODO: Participant.check(...)

    # Step 2: Detect more issues through the use of a graph
    root = xml_processing.parse_file(path)
    graph = graph.get_graph(root)

    # individual checks need the graph
    check_all_rules(graph)

    # if the user uses severity=debug, then the severity has to be passed here as an argument
    print_all_results(debug)
