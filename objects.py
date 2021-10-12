#/usr/bin/env python3

import random
from datetime import datetime, time
import db

class Card:

    def __init__(self, suit, value, points):
        self.__suit = suit
        self.__value = value
        self.__points = points

    @property
    def value(self):
        return self.__value

    @property
    def suit(self):
        return self.__suit

    @property
    def points(self):
        return self.__points

    def __str__(self):
        return (self.__value + " of " + self.__suit)




class Deck:
    def __init__(self):
        self.__cards = []
        #suits = ["Clubs", "Spades", "Hearts", "Diamonds"]
        #values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        #points = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

        dictOfRank = {
            "Ace": 11,
            "2": 2,
            "3":3,
            "4":4,
            "5":5,
            "6":6,
            "7":7,
            "8":8,
            "9":9,
            "10":10,
            "Jack":10,
            "Queen":10,
            "King":10}

        dictOfCards = {
            "Clubs": dictOfRank,
            "Spades": dictOfRank,
            "Hearts": dictOfRank,
            "Diamonds": dictOfRank}

        for suit, dictRP in dictOfCards.items():
            for rank, points in dictRP.items():
                self.__cards.append(Card(suit, rank, points))

        #for card in self.__cards:  #test
        #    print(card) #test


        #old for suit in suits:
        #old     for i in range(len(values)):
        #old         self.__cards.append(Card(suit, values[i], points[i]))

    def shuffleCards(self):
        random.shuffle(self.__cards)

    def cardDraw(self):
        return self.__cards.pop()






class Hand:
    def __init__(self):
        self.__cards = []
        self.__aces = 0


    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        if (self.__index >= len(self.__cards) -1):
            raise StopIteration()
        self.__index += 1
        card = self.__cards[self.__index]
        return card

    def addCard(self, newCard):
        self.__cards.append(newCard)
        if (newCard.value == "Ace"):
            self.__aces +=1


    #loops to get all points
    #if has an ace and over 21, switches aces to a value or 1
    def getPoints(self):
        totalPoints = 0
        for card in self.__cards:
            totalPoints += card.points
        count = 0
        while (totalPoints > 21 and self.__aces > count):
            count +=1
            totalPoints -= 10
        return totalPoints

    def valueOnlyString(self):
        string = ""
        for card in self.__cards:
            string += card.value + " "
        return string

    def cardCount(self):
        return (len(self.__cards))

    def __str__(self):
        string = ""
        for card in self.__cards:
            string += str(card) + "\n"
        return string

    @property
    def cards(self):
        return self.__cards


class Session:
    def __init__(self, startTime, startMoney, addedMoney, stopTime, stopMoney):
        self.__startTime = startTime
        self.__startMoney = startMoney
        self.__addedMoney = addedMoney
        self.__stopTime = stopTime
        self.__stopMoney = stopMoney

    def saveSession(self):
        startString = str(self.__startTime)
        endString = str(self.__stopTime)
        startFloat = float(str(self.__startMoney))
        addedFloat = float(str(self.__addedMoney))
        stopFloat = float(str(self.__stopMoney))

        db.writeSession(startString, startFloat, addedFloat, endString, stopFloat)

    @property
    def startTime(self):
        return self.__startTime

    @property
    def startMoney(self):
        return self.__startMoney

    @property
    def addedMoney(self):
        return self.__addedMoney

    @property
    def stopTime(self):
        return self.__stopTime

    @property
    def stopMoney(self):
        return self.__stopMoney



##_____________________________________________
##----------------------------------------------
##----------------------------------------------
## test stuff

def main():
    hand = Hand()
    deck = Deck()
    for i in range(random.randint(10, 52)):
        hand.addCard(deck.cardDraw())

    for card in hand:
        print(card)

    print("Card Count:  " + str(hand.cardCount()))

if __name__ == "__main__":
    main()
