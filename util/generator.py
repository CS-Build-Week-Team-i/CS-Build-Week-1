# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.

import random

class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y
    def __repr__(self):
        return f"{self.id}.zfill(3), ({self.x}, {self.y})"
    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room.id)
        setattr(connecting_room, f"{reverse_dir}_to", self.id)
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
        self.num_rooms = 0
        self.room_count = 0

    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid) # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)

    def new_print_rooms(self):
        reverse_grid = list(self.grid) # make a copy of the list
        reverse_grid.reverse()

        # top of container
        # for room in reverse_grid[0]:
        displayFormat = '-x,y-'
        print('*'*(len(reverse_grid[0])*len(displayFormat)+4))

        for row in reverse_grid:
            print('||', end='')
            for room in row:
                print('  |  ' if room and room.n_to else '     ', end='')
            print('||')

            print('||', end='')
            for room in row:
                print('-'if room and room.w_to else ' ', end='')
                print(f'{room.id}'.zfill(3) if room else '...', end='')
                print('-'if room and room.e_to else ' ', end='')
            print('||')

            print('||', end='')
            for room in row:
                print('  |  ' if room and room.s_to else '     ', end='')
            print('||')

        # bottom of container
        print('*'*(len(reverse_grid[0])*len(displayFormat)+4))

    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        self.num_rooms = num_rooms
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * size_x

        # Start from center (0,0)
        mid_x = int(self.width/2) # (this will become 0 on the first step)
        mid_y = int(self.height/2)

        def propagateHelper(previous_room,x,y):
            if y+1 < self.height and (self.grid[y+1][x] == None):
                propagate(previous_room, x, y+1, 'n')
            if x+1 < self.width and (self.grid[y][x+1] == None):
                propagate(previous_room, x+1, y, 'e')
            if x-1 >= 0 and (self.grid[y][x-1] == None):
                propagate(previous_room, x-1, y, 'w')
            if y-1 >= 0 and (self.grid[y-1][x] == None):   
                propagate(previous_room, x, y-1, 's')

        def propagate(previous_room, x, y, room_direction):
            # if number of rooms needed is reached
            if self.room_count >= num_rooms:
                return 
            # first execution
            elif self.room_count == 0:
                room0 = Room(0, "A Generic Room", "This is a generic room.", mid_x, mid_y)
                self.room_count += 1
                self.grid[mid_y][mid_x] = room0 # sets new room to the middle of the map
                propagateHelper(room0,x,y)
            else:
                coinFlip = random.randrange(0, 2)
                if coinFlip == 1:
                    room = Room(self.room_count, "A Generic Room", "This is a generic room.", x, y)
                    self.grid[y][x] = room
                    self.room_count += 1
                    previous_room.connect_rooms(room, room_direction)
                    propagateHelper(room,x,y)

        propagate(None, mid_x, mid_y, None)


w = World()
w.generate_rooms(16, 16, 100)
w.new_print_rooms()

print(f"\n\nWorld\n  height: {w.height},\n  width: {w.width},\n  num_rooms: {w.num_rooms},\n  num_gen_rooms: {w.room_count}\n")