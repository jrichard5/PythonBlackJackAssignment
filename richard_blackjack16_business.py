#!/usr/bin/env python3

from decimal import Decimal
from decimal import InvalidOperation
import locale


from objects import Deck
from ui import Person


class Dealer(Person):
    def __init__(self, name):
        Person.__init__(self, name)

    def showHandBefore(self):
        print(self.name + "'s cards:")
        print(self.hand.cards[0])
        print("????Another Card face down????")
        print()







class BlackjackGame:
    def __init__(self, player):
        self.__deck = Deck()
        self.__deck.shuffleCards()
        self.__player = player
        self.__dealer = Dealer("Dealer")
        self.__end = False
        self.__betAmount = Decimal("0")


    def doesPlayerHaveMoney(self):
        while (self.__player.money < 5):
            while True:
                print("Money in your account " + locale.currency(self.__player.money, grouping=True))
                moreChipsInput = input("You do not have enough money.  How many chips would you like to buy?  (type 'exit' to quit):  ")
                print()
                if (str.lower(moreChipsInput) == "exit"):
                    self.__end = True
                    break
                try:
                    chips = Decimal(moreChipsInput)
                    self.__player.addedMoney += chips
                    self.__player.money = self.__player.money + chips
                    break
                except TypeError:
                    print("Not a valid number, please try again (type 'exit' to quit)")
                    print()


    def getBetAmount(self):
        while True:
            try:
                print("Money in your account " + locale.currency(self.__player.money, grouping=True))
                betInput = Decimal(input("How much would you like to bet?  "))
                if (betInput < 5 or betInput > 1000):
                    print("Bets need to be between $5 and $1000")
                    print()
                elif (betInput > self.__player.money):
                    print("You do not have that much money")
                    print()
                else:
                    self.__betAmount = betInput
                    break
            except ValueError:
                print("Please enter a valid number")
                print()
            except InvalidOperation:
                print("Not a number")
                print()
        print()


    def dealStartCards(self):
        self.__player.hand.addCard(self.__deck.cardDraw())
        self.__dealer.hand.addCard(self.__deck.cardDraw())
        self.__player.hand.addCard(self.__deck.cardDraw())
        self.__dealer.hand.addCard(self.__deck.cardDraw())



        self.__player.showHand()
        self.__dealer.showHandBefore()

    def dealToPlayer(self):
        if (self.__player.hand.getPoints() < 21):
            while (self.__player.hand.getPoints() < 21):
                userInput = str.lower(input("Hit or Stand? (hit/stand):  "))
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
        self.doesPlayerHaveMoney()
        if (self.__end == False):
            self.getBetAmount()
            self.dealStartCards()
            self.dealToPlayer()
            self.dealToDealer()
            self.determineWinner()


    @property
    def player(self):
        return self.__player

    #@property
    #def dealer(self):
     #   return self.__dealer

#test function
#def main():
#    blackjackz = BlackjackGame()
#    blackjackz.player.hand.addCard(Card("Spade", "10", 10))
#    blackjackz.dealer.hand.addCard(Card("Spade", "9", 9))
#    blackjackz.player.hand.addCard(Card("Spade", "Ace", 11))
#    blackjackz.dealer.hand.addCard(Card("Spade", "Ace", 11))

#    blackjackz.dealToPlayer()
#    blackjackz.dealToDealer()
#    blackjackz.determineWinner()


#if __name__ == "__main__":
#    main()
