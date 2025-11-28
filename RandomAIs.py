from FranksZooPlayer import Player
from FranksZooState import State, PlayerState
from random import random, randint, randrange

class RandomPlayer1( Player ):
    def __init__( self, cardlist ):
        super().__init__( cardlist, self.__class__.__name__ )
    def play( self, lastplay, possible, state ):
        toplay = possible[randrange(0,len( possible ))]
        #print( self.report( state, toplay, lastplay ) )
        return toplay
    
class RandomPlayer2( Player ):
    def __init__( self, cardlist ):
        super().__init__( cardlist, self.__class__.__name__ )
    def play( self, lastplay, possible, state ):
        toplay = possible[randrange(0,len( possible ))]
        #print( self.report( state, toplay, lastplay ) )
        return toplay
    
class RandomPlayer3( Player ):
    def __init__( self, cardlist ):
        super().__init__( cardlist, self.__class__.__name__ )
    def play( self, lastplay, possible, state ):
        toplay = possible[randrange(0,len( possible ))]
        #print( self.report( state, toplay, lastplay ) )
        return toplay
    
class RandomPlayer4( Player ):
    def __init__( self, cardlist ):
        super().__init__( cardlist, self.__class__.__name__ )
    def play( self, lastplay, possible, state ):
        toplay = possible[randrange(0,len( possible ))]
        #print( self.report( state, toplay, lastplay ) )
        return toplay