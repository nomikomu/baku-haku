import libtcodpy as libtcod
import fonts

SCREEN_WIDTH = 88
SCREEN_HEIGHT = 50
LIMIT_FPS = 25

def handle_keys():
	global playerx, playery
	
	#movement keys
	
	if libtcod.console_is_key_pressed(libtcod.KEY_UP):
		playery -= 1
		
	elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
		playery += 1
		
	elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
		playerx -= 1
	
	elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
		playerx += 1
		
	#fullscrn mode; game q
	
	key = libtcod.console_check_for_keypress()
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		#Alt+Enter: toggle fullscreen
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
		
	elif key.vk == libtcod.KEY_ESCAPE:
		return True #exit game

#							 #
# initialization & main loop #
#							 #

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'kubrck-rl', False)
libtcod.sys_set_fps(LIMIT_FPS)

#player pos
playerx = SCREEN_WIDTH/2
playery = SCREEN_HEIGHT/2

while not libtcod.console_is_window_closed():
	libtcod.console_set_default_foreground(0, libtcod.dark_amber)
	libtcod.console_put_char(0, playerx, playery, '@', libtcod.BKGND_NONE)
	
	libtcod.console_flush()
	
	libtcod.console_put_char(0, playerx, playery, ' ', libtcod.BKGND_NONE)
	#clears out after '@' mark //temp
	
	#handle keys and exit game if needed
	exit = handle_keys()
	if exit:
		break
	
