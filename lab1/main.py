from typing import List
from constants import HELLO_WORLD
from helpers import Operation


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


def create_array(n: int) -> List:
    print('Generating array with even elements which don\'t exceed N')
    return [x for x in range(0, n+1, 2)]


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
        case 3:
            try:
                n = int(input('Enter upper bound of array elements: \n'))
                a = create_array(n)
                print(a)
            except ValueError:
                print('[Error] Invalid upper bound. Stopping.')
        case _:
            print("[Error] Invalid command. Stopping.")

        