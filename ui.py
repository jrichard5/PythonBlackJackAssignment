#/usr/bin/env python3

from datetime import datetime, time
import locale
from decimal import Decimal

#import richard_blackjack16_business as Business
from objects import Session, Hand
import db


################################################################
################################################################
################################################################
################################################################
class Person:
    def __init__(self, name):
        self.__name = name
        self.__hand = Hand()
        self.__blackjack = False


    def showHand(self):
        if (self.__name == "You"):
            print(self.__name + "r cards.")
        else:
            print(self.__name + "'s cards:")
        print(self.__hand)
        print()

    def resetHand(self):
        self.__hand = Hand()
        self.__blackjack = False

    @property
    def name(self):
        return self.__name

    @property
    def hand(self):
        return self.__hand

    @property
    def blackjack(self):
        return self.__blackjack

    @blackjack.setter
    def blackjack(self, value):
        if (value == True or value == False):
            self.__blackjack = value
        else:
            raise ValueError("Must be True or False")

class Player(Person):
    def __init__(self, name):
        Person.__init__(self, name)
        self.__money = Decimal(db.readLastStopMoney())
        self.__money = self.__money.quantize(Decimal("1.00"))
        self.__addedMoney = 0



    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, value):
        rounded = Decimal(value)
        self.__money = rounded

    @property
    def addedMoney(self):
        return self.__addedMoney

    @addedMoney.setter
    def addedMoney(self, value):
        self.__addedMoney = value


################################################################
################################################################
################################################################
def displayTitle():
    print("BlackJack")
    print("Blackjack payout is 3:2")
    print()
    print()

def getStartTime():
    startTime = datetime.now()
    stringStart = startTime.strftime("%I:%M:%S %p")
    print("Start time:  " + stringStart)
    return startTime

def printEndTime(startTime):
    endTime = datetime.now()
    timeElapsed = endTime - startTime
    timeElapsed = timeElapsed.seconds

    #get timeElapsed into hours, mintues, seconds
    elapsedMinutes = timeElapsed // 60
    elapsedSeconds = timeElapsed % 60
    elapsedHours = elapsedMinutes // 60
    elapsedMinutes = elapsedMinutes % 60

    elapsedTime = time(elapsedHours, elapsedMinutes, elapsedSeconds)

    stringEnd = endTime.strftime("%I:%M:%S %p")

    #print both end time and elapsedTime
    print("Stop Time:  " + stringEnd)
    print("Elapsed Time:  ", elapsedTime)

    return endTime


def main():
    displayTitle()
    userInput = ""
    startTime = getStartTime()
    locale.setlocale(locale.LC_ALL, 'en_US')

    player = Player("You")

    startMoney = player.money



    while True:
        player.resetHand()
        currentGame = Business.BlackjackGame(player)
        currentGame.playBlackjack()
        userInput = str.lower(input("Play again? (y/n): "))

        while (not(userInput == "n" or userInput == "y")):
            print("Not a valid choice.  Please try again.")
            userInput = str.lower(input("Play again? (y/n): "))

        if (userInput == "n"):
            break
        print()

    endTime = printEndTime(startTime)
    endMoney = player.money
    addedMoney = player.addedMoney

    sessionData = Session(startTime, startMoney, addedMoney, endTime, endMoney)
    sessionData.saveSession()

    print("Come back soon!")

if __name__ == "__main__":
    main()