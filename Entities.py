import random
from InputHandler import getch

name_val = {'A': 11, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 'J': 10, 'Q': 10, 'K': 10}

class Card():
    def __init__(self, name, suit):
        self.name = name
        self.suit = suit
        self.value = name_val[name]
    
    def __repr__(self):
        return '[Card: ' + str(self.name) + ' ' + self.suit + 's]'

class Deck():
    def __init__(self):
        self.cards = []
        for key in name_val.keys():
            self.cards.append(Card(key, 'jack'))
            self.cards.append(Card(key, 'diamond'))
            self.cards.append(Card(key, 'heart'))
            self.cards.append(Card(key, 'spade'))
        random.shuffle(self.cards)
    
    def drawCard(self):
        return self.cards.pop()

class Player():
    def __init__(self, deck):
        self.cards = []
        self.deck = deck
        self.total_value = 0
        self.hit()
        self.hit()
        self.state = 'continue' # Possible state include {continue, bust, win, hold}

    def hit(self):
        """Returns the card drawn and the state of the players hand from {bust, win, continue}"""
        card = self.deck.drawCard()
        self.cards.append(card)
        self.total_value += card.value
        self.state = self.checkEndState()
        return card

    def hold(self):
        """Sets the player's stae to hold so they will not recieve any more turns"""
        self.state = 'hold'

    def reduceAce(self):
        """Converts an ace in the hand form value 11 to 1 if it will keep the player from busting"""
        for i in range(len(self.cards)):
            if self.cards[i].value == 11:
                self.cards[i].value = 1
                self.total_value -= 10
                return True
        return False

    def checkEndState(self):
        """Checks if the players had busted or won"""
        if self.total_value > 21:
            if not self.reduceAce():
                return 'bust'
        if self.total_value == 21:
            return 'win'
        return 'continue'

class HumanPlayer(Player):
    def __init__(self, deck):
        super().__init__(deck)

    def takeTurn(self):
        choice = 'X'
        while choice not in '12':
            print('Please press 1 or 2 to take an action:\n1. Hit\n2. Hold\n3. Exit Game')
            choice = getch()

        if choice == '3':
            return 'quit'
        elif choice == '1':
            self.hit()
        else:
            self.hold()

        return self.state

class AIPlayer(Player):
    def __init__(self, deck):
        super().__init__(deck)
    
    def takeTurn(self):
        if random.randint(11, 21) >= self.total_value:
            self.hit()
        else:
            self.hold()

class GameController():
    def clearScreen(self):
        print(chr(27) + '[2J')

    def checkGameOver(player1, player2=None):
        print(player1, player2)
        if player2 is not None:
            if player1.state == 'hold' and player2.state == 'hold':
                return True
        else:
            if player1.state in ['bust', 'win']:
                return True
        return False

    def startGame(self):
        deck = Deck()
        self.clearScreen()

        if random.randint(0, 1) == 1:
            player1 = HumanPlayer(deck)
            player2 = AIPlayer(deck)
            human = player1
            print('You get to draw first!\n\n')
        else:
            player1 = AIPlayer(deck)
            player2 = HumanPlayer(deck)
            human = player2

        while len(deck.cards) > 0:
            print('Your hand:')
            for card in human.cards:
                print(str(card.name) + ' of ' + card.suit[0].upper() + card.suit[1:] + 's')
            print('\nTotal: ' + str(human.total_value)) 
            print('\n\n')

            if player1.state != 'hold':
                player1.takeTurn()
                if self.checkGameOver(player1):
                    break
            if player2.state != 'hold':
                player2.takeTurn()
                if self.checkGameOver(player2):
                    break
            if self.checkGameOver(player1, player2):
                break

            self.clearScreen()
