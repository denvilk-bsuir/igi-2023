import os
import json
import re
from typing import Any, Set

class Container:
    username: str
    current_state: Set[Any]
    saved: bool

    def __init__(self, username):
        self.saved = True
        self.load(username)

    def load(self, username: str) -> None:
        if not self.saved:
            ans = input("Your data is not saved. Do you want to continue? (y/N):")
            if ans!='y':
                print('Loading new data without saving.')
            else:
                self.save()

        print("Loading data...")
        data:dict = {}
        self.username = username
        try:
            with open("data.txt","r+") as f:
                data = json.load(f)
                print(data)
        except FileNotFoundError:
            os.system("touch data.txt && echo {} >> data.txt")
            with open("data.txt","r+") as f:
                data = json.load(f)
                print(data)
            
        if not username in data:
            print("No such user in db, creating new.")
            self.current_state = set()
            self.save()
        else:
            self.current_state = set(data.get(username, []))
            self.saved = True

        print("Loaded: ", *self.current_state)

    def save(self) -> None:
        if self.saved:
            print("Your data has been already saved.")
            return

        data = None
        with open("data.txt", "r+") as f:
            data = json.load(f)
        data[self.username] = list(self.current_state)
        print(data)
        with open("data.txt", "w+") as f:
            json.dump(data, f)

        
        self.saved = True
        print("Saved!")

    def add(self, *args) -> None:
        if self.saved:
            self.saved = False

        print("Adding", *args)
        count = self.current_state.__len__()
        self.current_state.update(args)
        print(f"Has been added {len(self.current_state)-count} elements!")
    
    def remove(self, *args) -> None:
        if self.saved:
            self.saved = False

        print("Removing", *args)
        count = len(self.current_state)
        for item in args:
            if item in self.current_state:
                self.current_state.remove(item)
            else:
                print("You trying to remove element which doesn't exist.")

        print(f"Has been removed {count-len(self.current_state)} elements!")

    def find(self, *args) -> None:
        c = 0
        for item in args:
            if item in self.current_state:
                print(f"Found {item}.")
                c+=1
            else:
                print(f"{item} not found.")
        if not c:
            print("No items found.")
        else:
            print(f"Matches found: {c}")

    def grep(self, regex: str) -> None:
        c = 0
        for item in self.current_state:
            if (res := re.match(regex, item)):
                print(f"Matching pattern {item}")
                c+=1
        if not c:
            print("No items matched with regular expression")
        else:
            print(f"Matches found: {c}")

    def list(self) -> None:
        print("Printing all elements from container")
        print(*self.current_state, sep='\n')

    def switch(self, username) -> None:
        if self.username == username:
            print("You have been already logged in as such user.")
            return
        
        self.load(username)

username = input("Enter username to load data: ")
container = Container(username)

print("""Choose command:
        list - To view elements in container
        grep - To find elements with regexp pattern
        save - Save data
        load - Load data
        remove - Remove element (or elements) from container
        add - Add element (or elements) from container
        find - Check existence for element (or elements) in container
        switch - Switch to other user
        stop - Stop work

        Choose:
    """)

while (cmd := input())!="stop":
    os.system("clear")
    print("Results")
    print("-"*20)
    match (cmd):
        case "list":
            container.list()
        case "grep":
            regex = input("Enter regular expression to filter items: ")
            container.grep(regex)
        case "save":
            container.save()
        case "load":
            username = input("Enter username to load data: ")
            container.load(username)
        case "add":
            elements = input("Enter element (or elements) to add to container(splitting by @): ")
            container.add(*(elements.split('@')))
        case "remove":
            elements = input("Enter element (or elements) to remove to container(splitting by @): ")
            container.remove(*(elements.split('@')))
        case "find":
            elements = input("Enter element (or elements) to check existance in container(splitting by @): ")
            container.find(*(elements.split('@')))
        case "switch":
            username = input("Enter username to load data: ")
            container.switch(username)
        case _:
            continue
    print("-"*20)

    print("""Choose command:
        list - To view elements in container
        grep - To find elements with regexp pattern
        save - Save data
        load - Load data
        remove - Remove element (or elements) from container
        add - Add element (or elements) from container
        find - Check existence for element (or elements) in container
        switch - Switch to other user
        stop - Stop work

        Choose:
    """)


if not container.saved:
    ans = input("Your data is not saved. Do you want to continue? (y/N):")
    if ans!='y':
        print('Loading new data without saving.')
    else:
        container.save()