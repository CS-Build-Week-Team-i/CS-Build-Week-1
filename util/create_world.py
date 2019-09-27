from django.contrib.auth.models import User
from adventure.models import Player, Room, Map
from util.generator import World

Room.objects.all().delete()

w = World()
w.generate_rooms(14, 14, 100)
w.new_print_rooms()

i=0
for row in w.grid:
	j=0
	for room in row:
		if room:
			new_room = Room(id=room.id, title=room.name, description=room.description, x=room.x, y=room.y)
			new_room.save()
			room.n_to and new_room.connectRoomByID(room.n_to, 'n')
			room.s_to and new_room.connectRoomByID(room.s_to, 's')
			room.e_to and new_room.connectRoomByID(room.e_to, 'e')
			room.w_to and new_room.connectRoomByID(room.w_to, 'w')
		j+=1
	i+=1
	
players=Player.objects.all()
for p in players:
  p.currentRoom=r_outside.id
  p.save()