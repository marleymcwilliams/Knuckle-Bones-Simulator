import random
from random import shuffle

def New_Game(P):

    try:
        P = int(P)
        if P <= 1:
            print("You need at least 2 players.")
            return New_Game(input("I want to play with this many people: ").lower())
        if P > 13:
            print("Too many players. You can play with 13 at most.")
            return New_Game(input("I want to play with this many people: ").lower())
    except ValueError:
        print("Enter a number")
        return New_Game(input("I want to play with this many people: ").lower())

    #Setting up the deck

    Total_deck = [
        -2,-2,
        0,0,
        1,1,1,1,
        2,2,2,2,
        3,3,3,3,
        4,4,4,4,
        5,5,5,5,
        6,6,6,6,
        7,7,7,7,
        8,8,8,8,
        9,9,9,9,
        10,10,10,10,
        11,11,11,11,
        12,12,12,12,
        13,13]
    shuffle(Total_deck)

    #Setting up game parameters

    pdata = {}

    Memory = []

    for i in range(1,P+1):
        pdata["Player",i] = []
        pdata["Insight",i] = {}

        #Distributing Cards
        
        for j in range(0,4):
            selection = random.randint(0,len(Total_deck)-1)
            pdata["Player",i].append(Total_deck.pop(selection))

        print("Player",i,"Hand:",pdata["Player",i])

        #Establishing Each Players' insight
        
        for k in range(1,P+1):
            if k != i:
                pdata["Insight",i][k] = ["?","?","?","?"]
            else:
                pdata["Insight",i][k] = [pdata["Player",i][0],pdata["Player",i][1],"?","?"]

        for x in pdata["Insight",i]:
            print("      ",x,":",pdata["Insight",i][x])
        print("")

    Discard = [Total_deck.pop(random.randint(0,len(Total_deck)-1))]

    TrueBoo = False
    
    print("Deck:",Total_deck)
    print("Discard:", Discard)
    for i in range(1,P+1):
        pdata["Insight",i]["Discard"] = Discard
        pdata["Insight",i]["Deck"] = "{} Cards left".format(len(Total_deck))

    print("")

    def Insight(i):
        print("")
        print("Player",i,"insight:")
        for x in pdata["Insight",i]:
            print("      ",x,":",str(pdata["Insight",i][x]).replace("'",""))
        print("      ","Memory:", Memory)
        print("")
    
    def turn(i,boo):

        if boo == False:
            ability = ", Call (Red King)"
        else:
            ability = ""
        
        Jump = True
        
        print("")
        print("Player {}'s Turn:".format(i))
        print("")

        choice = input("What do you want to do? [Draw, Insight, Retrieve (from discard){}] ".format(ability)).lower()
        options = ["draw","insight","retrieve","call"]

        boolean = False
        breakerOmega = False

        def sharing(store):
            choice4 = input("Do you want to pair the {} with your or another player's card? [Yes, No] ".format(store)).lower()

            breaker2 = False
            
            while True:
                if choice4 in ["no","n"]:
                    return
            
                if choice4 in ["yes","y"]:
                    print("")
                    choice5 = input("Which player? [1 through {}] ".format(P)).lower()

                    breaker3 = False
                    while True:
                        if isint(choice5) == True:
                            choice5 = int(choice5)
                            if choice5 in range(1,P+1):
                                
                                preview2 = []
                                for h in range(1,len(pdata["Player",choice5])+1):
                                    preview2.append(h)
                                print("")
                                print("Player {}s' Indexes:".format(choice5),preview2)
                                
                                choice6 = input("Which index? [1 through {}] ".format(len(pdata["Player",choice5]))).lower()

                                breaker4 = False
                                while True:
                                    if isint(choice6) == True:
                                        choice6 = int(choice6)
                                        if choice6 in range(1,len(pdata["Player",choice5])+1):
                                            print("")
                                            if i == choice5:
                                                print("Exposing your second card, you had a {}.".format(pdata["Player",i][choice6-1]))
                                            else:
                                                print("Exposing their card, they had a {}.".format(pdata["Player",choice5][choice6-1]))
                                            print("")

                                            diff = int(store) - int(pdata["Player",choice5][choice6-1])

                                            if int(diff) in [-15,0,15]:
                                                if i == choice5:
                                                    print("You place both your cards down and end your turn.")

                                                    Discard.append(int(pdata["Player",choice5][choice6-1]))

                                                    for l in range(1,P+1):
                                                        del(pdata["Insight",l][i][choice6-1])
                                                    del(pdata["Player",i][choice6-1])
                                                    
                                                if i != choice5:
                                                    print("You take player {}'s card and place it with yours, ending your turn. They replace it by drawing from the deck.".format(choice5))

                                                    Discard.append(int(pdata["Player",choice5][choice6-1]))
                                                    
                                                    pdata["Player",choice5][choice6-1] = int(Total_deck.pop(0))
                                                    for l in range(1,P+1):
                                                        pdata["Insight",l][choice5][choice6-1] = "?"
                                                        
                                                
                                                Jump = False
                                                breaker2 = True
                                                    
                                            else:
                                                if i == choice5:
                                                    print("You turn your card back over and add an additional card from the deck to your hand.")
                                                else:
                                                    print("You turn player {}'s card back over and add an additional card from the deck to your hand.".format(choice5))
                                                print("")

                                                pdata["Player",i].append(Total_deck.pop(0))
                                                for l in range(1,P+1):
                                                    pdata["Insight",l][choice5][choice6-1] = pdata["Player",choice5][choice6-1]
                                                    pdata["Insight",l][i].append("?")

                                                choice7 = input("You can try again to pair your or another's card with the {}. Do you want to? [Yes, No] ".format(store)).lower()

                                                while True:
                                                    if choice7 in ["yes","y"]:
                                                        breaker2 = False
                                                        breaker5 = True
                                                    elif choice7 in ["no","n"]:
                                                        breaker2 = True
                                                        breaker5 = True
                                                    else:
                                                        print("Yes or No")
                                                        print("")
                                                        choice7 = input("You can try again to pair your or another's card with the {}. Do you want to? [Yes, No] ".format(card)).lower()

                                                    if breaker5 == True:
                                                        break
                                            
                                            breaker4 = True
                                            break
                                            
                                        else:
                                            print("That's outside the range.")
                                            print("")
                                            choice6 = input("Which index? [1 through {}] ".format(len(pdata["Player",choice5]))).lower()
                                    else:
                                        print("Please enter an integer")
                                        print("")
                                        choice6 = input("Which index? [1 through {}] ".format(len(pdata["Player",choice5]))).lower()
                                    if breaker4 == True:
                                        break
                                    
                                breaker3 = True
                                
                            else:
                                print("That's outside the range.")
                                print("")
                                choice5 = input("Which player? [1 through {}] ".format(P)).lower()
                        else:
                            print("Please enter an integer")
                            print("")
                            choice5 = input("Which player? [1 through {}] ".format(P)).lower()
                        if breaker3 == True:
                            break
                    
                else:
                    print("Yes or No")
                    print("")
                    choice4 = input("Do you want to pair the {} with your or another player's card? [Yes, No] ".format(card)).lower()
                    
                if breaker2 == True:
                    break

            breaker = True

        def Tomfuckery(know):
            message = "Choose an index to replace [1 through {}]: ".format(len(pdata["Insight",i][x]))

            preview = []
            for h in range(1,len(pdata["Player",i])+1):
                preview.append(h)
            print("")
            print("Indexes:",preview)

            choice3 = input(message).lower()
            breaker = False
            
            while True:
                if isint(choice3) == True:
                    choice3 = int(choice3)
                    
                    if int(choice3) in range(1,len(pdata["Insight",i][x])+1):
                        print("")
                        print("You replace your {} for a {}.".format(pdata["Player",i][choice3-1],card))

                        pdata["Player",i][choice3-1], store = card, pdata["Player",i][choice3-1]
                        for l in range(1,P+1):
                            pdata["Insight",l][i][choice3-1] = "?"
                        pdata["Insight",i][i][choice3-1] = card

                        if know == True:
                            for l in range(1,P+1):
                                pdata["Insight",l][i][choice3-1] = card
                        else:
                            pdata["Insight",i][i][choice3-1] = card

                        Discard.append(store)

                        sharing(store)

                        breaker = True

                    else:
                        print("That's outside the range.")
                        print("")
                        choice3 = input(message).lower()
                else:
                    print("Please enter an integer")
                    print("")
                    choice3 = input(message).lower()

                if breaker == True:
                    break

        while True:
            if choice not in options:
                print("That's not an option.")
                print("")
                if boolean == True:
                    choice = input("What do you want to do? [Draw, Retrieve (from discard){}] ".format(ability)).lower()
                else:
                    choice = input("What do you want to do? [Draw, Insight, Retrieve (from discard){}] ".format(ability)).lower()

            if choice == "insight":
                Insight(i)
                boolean = True
                choice = input("What do you want to do? [Draw, Retrieve (from discard){}] ".format(ability)).lower()

            if choice == "call":
                if boo == False:
                    TrueBoo = True
                    return TrueBoo
                else:
                    print("Someone has already called Red King.")
                    if boolean == True:
                        choice = input("What do you want to do? [Draw, Retrieve (from discard){}] ".format(ability)).lower()
                    else:
                        choice = input("What do you want to do? [Draw, Insight, Retrieve (from discard){}] ".format(ability)).lower()
                        

            if choice == "retrieve":
                breakerOmega = True
                
                card = Discard[len(Discard)-1]
                del(Discard[len(Discard)-1])
                
                print("You pull the {} from the Discard pile.".format(card))
                
                Tomfuckery(True)


            if choice == "draw":
                breakerOmega = True
                
                card = int(Total_deck.pop(0))
                print("Drawing from the deck. It's a {}.".format(card))
                print("")
                
                choice2 = input("Will you replace one of your own? [Yes, No] ").lower()
                breaker0 = False

                while True:
                    if choice2 in ["yes","y"]:

                        ####STUFFFFFF
                        
                        Tomfuckery(False)
                        breaker0 = True
                        
                    elif choice2 in ["no","n"]:
                        print("You place the {} in the discard pile.".format(card))
                        print("")
                        if card in [13]:
                            other = input("You can look at another player's cards and have the option to trade. Which player? [1 through {}] ".format(P)).lower()

                            breakerGamma = False

                            while True:
                                if isint(other) == True:
                                    other = int(other)
                                    
                                    if other in range(1,P+1):
                                        preview2 = []
                                        for h in range(1,len(pdata["Player",other])+1):
                                            preview2.append(h)
                                        print("")
                                        
                                        print("Player {}s' Indexes:".format(other),preview2)
                                
                                        otherIndex = input("Which index? [1 through {}] ".format(len(pdata["Player",other]))).lower()

                                        breakerZeta = False

                                        while True:
                                            if isint(otherIndex) == True:
                                                otherIndex = int(otherIndex)
                                                
                                                if otherIndex in range(1,len(pdata["Player",other])+1):
                                                    print("")
                                                    print("You glance at the card. It's a {}.".format(pdata["Player",other][otherIndex-1]))
                                                    print("")
                                                    
                                                    trade = input("Do you want to trade a card with them? [Yes, No] ").lower()

                                                    breakerPeta = False
                                                    
                                                    while True:
                                                        if trade in ["yes","y"]:

                                                            preview = []
                                                            for h in range(1,len(pdata["Player",i])+1):
                                                                preview.append(h)
                                                            print("")
                                                            print("Indexes:",preview)

                                                            choice3 = input("Choose an index to replace [1 through {}]: ".format(len(pdata["Insight",i][x]))).lower()
                                                            breaker = False
                                                            
                                                            while True:
                                                                if isint(choice3) == True:
                                                                    choice3 = int(choice3)
                                                                    
                                                                    if choice3 in range(1,len(pdata["Insight",i][x])+1):
                                                                        print("")
                                                                        print("You replace your card for their {}.".format(pdata["Player",other][otherIndex-1]))

                                                                        for l in range(1,P+1):
                                                                            pdata["Insight",l][i][choice3-1], pdata["Insight",l][other][otherIndex-1] = pdata["Insight",l][other][otherIndex-1], pdata["Insight",l][i][choice3-1]
                                                                        pdata["Player",i][choice3-1], pdata["Player",other][otherIndex-1] = pdata["Player",other][otherIndex-1], pdata["Player",i][choice3-1]

                                                                        breaker = True

                                                                    else:
                                                                        print("That's outside the range.")
                                                                        print("")
                                                                        choice3 = input(message).lower()
                                                                else:
                                                                    print("Please enter an integer")
                                                                    print("")
                                                                    choice3 = input(message).lower()

                                                                if breaker == True:
                                                                    break

                                                            breakerPeta = True
                                                        elif trade in ["no","n"]:
                                                            pdata["Insight",i][other][otherIndex-1] = pdata["Player",other][otherIndex-1]
                                                            print("")
                                                            
                                                            breakerPeta = True
                                                        else:
                                                            print("Yes or No.")
                                                            print("")
                                                            trade = input("Do you want to trade a card with them? [Yes, No] ").lower()
                                                            
                                                        if breakerPeta == True:
                                                            break

                                                    breakerZeta = True
                                                else:
                                                    print("That's outside the range.")
                                                    print("")
                                                    otherIndex = input("Which index? [1 through {}] ".format(len(pdata["Player",other]))).lower()
                                            else:
                                                print("Please enter an integer.")
                                                print("")
                                                otherIndex = input("Which index? [1 through {}] ".format(len(pdata["Player",other]))).lower()

                                            if breakerZeta == True:
                                                break

                                        breakerGamma = True
                                    else:
                                        print("That's outside the range.")
                                        print("")
                                        other = input("You can look at another player's cards. Which player? [1 through {}] ".format(P)).lower()
                                else:
                                    print("Please enter an integer.")
                                    print("")
                                    other = input("You can look at another player's cards. Which player? [1 through {}] ".format(P)).lower()
                                
                                if breakerGamma == True:
                                    break


                            breaker0 = True


                        elif card in [11,12]:
                            trade = input("You can blind swap with another player's cards. Do you want to? [Yes, No] ".format(P)).lower()

                            breakerZhi = False

                            while True:
                                if trade in ["no","n"]:

                                    breakerZhi = True

                                elif trade in ["yes","y"]:
                                    print("")
                                    other = input("Which player do you want to swap with? [1 through {}] ".format(P)).lower()

                                    breakerGamma = False

                                    while True:
                                        if isint(other) == True:
                                            other = int(other)
                                            
                                            if other in range(1,P+1):
                                                preview2 = []
                                                for h in range(1,len(pdata["Player",other])+1):
                                                    preview2.append(h)
                                                print("")
                                                
                                                print("Player {}s' Indexes:".format(other),preview2)
                                        
                                                otherIndex = input("Which index? [1 through {}] ".format(len(pdata["Player",other]))).lower()

                                                breakerZeta = False

                                                while True:
                                                    if isint(otherIndex) == True:
                                                        otherIndex = int(otherIndex)
                                                        
                                                        if otherIndex in range(1,len(pdata["Player",other])+1):
                                                            preview = []
                                                            for h in range(1,len(pdata["Player",i])+1):
                                                                preview.append(h)
                                                            print("")
                                                            print("Indexes:",preview)

                                                            choice3 = input("Choose an index to replace [1 through {}]: ".format(len(pdata["Insight",i][x]))).lower()
                                                            breaker = False
                                                            
                                                            while True:
                                                                if isint(choice3) == True:
                                                                    choice3 = int(choice3)
                                                                    
                                                                    if choice3 in range(1,len(pdata["Insight",i][x])+1):
                                                                        print("")
                                                                        print("You replace your card for their card.")
                                                                        print("")

                                                                        for l in range(1,P+1):
                                                                            pdata["Insight",l][i][choice3-1], pdata["Insight",l][other][otherIndex-1] = pdata["Insight",l][other][otherIndex-1], pdata["Insight",l][i][choice3-1]
                                                                        pdata["Player",i][choice3-1], pdata["Player",other][otherIndex-1] = pdata["Player",other][otherIndex-1], pdata["Player",i][choice3-1]

                                                                        breaker = True

                                                                    else:
                                                                        print("That's outside the range.")
                                                                        print("")
                                                                        choice3 = input(message).lower()
                                                                else:
                                                                    print("Please enter an integer")
                                                                    print("")
                                                                    choice3 = input(message).lower()

                                                                if breaker == True:
                                                                    break

                                                            breakerZeta = True
                                                        
                                                        else:
                                                            print("That's outside the range.")
                                                            print("")
                                                            otherIndex = input("Which index? [1 through {}] ".format(len(pdata["Player",other]))).lower()
                                                    else:
                                                        print("Please enter an integer.")
                                                        print("")
                                                        otherIndex = input("Which index? [1 through {}] ".format(len(pdata["Player",other]))).lower()

                                                    if breakerZeta == True:
                                                        break

                                                breakerGamma = True
                                            else:
                                                print("That's outside the range.")
                                                print("")
                                                other = input("You can look at another player's cards. Which player? [1 through {}] ".format(P)).lower()
                                        else:
                                            print("Please enter an integer.")
                                            print("")
                                            other = input("You can look at another player's cards. Which player? [1 through {}] ".format(P)).lower()
                                        
                                        if breakerGamma == True:
                                            break

                                    breakerZhi = True

                                else:
                                    print("Yes or No.")
                                    print("")
                                    trade = input("You can blind swap with another player's cards. Do you want to? [Yes, No] ".format(P)).lower()
                                    

                                if breakerZhi == True:
                                    break




                        elif card in [9,10]:
                            other = input("You can look at another player's cards. Which player? [1 through {}] ".format(P)).lower()

                            breakerGamma = False

                            while True:
                                if isint(other) == True:
                                    other = int(other)
                                    
                                    if other in range(1,P+1):
                                        preview2 = []
                                        for h in range(1,len(pdata["Player",other])+1):
                                            preview2.append(h)
                                        print("")
                                        
                                        print("Player {}s' Indexes:".format(other),preview2)
                                
                                        otherIndex = input("Which index? [1 through {}] ".format(len(pdata["Player",other]))).lower()

                                        breakerZeta = False

                                        while True:
                                            if isint(otherIndex) == True:
                                                otherIndex = int(otherIndex)
                                                
                                                if otherIndex in range(1,len(pdata["Player",other])+1):
                                                    print("")
                                                    print("You glance at the card. It's a {}.".format(pdata["Player",other][otherIndex-1]))
                                                    print("")

                                                    pdata["Insight",i][other][otherIndex-1] = pdata["Player",other][otherIndex-1]

                                                    breakerZeta = True
                                                else:
                                                    print("That's outside the range.")
                                                    print("")
                                                    otherIndex = input("Which index? [1 through {}] ".format(len(pdata["Player",other]))).lower()
                                            else:
                                                print("Please enter an integer.")
                                                print("")
                                                otherIndex = input("Which index? [1 through {}] ".format(len(pdata["Player",other]))).lower()

                                            if breakerZeta == True:
                                                break

                                        breakerGamma = True
                                    else:
                                        print("That's outside the range.")
                                        print("")
                                        other = input("You can look at another player's cards. Which player? [1 through {}] ".format(P)).lower()
                                else:
                                    print("Please enter an integer.")
                                    print("")
                                    other = input("You can look at another player's cards. Which player? [1 through {}] ".format(P)).lower()
                                
                                if breakerGamma == True:
                                    break


                            breaker0 = True


                        elif card in [7,8]:
                            preview = []
                            for h in range(1,len(pdata["Player",i])+1):
                                preview.append(h)
                            print("Indexes:",preview)
                            
                            self = input("You can look at one of your own cards. Which index? [1 through {}] ".format(len(pdata["Player",i]))).lower()
                            breakerBeta = False

                            while True:
                                if isint(self) == True:
                                    self = int(self)
                                    
                                    if self in range(1,len(pdata["Player",i])+1):
                                        print("")
                                        print("It's a {}.".format(pdata["Player",i][self-1]))
                                        print("")

                                        pdata["Insight",i][i][self-1] = pdata["Player",i][self-1]

                                        breakerBeta = True
                                    else:
                                        print("That's outside the range.")
                                        print("")
                                        self = input("You can look at one of your own cards. Which index? [1 through {}] ".format(len(pdata["Player",i]))).lower() 
                                else:
                                    print("Please enter an integer")
                                    print("")
                                    self = input("You can look at one of your own cards. Which index? [1 through {}] ".format(len(pdata["Player",i]))).lower()

                                if breakerBeta == True:
                                    break

                        Discard.append(card)
                        
                        breaker0 = True
                            
                        sharing(card)
                        
                    else:
                        print("Yes or No")
                        choice2 = input("Will you replace one of your own? [Yes, No] ").lower()
                        
                    if breaker0 == True:
                        break

            if breakerOmega == True:
                break

    while True:
        for x in range(1,P+1):
            if len(Total_deck) == 0:
                Discard.sort()
                Memory = Discard.copy()
                shuffle(Discard)
                Total_deck = Discard.copy()
                Discard.clear()
                print("")
                print("Reshuffling the deck")
                print("")
            
            for i in range(1,P+1):
                pdata["Insight",i]["Deck"] = "{} Cards left".format(len(Total_deck))

            print("")
            print("██████████████████████████████████████████████████████████████████████████")
            print("--------------------------------------------------------------------------")
            print("██████████████████████████████████████████████████████████████████████████")
            
            if turn(x, TrueBoo) == True:
                TrueBoo = True
        if TrueBoo == True:
            print("")
            rank = []
            for l in range(1,P+1):
                print("Player {}:".format(l),pdata["Player",l])
                print("      ","Total:",sum(pdata["Player",l]))
                rank.append(sum(pdata["Player",l]))
            print("")
            print("Player {} wins!".format(int(rank.index(min(rank)))+1))

            break

def isint(x):     
    try:
        x = int(x)
        return True
    except ValueError:
        return False

def rotate(li):
  return li[-1 % len(li):] + li[:-1 % len(li)]

New_Game(input("I want to play with this many people: ").lower())

#Next Steps: 1. Implement a jump in system (?); 2. Implement a conclusion; 3. Debug

    
