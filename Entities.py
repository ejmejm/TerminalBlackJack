import random
from InputHandler import getch

name_val = {'Ace': 11, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 'Jack': 10, 'Queen': 10, 'King': 10}

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

    def handToStr(self):
        string = ''
        for card in self.cards:
            string += str(card.name) + ' of ' + card.suit[0].upper() + card.suit[1:] + 's, ')
        return string[:-2]


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

    def checkGameOver(self, player1, player2=None):
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
            ai = player2
            print('You get to draw first!\n\n')
        else:
            player1 = AIPlayer(deck)
            player2 = HumanPlayer(deck)
            human = player2
            ai = player1

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
            
        self.postGame()

    def postGame(self, human, ai):
       if human.state == 'win':
            print('You hit 21! You win!')
        elif human.state == 'bust':
            print('You busted :(')
       elif ai.state == 'win':
            print('Your opponent won by hitting 21')
        elif ai.state == 'bust':
            print('Your opponent busted and you won!')
        elif human.total_value > ai.total_value:
            print('You have a better hand than opponent, you win!')
        elif ai.total_value > human.total_value:
            print('Your oppenent had a better hand than you, better luck next time')
        else:
            print('The game was a draw :O')

        print()
        print('Your hand:')
        print(human.handToStr())
        print()
        print('Opponent\'s hand:')
        print(ai.handToStr())

