import libtcodpy as libtcod
import fonts

#size of window
SCREEN_WIDTH = 88
SCREEN_HEIGHT = 50

#size of map
MAP_WIDTH = 80
MAP_HEIGHT = 45

LIMIT_FPS = 25 # max 25 frames/ps

#def colors
color_dark_wall = libtcod.Color(39, 81, 81)
color_dark_ground = libtcod.Color(3, 34, 34)


class Title:
	#title of map and properties
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked
		
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight

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
		#set the color and then draw the character that represents this object at its position
		libtcod.console_set_default_foreground(con, self.color)
		libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
		
	def clear(self):
		#erase the character that represents this object
		libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE) 

def make_map():
	global map
	
	#fill map with "unblocked" titles
	map = [[ Title(False)
		for y in range(MAP_HEIGHT) ]
			for x in range(MAP_WIDTH) ]
			
	#place two pillars the map //test
	map[30][22].blocked = True
	map[30][22].block_sight = True
	map[50][22].blocked = True
	map[50][22].block_sight = True

def render_all():
	global color_light_wall
	global color_light_ground
		
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			wall = map[x][y].block_sight
			if wall:
				libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET )
			else:
				libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET )
				
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
		
	elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
		player.move(0, 1)
		
	elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
		player.move(-1, 0)
	
	elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
		player.move(1, 0)
		
	#fullscrn mode; game q
	
	

#							 #
# initialization & main loop #
#							 #

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'kubrck-rl', False)
libtcod.sys_set_fps(LIMIT_FPS)

con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.dark_amber)
npc = Object(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', libtcod.violet)

objects = [npc, player]


make_map() #map call

while not libtcod.console_is_window_closed():
	
	render_all()
	
	libtcod.console_flush()
	
	for object in objects:
		object.clear()
	
	#handle keys and exit game if needed
	exit = handle_keys()
	if exit:
		break
	
