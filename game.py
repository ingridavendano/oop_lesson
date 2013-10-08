import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import time

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER1 = None
PLAYER2 = None
CURRENT_PLAYER = None
######################

GAME_WIDTH = 10
GAME_HEIGHT = 10

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True


###################################################
class Character(GameElement):
    SOLID = True
    count = 0

    def __init__(self, player):
        GameElement.__init__(self)
        self.inventory = []
        self.IMAGE = player

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None


class Gem(GameElement):
    IMAGE = "OrangeGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" %(len(player.inventory)))


class Roof(GameElement):
    SOLID = True

    def __init__(self,roof_type):
        self.IMAGE = roof_type


####   End class definitions    ####
def keyboard_handler():
    pick_player()

    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"
  
    if direction:
        next_location = CURRENT_PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]
    
        existing_el = GAME_BOARD.get_el(next_x, next_y)
        if existing_el:
            existing_el.interact(CURRENT_PLAYER)

        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(CURRENT_PLAYER.x, CURRENT_PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, CURRENT_PLAYER)
        if len(CURRENT_PLAYER.inventory) >= 5:
            print "Congratulations, %s! You just won because you retrieved 5 items!" %CURRENT_PLAYER
            # time.sleep function creates a pause in the game before it "ends/exits" the
            # game and the window of the game
            ###### HOWEVER ######
            # the game does not show that the last gem gets picked up before it ends the game
            time.sleep(5)
            sys.exit(0)



# if a the 1 or 2 key is hit then it will switch which player 
# is allowed to move as the current player
def pick_player():
    global CURRENT_PLAYER
    if KEYBOARD[key._1]:
        CURRENT_PLAYER = PLAYER1

    if KEYBOARD[key._2]:
        CURRENT_PLAYER = PLAYER2

######################################################################
def initialize():
    """Put game initialization code here"""

    rock_positions = [
        (2, 1),
        (1, 2),
        (3, 2),
        (4, 4)
    ]
    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0],pos[1], rock)
        rocks.append(rock)


    # rocks[-1].SOLID = False

    for rock in rocks:
        print rock


    gem_positions = [
        (7, 1),
        (8, 6),
        (3, 8),
        (7, 3),
        (8, 8),
        (5, 7),
        (6, 8)
    ]
    gems = []

    for pos in gem_positions:
        gem = Gem()
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(pos[0],pos[1], gem)
        gems.append(gem)



    global PLAYER1
    PLAYER1 = Character("Girl")
    GAME_BOARD.register(PLAYER1)
    GAME_BOARD.set_el(2, 2, PLAYER1)
    print PLAYER1

    global PLAYER2
    PLAYER2 = Character("Boy")
    GAME_BOARD.register(PLAYER2)
    GAME_BOARD.set_el(5, 5, PLAYER2)
    print PLAYER2

    global CURRENT_PLAYER
    CURRENT_PLAYER = PLAYER1

