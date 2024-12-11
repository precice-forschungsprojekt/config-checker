from enum import Enum

#colors: 0:grey, 1:red 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, 7:white
class Severity(Enum):
    INFO =    "\033[1;34mInfo\033[0m"
    WARNING = "\033[1;33mWarning\033[0m"
    ERROR =   "\033[1;31mError\033[0m"