

# define direction and movement parameter
DIRECTIONS = ['N', 'E', 'S', 'W']
MOVE_MAP = {
    'N': (0, 1),   # move up
    'E': (1, 0),   # move right
    'S': (0, -1),  # move down
    'W': (-1, 0)   # move left
}

# Car class to hold car info and how it moves
class Car:
    def __init__(self, name, x, y, direction, commands):
        self.name = name
        self.x = x
        self.y = y
        self.direction = direction
        self.commands = list(commands)  # list of moves
        self.command_index = 0  # to keep track of which command is next
        self.collided = False  # flag if car crashes

    def __str__(self):
        return f"{self.name}, ({self.x},{self.y}) {self.direction}, {''.join(self.commands)}"

    # get the next move if available
    def next_command(self):
        if self.collided or self.command_index >= len(self.commands):
            return None
        return self.commands[self.command_index]

    # perform move and update position or turn
    def execute_command(self, field_width, field_height):
        if self.collided or self.command_index >= len(self.commands):
            return (self.x, self.y)

        cmd = self.commands[self.command_index]

        if cmd == 'L':
            self.direction = DIRECTIONS[(DIRECTIONS.index(self.direction) - 1) % 4]
        elif cmd == 'R':
            self.direction = DIRECTIONS[(DIRECTIONS.index(self.direction) + 1) % 4]
        elif cmd == 'F':
            dx, dy = MOVE_MAP[self.direction]
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < field_width and 0 <= new_y < field_height:
                self.x = new_x
                self.y = new_y

        self.command_index += 1
        return (self.x, self.y)

# manage field and cars for the simulation
class Simulation:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.cars = {}

    # create field grid 
    def set_field(self, width, height):
        self.width = width
        self.height = height

    # add car into grid
    # x = x position
    # y = y position
    # direction = initial facing direction
    # commands = sequence of movement
    def add_car(self, name, x, y, direction, commands):
        self.cars[name] = Car(name, x, y, direction, commands)

    # run the simulation until all moves are done or crash happens
    def run(self):
        step = 0
        names = list(self.cars.keys())
        still_running = True
        while still_running:
            step += 1
            still_running = False
            pos = {}
            for name in names:
                car = self.cars[name]
                if car.collided:
                    continue
                cmd = car.next_command()
                if cmd:
                    still_running = True
                    new_pos = car.execute_command(self.width, self.height)
                    if new_pos in pos: # collision check
                        other = pos[new_pos]
                        car.collided = True
                        self.cars[other].collided = True
                        print(f"- {car.name}, collides with {other} at {new_pos} at step {step}")
                        print(f"- {other}, collides with {car.name} at {new_pos} at step {step}")
                    else:
                        pos[new_pos] = car.name

        for car in self.cars.values():
            if not car.collided:
                print(f"- {car.name}, ({car.x},{car.y}) {car.direction}")

# helper input function to handle sandbox issues
import sys

def safe_input(prompt):
    try:
        return input(prompt)
    except OSError:
        print("Something went wrong with input. Try again.")
        sys.exit(1)

# user prompts
if __name__ == '__main__':
    sim = Simulation()
    print("Welcome to the car simulation\n")
    try: # to set the grid size
        width, height = map(int, safe_input("Please enter the width and height of the simulation field in x y format: ").split())
        sim.set_field(width, height)
    except ValueError:
        print("Invalid input, please enter valid numbers.")
        sys.exit(1)
    print(f"You have created a field of {width} x {height}.\n")
  
    while True: # user's selection
        print("Please choose from the following options:")
        print("[1] Add a car to field")
        print("[2] Run simulation")
        choice = safe_input("Your choice: ").strip()
        if choice == '1': # to add car
            name = safe_input("Please enter the name of the car: ").strip()
            try:
                x, y, d = safe_input("Please enter initial position of car A in (x y Direction) format: ").split()
                x = int(x)
                y = int(y)
                if d not in DIRECTIONS:
                    print("Use N, S, E, or W for direction.")
                    continue
                moves = safe_input("Please enter the commands: ").strip().upper()
                sim.add_car(name, x, y, d, moves)
                print("\nYour current list of cars are: ")
                for c in sim.cars.values():
                    print("-", c)
            except ValueError:
                print("Invalid input format, try again.")
        elif choice == '2': # to start simulation
            print("\nYour current list of cars are:")
            for c in sim.cars.values():
                print("-", c)
            print("\nAfter simulation, the result is:")
            sim.run() # run simulation and print the result
            print("\nPlease choose from the following options:")
            print("[1] Start over")
            print("[2] Exit")
            after = safe_input("Your choice: ").strip()
            if after == '1': # to restart simulation
                sim = Simulation()
                print("Welcome to Auto Driving Car Simulation!\n")
                try:
                    width, height = map(int, safe_input("Please enter the width and height of the simulation field in x y format: ").split())
                    sim.set_field(width, height)
                except ValueError:
                    print("Invalid input.")
                    sys.exit(1)
            else: # to exit simulation
                print("Thank you for running the simulation. Goodbye!\n")
                sys.exit()
        else:
            print("Invalid choice. Please try again.")
