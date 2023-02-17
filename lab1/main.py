from constants import HELLO_WORLD

def hello_world():
    print(HELLO_WORLD)

def calculator():
    pass

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
            calculator()
        case 3:
            create_array()
        case _:
            print("Invalid command. Stopping.")
            
        