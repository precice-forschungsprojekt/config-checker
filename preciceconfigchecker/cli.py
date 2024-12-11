#import sys
#from precice_config_graph import graph, xml_processing
#from pyprecice import Participant
import os

def check_all_rules() -> None:
    path:str = "./preciceconfigchecker/collection_of_rules"
    levels = os.listdir(path)
    for level in levels:
        level_path:str = path + "/" + level
        rule_files = os.listdir(level_path)
        for rule_file in rule_files:
            rule_path = level_path + "/" + rule_file
            exec(open(rule_path).read())

if __name__ == "__main__":
    #path = sys.argv[1]

    #print(f"Checking file at {path}")

    # Step 1: Use PreCICE itself to check for basic errors
    #TODO: Participant.check(...)

    # Step 2: Detect more issues through the use of a graph
    #root = xml_processing.parse_file(path)
    #graph.get_graph(root)

    check_all_rules()