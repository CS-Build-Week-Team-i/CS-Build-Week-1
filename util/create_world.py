from django.contrib.auth.models import User
from adventure.models import Player, Room
import random
Room.objects.all().delete()
# r_outside = Room(title="Outside Cave Entrance", description="North of you, the cave mount beckons")
# r_foyer = Room(title="Foyer", description="""Dim light filters in from the south. Dusty
# passages run north and east.""")
# r_outside.save()
# r_foyer.save()
# # Link rooms together
# r_outside.connectRooms(r_foyer, "n")
# r_foyer.connectRooms(r_outside, "s")
class Dungeon:
  def __init__(self):
    self.grid = None
    self.width = 0
    self.height = 0
    self.num_rooms = 0
    self.room_count = 0
  def generate_rooms(self, size_x, size_y, num_rooms):
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
        room0 = Room(0, "Mine Entrance", "A mine entrance opens up to the north.", mid_x, mid_y)
        room0.save()
        self.room_count += 1
        self.grid[mid_y][mid_x] = room0 # sets new room to the middle of the map
        propagateHelper(room0,x,y)
        players=Player.objects.all()
        for p in players:
          p.currentRoom=room0.id
          p.save()
      else:
        coinFlip = random.randrange(0, 2)
        if coinFlip == 1:
          room = Room(self.room_count, "Mine", "The dimmly lit halls of the mine show the years of digging. Old tools and abandoned items lie on the ground", x, y)
          room.save()
          self.room_count += 1
          previous_room.connectRooms(room, room_direction)
          propagateHelper(room,x,y)
    propagate(None, mid_x, mid_y, None)
w = Dungeon()
w.generate_rooms(16, 16, 100)