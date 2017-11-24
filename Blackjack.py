# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
winner = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print
            "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        hand_string = "Hand contains "
        for card in self.cards:
            hand_string += str(card) + " "
        return hand_string

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        has_aces = False
        value = 0
        for card in self.cards:
            if card.rank == "A":
                has_aces = True
            value += VALUES[card.rank]
        if not has_aces:
            return value
        else:
            if value + 10 <= 21:
                return value + 10
            else:
                return value

    def draw(self, canvas, pos):
        for card in self.cards:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(card.rank),
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(card.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE,
                              [pos[0] + CARD_CENTER[0] * self.cards.index(card) * 2,
                               pos[1] + CARD_CENTER[1]], CARD_SIZE)


# define deck class
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def __str__(self):
        deck_string = "Deck contains "
        for card in self.cards:
            deck_string += str(card) + " "
        return deck_string


# define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, score

    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    print
    "Player " + str(player)
    print
    "Dealer " + str(dealer)
    print
    "Player: " + str(player.get_value())
    print
    "Dealer: " + str(dealer.get_value())
    outcome = "Hit or stand?"
    winner = ""

    in_play = True


def hit():
    global winner, score

    if in_play and player.get_value() <= 21:
        player.add_card(deck.deal_card())
    print
    "Player: " + str(player.get_value()) + " - " + str(player)

    if player.get_value() > 21:
        winner = "You have busted"
        score -= 1


def stand():
    global in_play, outcome, winner, score

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        if player.get_value() > 21:
            winner = "You have busted"
            score -= 1
        else:
            while dealer.get_value() < 17:
                dealer.add_card(deck.deal_card())
                print
                "Dealer: " + str(dealer.get_value())
            if dealer.get_value() > 21:
                winner = "Dealer has busted! You win!"
                score += 1
            elif dealer.get_value() >= player.get_value():
                winner = "Dealer wins!"
                score -= 1
            else:
                winner = "You win!"
                score += 1

    print
    "Player: " + str(player.get_value())
    print
    "Dealer: " + str(dealer.get_value())
    in_play = False
    outcome = "New deal?"


# draw handler
def draw(canvas):
    global in_play, score
    canvas.draw_text("Blackjack", [200, 50], 40, "Black")
    canvas.draw_text("Dealer", [100, 150], 30, "Black")
    canvas.draw_text("Player", [100, 350], 30, "Black")
    canvas.draw_text(outcome, [250, 350], 25, "Black")
    canvas.draw_text(winner, [250, 150], 25, "Black")
    canvas.draw_text("Score: " + str(score), [450, 50], 25, "Black")
    dealer.draw(canvas, [200, 200])
    player.draw(canvas, [200, 400])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [200, 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()