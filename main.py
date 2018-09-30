from InputHandler import getch
from Entities import *

deck = Deck()
print(deck.drawCard())

hp = HumanPlayer(deck)

gc = GameController()

gc.startGame()