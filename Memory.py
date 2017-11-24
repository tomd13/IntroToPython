# implementation of card game - Memory

import simplegui
import random

DECK = [0, 1, 2, 3, 4, 5, 6, 7] * 2
card1 = ""
card2 = ""
c1_idx = ""
c2_idx = ""
turn = 0


# helper function to initialize globals
def new_game():
    global DECK, exposed, state, turn
    random.shuffle(DECK)
    exposed = [False] * 16
    state = 0
    turn = 0
    pass


# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, state, card1, card2, c1_idx, c2_idx, turn
    card = pos[0] / 50
    if exposed[card] == False and state == 0:
        state = 1
        exposed[card] = True
        card1 = DECK[card]
        c1_idx = card
    elif exposed[card] == False and state == 1:
        state = 2
        exposed[card] = True
        card2 = DECK[card]
        c2_idx = card
        turn += 1
    elif exposed[card] == False and state == 2:
        if not card1 == card2:
            exposed[c1_idx] = False
            exposed[c2_idx] = False
        state = 1
        exposed[card] = True
        card1 = DECK[card]
        c1_idx = card
        card2 = ""
    pass


# cards are logically 50x100 pixels in size    
def draw(canvas):
    horiz = 15
    for idx, num in enumerate(DECK):
        if exposed[idx] == True:
            canvas.draw_text(str(num), [horiz, 60], 50, "White")
        else:
            canvas.draw_polygon([[horiz - 15, 0], [horiz + 35, 0],
                                 [horiz + 35, 100], [horiz - 15, 100]],
                                1, "White", "Green")
        horiz += 50
    label.set_text("Turns = " + str(turn))
    pass


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()