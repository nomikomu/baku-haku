import libtcodpy as libtcod
import fonts

#size of window
SCREEN_WIDTH = 88
SCREEN_HEIGHT = 50

#size of map
MAP_WIDTH = 80
MAP_HEIGHT = 45
 
#parameters for dungeon generator
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

#field of view
FOV_ALGO = 0 #default FOV algorithm
FOV_LIGHT_WALLS = True #light walls or not
TORCH_RADIUS = 10

LIMIT_FPS = 25 # max 25 frames/ps

#def colors
color_dark_wall = libtcod.Color(178, 201, 22)
color_light_wall = libtcod.Color(107, 187, 21)
color_dark_ground = libtcod.Color(121, 17, 135)
color_light_ground = libtcod.Color(180, 20, 79)

class Title:
	#title of map and properties
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked
		
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight
		
class Rect:
	#a rectangle on the map. used to characterize a room.
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h
 
	def center(self):
		center_x = (self.x1 + self.x2) / 2
		center_y = (self.y1 + self.y2) / 2
		return (center_x, center_y)
 
	def intersect(self, other):
		#returns true if this rectangle intersects with another one
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
				self.y1 <= other.y2 and self.y2 >= other.y1)

class Object:
	def __init__(self, x, y, char, color):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
		
	def move(self, dx, dy):
		#move by the given amount / if the destination is not blocked
		if not map[self.x + dx][self.y + dy].blocked:
			self.x += dx
			self.y += dy
		
	def draw(self):
		#only show if it's visible to the player
		if libtcod.map_is_in_fov(fov_map, self.x, self.y):
			#set the color and then draw the character that represents this object at its position
			libtcod.console_set_default_foreground(con, self.color)
			libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
		
		
	def clear(self):
		#erase the character that represents this object
		libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE) 

def create_room(room):
	global map
	for x in range(room.x1 + 1, room.x2):
		for y in range(room.y1 + 1, room.y2):
			map[x][y].blocked = False
			map[x][y].block_sight = False
			
def create_h_tunnel(x1, x2, y):
	global map
	#horizontal tunnel. min() nad max() are used in case x1>x2
	for x in range(min(x1, x2), max(x1, x2) + 1):
		map[x][y].blocked = False
		map[x][y].block_sight = False	
		
def create_v_tunnel(y1, y2, x):
	global map
	#vertical tunnel
	for y in range(min(y1, y2), max(y1, y2) + 1):
		map[x][y].blocked = False
		map[x][y].block_sight = False			


def make_map():
	global map, player
	
	#fill map with "unblocked" titles
	map = [[ Title(False)
		for y in range(MAP_HEIGHT) ]
			for x in range(MAP_WIDTH) ]
			
	rooms = []
	num_rooms = 0
	
	for r in range(MAX_ROOMS):
		#rand width and height
		w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		#rand position without going out of the boundaries of the map
		x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
		y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)
		
		new_room = Rect(x, y, w, h)

		failed = False
		for other_room in rooms:
			if new_room.intersect(other_room):
				failed = True
				break
				
		if not failed:
			create_room(new_room)
			
			(new_x, new_y) = new_room.center()
			
			if num_rooms == 0:
				player.x = new_x
				player.y = new_y
			else:
				(prev_x, prev_y) = rooms[num_rooms-1].center()
				
			if libtcod.random_get_int(0, 0, 1) == 1:
				create_h_tunnel(prev_x, new_x, prev_y)
				create_v_tunnel(prev_y, new_y, new_x)
				
		#append the new room to list
		rooms.append(new_room)
		num_rooms += 1
		
		
def render_all():
	global fov_map, color_dark_wall, color_light_wall
	global color_light_wall, color_light_ground
	global fov_recompute
	
	if fov_recompute:
		#recompt. FOV if needed
		fov_recompute = False
		libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
		
		for y in range(MAP_HEIGHT):
			for x in range(MAP_WIDTH):
				visible = libtcod.map_is_in_fov(fov_map, x, y)
				wall = map[x][y].block_sight
				
				if not visible:
					if wall:
						libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET )
					else:
						libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET )
				
				else:
					if wall:
						libtcod.console_set_char_background(con, x, y, color_light_wall, libtcod.BKGND_SET )
					else: 
						libtcod.console_set_char_background(con, x, y, color_light_ground, libtcod.BKGND_SET )
						
	#draw all objects in the list
	for object in objects:
		object.draw()
				
	libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

def handle_keys():
	#key = libtcod.console_check_for_keypress()  #real-time
	#key = libtcod.console_wait_for_keypress(True)  #turn-based
	
	key = libtcod.console_check_for_keypress()
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		#Alt+Enter: toggle fullscreen
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
		
	elif key.vk == libtcod.KEY_ESCAPE:
		return True #exit game
	
	#movement keys
	
	if libtcod.console_is_key_pressed(libtcod.KEY_UP):
		player.move(0, -1)
		fov_recompute = True
		
	elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
		player.move(0, 1)
		fov_recompute = True
		
	elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
		player.move(-1, 0)
		fov_recompute = True
	
	elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
		player.move(1, 0)
		fov_recompute = True
		
	#fullscrn mode; game q
	
	

#                            #
# initialization & main loop #
#                            #

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'kubrck-rl', False)
libtcod.sys_set_fps(LIMIT_FPS)

con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.dark_amber)
npc = Object(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', libtcod.violet)

objects = [npc, player]


make_map() #map call

fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
	for x in range(MAP_WIDTH):
		libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)
		

fov_recompute = True

while not libtcod.console_is_window_closed():
	
	render_all()
	
	libtcod.console_flush()
	
	for object in objects:
		object.clear()
	
	#handle keys and exit game if needed
	exit = handle_keys()
	if exit:
		break
	
