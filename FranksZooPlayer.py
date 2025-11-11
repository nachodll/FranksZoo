from random import randrange
from FranksZooGame import Animal, Hand

class Player():

    def __init__( self, cardlist=None, name="" ):
        self.name = name
        self.hand = Hand()
        self.games = 0
        self.totalscore = 0
        self.timeused = 0
        self.id = 0
        self.cardlist = cardlist # This is of the type Hand, which contains a list cards,
        # whereby the items are of the type Animal; each of these items is one type of 
        # card in the game.

    def __str__( self ):
        return f'[{self.name},{self.hand}]'

    def __eq__( self, other ):
        if other == None:
            return False
        return self.name == other.name and self.id == other.id

    def __lt__( self, other ):
        return self.score() > other.score() or \
            (self.score() == other.score() and self.name < other.name ) or \
            (self.score() == other.score() and self.name == other.name and self.id < other.id)
            
    def __ge__( self, other ):
        return not self < other

    def __le__( self, other ):
        return self == other or self < other

    def __gt__( self, other ):
        return not self <= other

    def score( self ):
        if self.games <= 0:
            return 0.0
        return float( self.totalscore ) / float( self.games )

    def setName( self, name ):
        self.name = name

    def addCard( self, card ):
        self.hand.addCard( card )
        self.hand.sort()

    def removeCard( self, card ):
        return self.hand.removeCard( card )

    def reset( self ):
        self.hand = Hand()
        self.lastplay = None

    # lastplay contains a Play object that represent the last combination that was played.
    # If this is an opening play, then lastplay is None.
    # possible is a list of Play objects which are all combinations that can now be played from
    # the player's hand. The first of these is a "pass", represented by Play([]), unless
    # this is an opening play, in which case "pass" is not allowed. The only possible way to
    # pass when opening is when the player only holds the chameleon card. The first card in
    # the Play objects in the possible list is always the "lead" card, i.e., possible substitutes
    # follow later. E.g., if a Play object contains an elephant and a mosquito, the elephant will
    # be first. 
    # state is an overview of all players, in the order that they play, with their handsizes.
    # state also contains a list of all the cards that have been played (as a Hand object).
    # You must return a Play object which consists of cards from your hand. It is not necessary that
    # the ordering of the cards in the Play object is the same as for that particular play in 
    # the possible list. 
    def play( self, lastplay, possible, state ):
        return possible[randrange(0,len( possible ))]

    def startGame( self ):
        pass

    def endGame( self, state ):
        pass

    def report( self, state, toplay, lastplay=None ):
        cardlist = []
        for c in self.hand.cards:
            cardlist.append( str( c ) )
        rep = ",".join( cardlist )
        rep = f"{self.name}; hand: " + rep
        rep += f"; play: {str(toplay)}"
        if lastplay != None:
            rep += f"; lastplay: {str( lastplay )}"
        rep += f"; state: {state}"
        return rep
        
        