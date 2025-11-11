from FranksZooPlayer import Player
from FranksZooState import State, PlayerState
from random import random, randint, randrange

class RandomPlayer( Player ):
    def __init__( self, cardlist ):
        super().__init__( cardlist, self.__class__.__name__ )
    def play( self, lastplay, possible, state ):
        toplay = possible[randrange(0,len( possible ))]
        #print( self.report( state, toplay, lastplay ) )
        return toplay

class PassABit( Player ):
    def __init__( self, cardlist ):
        super().__init__( cardlist, self.__class__.__name__ )
    def play( self, lastplay, possible, state ):
        if randint( 0, 4 ) == 0:
            toplay = possible[0]
        else:
            toplay = possible[randrange(0,len( possible ))]
        #print( self.report( state, toplay, lastplay ) )
        return toplay

class PassALot( Player ):
    def __init__( self, cardlist ):
        super().__init__( cardlist, self.__class__.__name__ )
    def play( self, lastplay, possible, state ):
        if randint( 0, 1 ) == 0:
            toplay = possible[0]
        else:
            toplay = possible[randrange(0,len( possible ))]
        #print( self.report( state, toplay, lastplay ) )
        return toplay

class PlayLongest( Player ):
    def __init__( self, cardlist ):
        super().__init__( cardlist, self.__class__.__name__ )
    def play( self, lastplay, possible, state ):
        longest = 0
        for i in range( 1, len( possible ) ):
            if len( possible[i].cards ) >= len( possible[longest].cards ):
                longest = i
        toplay = possible[longest]
        #print( self.report( state, toplay, lastplay ) )
        return toplay

class PlayLongestReverse( Player ):
    def __init__( self, cardlist ):
        super().__init__( cardlist, self.__class__.__name__ )
    def play( self, lastplay, possible, state ):
        longest = 0
        for i in range( len( possible )-1, 0, -1 ):
            if len( possible[i].cards ) >= len( possible[longest].cards ):
                longest = i
        toplay = possible[longest]
        #print( self.report( state, toplay, lastplay ) )
        return toplay
