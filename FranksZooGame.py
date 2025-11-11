from random import randrange
from itertools import combinations
from os.path import isfile

# IDs
#WHALE = 12
#ELEPHANT = 11
#CROCODILE = 10
#POLARBEAR = 9
#LION = 8
#SEAL = 7
#FOX = 6
#PERCH = 5
#HEDGEHOG = 4
#FISH = 3
#MOUSE = 2
#MOSQUITO = 1
#CHAMELEON = 0

# A card with id 0 cannot be played by itself!
class Animal():

    def __init__( self, name, ordering ):
        self.name = name            # name of animal
        self.id = ordering          # ID of animal
        self.predator = []          # animals that are predator for this animal
        self.prey = []              # animals that are prey for this animal
        self.transform = []         # animals this animal can transform into (mosquito -> elephant)
        self.substitute = []        # animals that can be substituted (mosquito for elephant)
        self.ordering = ordering    # ordering number
        self.number = 5             # How many there are in the deck

    def __repr__( self ):
        return f"{self.name}"

    def __str__( self ):
        return f"{self.name}"

    def __lt__( self, other ):
        return self.ordering < other.ordering

    def __le__( self, other ):
        return self.ordering <= other.ordering

    def __gt__( self, other ):
        return self.ordering > other.ordering

    def __ge__( self, other ):
        return self.ordering >= other.ordering

    #def __repr__( self ):
    #    return f"[{self.name},{self.id},{self.predator},{self.prey},{self.transform}]"


class Hand():

    def __init__( self, cards=[] ):
        self.cards = []
        for card in cards:
            self.cards.append( card )

    def __repr__( self ):
        s = '['
        size = len( self.cards )
        for i in range( size ):
            s += str( self.cards[i].name )
            if i < size-1:
                s += ','
        s += ']'
        return s

    def __len__( self ):
        return len( self.cards )

    def __getitem__( self, index ):
        if index >= len( self ) or index < -len( self ):
            return None
        return self.cards[index]

    def sort( self ):
        self.cards.sort( reverse=True )

    def shuffle( self ):
        size = len(self.cards)
        for i in range(size):
            j = randrange(i,size)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def removeCard( self, card ):
        if card in self.cards:
            self.cards.remove( card )
            return True
        return False

    def popCard( self ):
        if self.isEmpty():
            return None
        return self.cards.pop()

    def isEmpty( self ):
        return len( self ) <= 0
        
    def drawFromDeck( self, deck, number ):
        i = 0
        while i < number and not deck.isEmpty():
            self.cards.append( deck.popCard() )
            i += 1

    def addCard( self, card ):
        self.cards.append( card )

    def playAnswersWithSubstitutes( self, answers, defeatcard, number ):
        for r in range( 1, len( defeatcard.substitute )+1 ):
            if r >= number: # at least one card must be the original
                break
            if self.cards.count( defeatcard ) < number-r:
                continue
            substitutes = []
            for c in defeatcard.substitute:
                if c in self.cards:
                    substitutes.append( c )
            for comb in combinations( substitutes, r ):
                cardlist = []
                for i in range( number-r ):
                    cardlist.append( defeatcard )
                for card in comb:
                    cardlist.append( card )
                answers.append( Play( cardlist ) )

    # Creates a list of all the possible plays that a player can make based on
    # their hand and the Play that they have to answer to.
    def playAnswers( self, play ):
        answers = [Play( [] )] # Pass
        defeat = play.simplifiedPlay()
        if defeat == None:
            return answers
        if self.cards.count( defeat[0] ) > len( defeat ):
            answers.append( Play( (len( defeat )+1)*[defeat[0]] ) ) # one more than before
        self.playAnswersWithSubstitutes( answers, defeat[0], len(defeat )+1 )
        for p in defeat[0].prey:
            if self.cards.count( p ) >= len( defeat ):
                answers.append( Play( (len( defeat ))*[p] ) ) # predators
            self.playAnswersWithSubstitutes( answers, p, len( defeat ) )
        return answers        

    # Creates a list of all the possible openings.
    def playOpening( self ):
        answers = []
        cardset = []
        for card in self.cards:
            if card not in cardset:
                cardset.append( card )
        for card in cardset:
            if card.ordering <= 0: # This is the chameleon which cannot be played alone
                continue
            for i in range( 1, self.cards.count( card )+1 ):
                answers.append( Play( i*[card] ) )
                substitutes = []
                for c in card.substitute:
                    if c in self.cards:
                        substitutes.append( c )
                for r in range( 1, len( substitutes )+1 ):
                    for comb in combinations( substitutes, r ):
                        cardlist = []
                        for j in range( i ):
                            cardlist.append( card )
                        for c in comb:
                            cardlist.append( c )
                        answers.append( Play( cardlist ) )
        # Theoretically, it can happen that a player must open with only a chameleon
        # in hand, namely when they stupidly played all their non-chameleon cards
        # at once, and then everybody else passed. In that case, and in that case alone,
        # they must pass, and play will continue with the next player.
        if len( answers ) <= 0:
            answers.append( Play( [] ) )
        return answers        
        
class CardList( Hand ):

    def __init__( self, filename="fzdefault.txt" ):
        super().__init__()
        if filename == "" or not isfile( filename ):
            whale = Animal( "whale", 12 )
            elephant = Animal( "elephant", 11 )
            crocodile = Animal( "crocodile", 10 )
            polarbear = Animal( "polar bear", 9 )
            lion = Animal( "lion", 8 )
            seal = Animal( "seal", 7 )
            fox = Animal( "fox", 6 )
            perch = Animal( "perch", 5 )
            hedgehog = Animal( "hedgehog", 4 )
            fish = Animal( "fish", 3 )
            mouse = Animal( "mouse", 2 )
            mosquito = Animal( "mosquito", 1 )
            chameleon = Animal( "chameleon", 0 ) # Use 0 for chameleon, indicating that it cannot be played by itself
            whale.predator = [fish,perch,seal,polarbear]
            whale.substitute = [chameleon]
            elephant.prey = [mouse]
            elephant.predator = [fox,lion,polarbear,crocodile]
            elephant.substitute = [chameleon,mosquito]
            crocodile.prey = [elephant]
            crocodile.predator = [mouse,fish,perch,fox]
            crocodile.substitute = [chameleon]
            polarbear.prey = [elephant,whale]
            polarbear.predator = [mouse,perch,fox,seal]
            polarbear.substitute = [chameleon]
            lion.prey = [elephant]
            lion.predator = [mouse,fox]
            lion.substitute = [chameleon]
            seal.prey = [polarbear,whale]
            seal.predator = [mouse,fish,perch]
            seal.substitute = [chameleon]
            fox.prey = [lion,crocodile,polarbear,elephant]
            fox.predator = [mouse,hedgehog]
            fox.substitute = [chameleon]
            perch.prey = [seal,polarbear,crocodile,whale]
            perch.predator = [fish]
            perch.substitute = [chameleon]
            hedgehog.prey = [fox]
            hedgehog.predator = [mosquito,mouse]
            hedgehog.substitute = [chameleon]
            fish.prey = [perch,seal,crocodile,whale]
            fish.predator = [mosquito]
            fish.substitute = [chameleon]
            mouse.prey = [hedgehog,fox,seal,lion,polarbear,crocodile]
            mouse.predator = [mosquito,elephant]
            mouse.substitute = [chameleon]
            mosquito.prey = [mouse,fish,hedgehog]
            mosquito.transform = [elephant]
            mosquito.substitute = [chameleon]
            mosquito.number = 4
            chameleon.transform = [mosquito,mouse,fish,hedgehog,perch,fox,seal,lion,polarbear,crocodile,elephant,whale]
            chameleon.number = 1
            self.cards = [whale,elephant,crocodile,polarbear,lion,seal,fox,perch,hedgehog,fish,mouse,mosquito,chameleon]
        else:
            zoo = {}
            with open( filename ) as fp:
                buf = fp.readline() # First line is "ANIMAL"
                for line in fp:
                    line = line.strip()
                    if line == "PREDATOR":
                        break
                    name,id,number = line.split(",")
                    id = int(id)
                    number = int(number)
                    animal = Animal(name,id)
                    animal.number = number
                    zoo[id] = animal
                for line in fp: # predators
                    line = line.strip()
                    if line == "SUBSTITUTE":
                        break
                    id,prey = line.split(":")
                    id = int(id)
                    preylist = prey.split(",")
                    for p in preylist:
                        p = int(p)
                        zoo[id].predator.append(zoo[p])
                        zoo[p].prey.append(zoo[id])
                for line in fp: # substitutes
                    line = line.strip()
                    if line == "":
                        break
                    id,sub = line.split(":")
                    id = int(id)
                    sublist = sub.split(",")
                    for p in sublist:
                        p = int(p)
                        zoo[id].substitute.append(zoo[p])
                        zoo[p].transform.append(zoo[id])
            self.cards = list( zoo.values() )
    
        
# This is the Frank's Zoo deck.
# Different decks can be created, with different cards.
class FranksZooDeck( Hand ):

    def __init__( self, cardlist ):
        super().__init__()
        for card in cardlist.cards:
            self.cards.extend( card.number*[card] )
        self.shuffle()


class Play( Hand ):
    
    def __init__( self, cards=[], player=None, opening=False, out=False ):
        super().__init__( cards )
        self.player = player # For history and lastplay, this is the name of the player.
        self.opening = opening
        self.out = out
    
    # This function translates a Hand (which constitutes a group of cards played together)
    # into a simplified representation. E.g., if Hand would be mosquito+elephant, then the
    # simplified version of that is two elephants -- however, this is None if the group
    # offered is not a legal play, e.g., mosquito+perch.
    def simplifiedPlay( self ):
        lead = None
        for card in self.cards: # First check all the cards that cannot transform
            if len( card.transform ) <= 0:
                if lead != None and card != lead:
                    return None
                lead = card
        if lead == None: # Otherwise the lead may be a card that can transform; however, never a chameleon
            for card in self.cards:
                if card.ordering > 0:
                    if lead != None and card != lead:
                        return None
                    lead = card
        if lead == None:
            return None
        # lead card found
        transforms = []
        for card in self.cards: # Now check if all the transform cards can transform into the lead
            if len( card.transform ) > 0:
                if card == lead: # transform card equal to lead (e.g., leading mosquitos), this is fine
                    continue
                if lead in card.transform:
                    if card in transforms: # can have each transform card only once
                        return None
                    transforms.append( card )
                else:
                    return None
        return Play( len( self.cards )*[lead] )
        
    def __repr__( self ):
        s = super().__repr__()
        if self.player != None:
            if isinstance( self.player, str ): # This is a bit of a kludge:
                s = f"{self.player}:{s}"       # To avoid AIs having access directly to player infor
            else:                              # I replace the player object by the player name in
                s = f"{self.player.name}:{s}"  # history and in lastplay
        if self.opening and self.out:
            s += "(open,out)"
        elif self.opening:
            s += "(open)"
        elif self.out:
            s += "(out)"
        return s


if __name__ == "__main__":
    cardlist = CardList()
    deck = FranksZooDeck( cardlist )
    print( deck.cards[0] )
    print( deck )
    hand = Hand()
    hand.drawFromDeck( deck, 5 )
    print( hand )
    hand.sort()
    print( hand )
    play = Play()
    play.drawFromDeck( deck, 2 )
    print( Play( [deck[0]] ).simplifiedPlay() )
    cardlist = CardList()
    deck = FranksZooDeck( cardlist )
    deck.sort()
    print( Play( [deck[35]] ).simplifiedPlay() ) # perch
    print( Play( [deck[35],deck[37]] ).simplifiedPlay() ) # perch, perch
    print( Play( [deck[59],deck[35]] ).simplifiedPlay() ) # chameleon, perch
    print( Play( [deck[35],deck[59]] ).simplifiedPlay() ) # perch, chameleon
    print( Play( [deck[37],deck[59],deck[35]] ).simplifiedPlay() ) # perch, chameleon, perch
    print( Play( [deck[37],deck[58],deck[35]] ).simplifiedPlay() ) # perch, mosquito, perch
    print( Play( [deck[37],deck[59],deck[45],deck[35]] ).simplifiedPlay() ) # perch, chameleon, fish, perch
    print( Play( [deck[5],deck[6]] ).simplifiedPlay() ) # elephant, elephant
    print( Play( [deck[5],deck[6],deck[7]] ).simplifiedPlay() ) # elephant, elephant, elephant
    print( Play( [deck[58],deck[5],deck[6]] ).simplifiedPlay() ) # mosquito, elephant, elephant
    print( Play( [deck[5],deck[58],deck[6]] ).simplifiedPlay() ) # elephant, mosquito, elephant
    print( Play( [deck[5],deck[6],deck[57]] ).simplifiedPlay() ) # elephant, elephant, mosquito
    print( Play( [deck[59],deck[58],deck[5]] ).simplifiedPlay() ) # chameleon, mosquito, elephant
    print( deck.playAnswers( Play( [deck[5]] ) ) )
    print( deck.playAnswers( Play( [deck[5],deck[6]] ) ) )
    print( deck.playAnswers( Play( [deck[42],deck[59]] ) ) )
    hand = Hand( [deck[54],deck[55],deck[49],deck[19],deck[18],deck[6],deck[5],deck[4]] )
    print( hand )
    print( hand.playAnswers( Play( [deck[7]] ) ) )
    print( hand.playAnswers( Play( [deck[7],deck[6]] ) ) )
    print( hand.playAnswers( Play( [deck[44],deck[59]] ) ) )
    print( hand.playAnswers( Play( [deck[49]] ) ) )
    print( hand.playAnswers( Play( [deck[44]] ) ) )
    print( hand.playAnswers( Play( [deck[44],deck[43]] ) ) )
    print( hand.playOpening() )
    hand = Hand( [deck[59],deck[54],deck[55],deck[56],deck[49],deck[19],deck[18],deck[16],deck[5],deck[4]] )
    print( hand.playOpening() )
    i = 0
    while i < len( deck ):
        print( f"{i}. {deck[i]}" )
        i += 1
    cardlist = CardList("fzstratego.txt")
    deck = FranksZooDeck( cardlist )
    i = 0
    while i < len( deck ):
        print( f"{i}. {deck[i]}" )
        i += 1    
    