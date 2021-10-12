#/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import locale
from decimal import Decimal
from decimal import InvalidOperation
from datetime import datetime, time


import ui
import objects


class MainFrameOfBlackJack(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent
        self.player = ui.Player("You")
        locale.setlocale(locale.LC_ALL, 'en_US')

        self.currentMoney = tk.StringVar()
        self.betAmount = tk.StringVar()
        self.dealerCards = tk.StringVar()
        self.dealerPoints = tk.StringVar()
        self.playerCards = tk.StringVar()
        self.playerPoints = tk.StringVar()
        self.gameResult = tk.StringVar()

        self.currentMoney.set(locale.currency(self.player.money, grouping=True))
        self.gameFinished = True

        self.newBlackjackgame = GUIBlackjack(self.player, 0)


        self.initComponents()

        self.startTime = datetime.now()
        self.startMoney = self.player.money

    def initComponents(self):
        self.pack()
        ttk.Label(self, text="Money:  ").grid(column=0, row =0, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.currentMoney, state="readonly").grid(column =1, row =0)


        ttk.Label(self, text="Bet:  ").grid(column=0, row =1, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.betAmount).grid(column =1, row =1)

        ttk.Label(self, text="DEALER").grid(column=0, row=2, sticky=tk.E)

        ttk.Label(self, text="YOU").grid(column=0, row=5, sticky=tk.E)

        self.resetHandUI()
        self.createHitStand()
        self.createPlayExit()

    def resetHandUI(self):

        ttk.Label(self, text="Cards:  ").grid(column=0, row = 3, sticky=tk.E)
        ttk.Entry(self, width=50, textvariable=self.dealerCards,state="readonly").grid(column =1, row = 3, sticky=tk.W)

        ttk.Label(self, text="Points:  ").grid(column = 0, row = 4, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.dealerPoints, state="readonly").grid(column = 1, row = 4, sticky=tk.W)

        ttk.Label(self, text="Cards:  ").grid(column=0, row = 6, sticky=tk.E)
        ttk.Entry(self, width=50, textvariable=self.playerCards,state="readonly").grid(column =1, row = 6, sticky=tk.W)

        ttk.Label(self, text="Points:  ").grid(column = 0, row = 7, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.playerPoints, state="readonly").grid(column = 1, row = 7, sticky=tk.W)

        ttk.Label(self, text="RESULT:  ").grid(column = 0, row = 9, sticky=tk.E)
        ttk.Entry(self, width=50, textvariable=self.gameResult, state="readonly").grid(column = 1, row = 9, sticky=tk.W)

        for child in self.winfo_children():
            child.grid_configure(padx=7, pady=4)

    def createHitStand(self):
        hitButtonFrame = ttk.Frame(self)
        hitButtonFrame.grid(column = 1, row = 8, columnspan=2)

        ttk.Button(hitButtonFrame, text="Hit", command=self.hitCommand).grid(column = 0, row = 0)                      #??????
        ttk.Button(hitButtonFrame, text="Stand", command=self.standCommand).grid(column = 1, row = 0)

    def createPlayExit(self):
        playButtonFrame = ttk.Frame(self)
        playButtonFrame.grid(column = 1, row = 10, columnspan=2)

        ttk.Button(playButtonFrame, text="Play", command=self.playCommand).grid(column = 0, row = 0)
        ttk.Button(playButtonFrame, text="Exit", command=self.exitCommand).grid(column = 1, row = 0)

    def playCommand(self):
        if(self.gameFinished):
            self.player.resetHand()
            self.dealerCards.set("")
            self.playerCards.set("")
            self.playerPoints.set("")
            self.dealerPoints.set("")
            currentBetAmount = 0
            money = Decimal(self.player.money)
            try:
                currentBetAmount = Decimal(self.betAmount.get())
                if (currentBetAmount > money):
                    print("You don't have enough chips")
                elif (currentBetAmount < 5 or currentBetAmount > 1000):
                    print("This table has a minimum bet of 5 and a maximum bet of 1000")
                else:
                    self.gameFinished = False
                    self.newBlackjackgame = GUIBlackjack(self.player, currentBetAmount)
                    playerBlackjack = self.newBlackjackgame.dealStartCards()
                    self.dealerCards.set(self.newBlackjackgame.updateDealerHandBefore())
                    self.playerCards.set(self.newBlackjackgame.updatePlayerHand())
                    self.playerPoints.set(str(self.newBlackjackgame.player.hand.getPoints()))
                    self.newBlackjackgame.playerTurn = True



            except InvalidOperation:
                print(currentBetAmount)
                self.gameResult.set("You must enter a number in bet before you can play")

    def hitCommand(self):
        if (self.newBlackjackgame.playerTurn):
            self.newBlackjackgame.givePlayerCard()
            self.playerCards.set(self.newBlackjackgame.updatePlayerHand())
            self.playerPoints.set(str(self.newBlackjackgame.player.hand.getPoints()))
            if (self.newBlackjackgame.player.hand.getPoints() > 21):
                self.finish()

    def standCommand(self):
        if (self.newBlackjackgame.playerTurn):
            self.finish()
            self.newBlackjackgame.playerTurn = False

    def finish(self):
        self.dealerCards.set(self.newBlackjackgame.updateDealerHand())
        self.dealerPoints.set(str(self.newBlackjackgame.dealer.hand.getPoints()))
        self.newBlackjackgame.afterTurn()
        self.dealerCards.set(self.newBlackjackgame.updateDealerHand())
        self.dealerPoints.set(str(self.newBlackjackgame.dealer.hand.getPoints()))
        self.gameResult.set(self.newBlackjackgame.resultString)
        self.currentMoney.set(locale.currency(self.player.money, grouping=True))
        self.gameFinished = True


    def exitCommand(self):
        endTime = datetime.now()
        endMoney =self.player.money
        addedMoney = 0  #Can't add money in this GUI
        sessionData = objects.Session(self.startTime, self.startMoney, addedMoney, endTime, endMoney)
        sessionData.saveSession()
        self.parent.destroy()





#############
#############





class Dealer(ui.Person):
    def __init__(self, name):
        ui.Person.__init__(self, name)

    def showHandBefore(self):
        print(self.name + "'s cards:")
        print(self.hand.cards[0])
        print("????Another Card face down????")
        print()

    def valueOnlyStringBefore(self):
        string = ""
        string += self.hand.cards[0].value
        return string


###########################
##########################
#########################

class GUIBlackjack:
    def __init__(self, player, betAmount):
        self.__deck = objects.Deck()
        self.__deck.shuffleCards()
        self.__player = player
        self.__dealer = Dealer("Dealer")
        self.__end = False
        self.__betAmount = betAmount
        self.playerTurn = False
        self.resultString = ""
        self.playerPoints = ""

    @property
    def end(self):
        return self.__end

    @property
    def player(self):
        return self.__player

    @property
    def dealer(self):
        return self.__dealer


    def dealStartCards(self):
        self.__player.hand.addCard(self.__deck.cardDraw())
        self.__dealer.hand.addCard(self.__deck.cardDraw())
        self.__player.hand.addCard(self.__deck.cardDraw())
        self.__dealer.hand.addCard(self.__deck.cardDraw())

        if (self.__player.hand.getPoints() == 21):
            self.__player.blackjack = True
            if (self.__dealer.hand.getPoints() == 21):
                self.__dealer.blackjack = True
            self.playerTurn = False

    def updateDealerHandBefore(self):
        return self.__dealer.valueOnlyStringBefore()

    def updatePlayerHand(self):
        return self.__player.hand.valueOnlyString()

    def updateDealerHand(self):
        return self.__dealer.hand.valueOnlyString()


    def givePlayerCard(self):
        self.__player.hand.addCard(self.__deck.cardDraw())
        if (self.__player.hand.getPoints() > 21):
            self.__end = True
            self.resultString =(self.__player.name + " busted with " + str(self.__player.hand.getPoints()) +" :(")
            self.__player.money = (self.__player.money - self.__betAmount)
            self.playerTurn = False


    def afterTurn(self):
        if (self.__end == False):
            if (self.__dealer.hand.getPoints() == 21):
                self.__dealer.blackjack = True
            while (self.__dealer.hand.getPoints() < 17):
                self.__dealer.hand.addCard(self.__deck.cardDraw())
            if (self.__dealer.hand.getPoints() > 21):
                self.resultString = ("Yay! The dealer busted. You win!")
                self.__player.money = self.__player.money + self.__betAmount
                self.__end = True
        if (self.__end == False):
            playerPoints = self.__player.hand.getPoints()
            dealerPoints = self.__dealer.hand.getPoints()


            #checks to see who has blackjack
            if (self.__player.blackjack and self.__dealer.blackjack):
                self.resultString = ("Both dealer and player have blackjack, :O")
            elif (self.__player.blackjack):
                self.resultString =(self.__player.name + " win with blackjack")
                self.resultString =(self.__player.name + " won " + str(self.__betAmount * Decimal("1.5")))
                self.__player.money = self.__player.money + (self.__betAmount * Decimal("1.5"))
            elif (self.__dealer.blackjack):
                self.resultString =("Dealer wins with blackjack")


            #No one has blackjack, compares points
            else:
                if (playerPoints == dealerPoints):
                    self.resultString =("Draw")
                elif (playerPoints > dealerPoints):
                        self.resultString =(self.__player.name + " win!")
                        self.__player.money = self.__player.money + self.__betAmount
                else:
                    self.resultString=(self.__dealer.name + " wins.")
                    self.__player.money = self.__player.money - self.__betAmount

        #print("Money: " + locale.currency(self.__player.money, grouping=True))




##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################
#old stuff

    def dealToPlayer(self, option):
        if (self.__player.hand.getPoints() < 21):
            while (self.__player.hand.getPoints() < 21):
                userInput = option
                print()
                if (userInput == "hit"):
                    self.__player.hand.addCard(self.__deck.cardDraw())
                    self.__player.showHand()
                elif (userInput == "stand"):
                    break
                else:
                    print("Not a valid input")
            if (self.__player.hand.getPoints() > 21):
                self.__end = True
                print(self.__player.name + " busted with " + str(self.__player.hand.getPoints()) +" :(")
                self.__player.money = (self.__player.money - self.__betAmount)
                print()
        else:
            print(self.__player.name + " have Blackjack!")
            self.__player.blackjack = True
            self.__dealer.showHand()
            if (self.__dealer.hand.getPoints() == 21):
                self.__dealer.blackjack = True

    def dealToDealer(self):
        if (self.__end == False):
            self.__dealer.showHand()
            if (self.__dealer.hand.getPoints() == 21):
                self.__dealer.blackjack = True
            while (self.__dealer.hand.getPoints() < 17):
                self.__dealer.hand.addCard(self.__deck.cardDraw())
                self.__dealer.showHand()
            if (self.__dealer.hand.getPoints() > 21):
                print("Yay! The dealer busted. You win!")
                print()
                self.__player.money = self.__player.money + self.__betAmount
                self.__end = True

    def determineWinner(self):
        if (self.__end == False):
            playerPoints = self.__player.hand.getPoints()
            dealerPoints = self.__dealer.hand.getPoints()
            print()

            print("Your points:  " + str(playerPoints))
            print("Dealer's points:  " + str(dealerPoints))


            #checks to see who has blackjack
            if (self.__player.blackjack and self.__dealer.blackjack):
                print("Both dealer and player have blackjack, :O")
            elif (self.__player.blackjack):
                print(self.__player.name + " win with blackjack")
                print(self.__player.name + " won " + str(self.__betAmount * Decimal("1.5")))
                self.__player.money = self.__player.money + (self.__betAmount * Decimal("1.5"))
            elif (self.__dealer.blackjack):
                print("Dealer wins with blackjack")


            #No one has blackjack, compares points
            else:
                if (playerPoints == dealerPoints):
                    print("Draw")
                elif (playerPoints > dealerPoints):
                        print (self.__player.name + " win!")
                        self.__player.money = self.__player.money + self.__betAmount
                else:
                    print (self.__dealer.name + " wins.")
                    self.__player.money = self.__player.money - self.__betAmount

            print()
        print("Money: " + locale.currency(self.__player.money, grouping=True))
        print()

    def playBlackjack(self):
        self.dealStartCards()
        self.dealToPlayer()
        self.dealToDealer()
        self.determineWinner()

##old stuff
##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Blackjack")
    MainFrameOfBlackJack(root)
    root.mainloop()


