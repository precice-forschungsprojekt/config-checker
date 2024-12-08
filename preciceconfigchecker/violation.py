from enum import Enum
from typing import List


class Problem(Enum):
    PARTICIPANT_MESH_NOT_CONNECTED = "Some meshes and participants are not connected"
    DATA_NOT_USED = "Some data was not used"


class Violation:
    numbers:int = 0 #static attribute: do not use 'self.numbers', use 'Violation.numbers'

    def __init__(self, problem:Problem, data:tuple) -> None:
        self.problem = problem
        self.data = data

    def get_output(self) -> str:
        explanation:str = ""
        possible_solutions:List[str] = []
        match self.problem:
            case Problem.PARTICIPANT_MESH_NOT_CONNECTED: # data[0] is MeshNode, data[1] is ParticipantNode
                explanation = "Mesh " + str(self.data[0]) + " is not connected to Participant " + str(self.data[1])
                possible_solutions.append("Delete Mesh " + str(self.data[0]))
            case Problem.DATA_NOT_USED: # data[0] is DataNode, data[1] is ParticipantNode or MeshNode
                explanation = "Data " + str(self.data[0]) + " is not used in Participant/Mesh " + str(self.data[1])
                possible_solutions.append("Delete Data " + str(self.data[0]))
                possible_solutions.append("Add Data " + str(self.data[0]) + " to Participant/Mesh " + str(self.data[1]))
            case _:
                print("[ERROR]: unknown violation")
                return
        return Violation.create_output(explanation, possible_solutions)
    
    def create_output(explanation:str, possible_solutions:List[str]) -> str:
        Violation.numbers += 1
        out:str = f"\n({Violation.numbers:3}.): " + explanation
        for possible_solution in possible_solutions:
            out += "\n\t- " + possible_solution
        return out