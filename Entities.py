import random

name_val = {'A': 11, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 'J': 10, 'Q': 10, 'K': 10}

class Card():
    def __init__(self, name, suit):
        self.name = name
        self.suit = suit
        self.value = name_val[name]

class Deck():
    def __init__(self):
        self.cards = []
        for key in name_val.keys():
            self.cards.append(Card(key, 'jack'))
            self.cards.append(Card(key, 'diamond'))
            self.cards.append(Card(key, 'heart'))
            self.cards.append(Card(key, 'spade'))
        self.cards = random.shuffle(self.cards)
    def drawCard(self):
        return self.cards.pop()

class Player():
    def __init__(self):
        self.cards = []
        self.total_value = 0
        self.drawCard()
        self.drawCard()

    def drawCard(self, deck):
        card = deck.drawCard()
        self.cards.append(card)
        self.total_value += card.value

    # def recalcTotalValue(self):
    #     self.total_value = 0
    #     for card in self.cards:
    #         self.total_value += card.value

    def reduceAce(self):
        for i in range(len(self.cards)):
            if self.cards[i].value == 11:
                self.cards[i].value = 1
                self.total_value -= 10
                return True
        return False

    def checkEndState(self):
        if self.total_value > 21:
            if not self.reduceAce():
                return 'loss'
        elif self.total_value == 21:
            return 'win'
        return 'continue'