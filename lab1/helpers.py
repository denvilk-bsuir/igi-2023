from enum import Enum

class Operation(Enum):
    ADD = 'add'
    SUB = 'sub'
    MULT = 'mult'
    DIV = 'div'

class Command(Enum):
    HELLO_WORLD = 1
    CALCULATOR = 2
    EVEN_ARRAY = 3