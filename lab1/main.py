from constants import HELLO_WORLD
from helpers import Operation

def hello_world():
    print(HELLO_WORLD)

def calculator(a: int, b: int, operation: Operation):
    match operation:
        case Operation.ADD:
            print(a+b)
        case Operation.SUB:
            print(a-b)
        case Operation.DIV:
            try:
                print(a/b)
            except ZeroDivisionError:
                print('[Error] Division by zero. Stopping.')
        case Operation.MULT:
            print(a*b)


def create_array():
    pass


if __name__ == '__main__':
    print('Choose function to execute (number [1-3]):')
    print('1) Hello world')
    print('2) Calculator')
    print('3) Create even array')
    cmd = int(input())
    match (cmd):
        case 1:
            hello_world()
        case 2:
            a, b = map(int, input('Enter number A and B (in one line):\n').split())
            operation_input = input('Enter operation (add, sub, mult, div):\n')
            try:
                operation = Operation(operation_input)
                calculator(a, b, operation)
            except ValueError:
                print('[Error] Invalid operation. Stopping')
                
        case 3:
            create_array()
        case _:
            print("Invalid command. Stopping.")

        