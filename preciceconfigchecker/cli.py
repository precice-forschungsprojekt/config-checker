#from config-graph import buildGraph # TODO: Import adjacent library
#from pyprecice import Participant
#
#if __name__ == "__main__":
#    # Step 1: Use PreCICE itself to check for basic errors
#    Participant.check(...)
#    # Step 2: Detect more issues through the use of a graph
#    buildGraph("precice-config.xml")

from collection_of_rules import check_all_rules, print_result


if __name__ == "__main__":
    check_all_rules()
    print_result()