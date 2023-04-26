from typing import List
from constants import HELLO_WORLD
from helpers import Operation, Command


def hello_world() -> None:
    print(HELLO_WORLD)


def calculator(a: int, b: int, operation: Operation) -> None:
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


def create_array(l: List) -> List:
    print('Generating array with even elements which don\'t exceed N')
    return [x for x in l if x%2==0]


if __name__ == '__main__':
    print('Choose function to execute (number [1-3]):')
    print('1) Hello world')
    print('2) Calculator')
    print('3) Create even array')

    try:
        cmd = int(input())
        command = Command(cmd)
    except ValueError:
        print('[Error] Invalid command. Stopping.')
        command = None

    match (command):
        case Command.HELLO_WORLD:
            hello_world()
        case Command.CALCULATOR:
            try:
                a, b = map(int, input('Enter number A and B (in one line):\n').split())
                operation_input = input('Enter operation (add, sub, mult, div):\n')

                try:
                    operation = Operation(operation_input)
                    calculator(a, b, operation)
                except ValueError:
                    print('[Error] Invalid operation. Stopping.')
            except ValueError:
                print('[Error] Invalid numbers. Stopping.')
        case Command.EVEN_ARRAY:
            try:
                l = list(map(int, input("Enter array of integer numbers in one line:\n").split()))
                a = create_array(l)
                
                print(a)
            except ValueError:
                print('[Error] Invalid numbers. Stopping.')

        