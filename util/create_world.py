from django.contrib.auth.models import User
from adventure.models import Player, Room
from util.generator import World

Room.objects.all().delete()

w = World()
w.generate_rooms(14, 14, 120)
w.new_print_rooms()

for row in w.grid:
	for room in row:
		if room.x == 5 and room.y == 5:
			currRoom = Room(id=room.id, title=room.name, description=room.description, x=room.x, y=room.y)
			currRoom.save()
			room.n_to and currRoom.connectRoomByID(room.n_to, 'n')
			room.s_to and currRoom.connectRoomByID(room.s_to, 's')
			room.e_to and currRoom.connectRoomByID(room.e_to, 'e')
			room.w_to and currRoom.connectRoomByID(room.w_to, 'w')
			players=Player.objects.all()
			for p in players:
			  p.currentRoom=currRoom.id
			  p.save()
		if room:
			new_room = Room(id=room.id, title=room.name, description=room.description, x=room.x, y=room.y)
			new_room.save()
			room.n_to and new_room.connectRoomByID(room.n_to, 'n')
			room.s_to and new_room.connectRoomByID(room.s_to, 's')
			room.e_to and new_room.connectRoomByID(room.e_to, 'e')
			room.w_to and new_room.connectRoomByID(room.w_to, 'w')