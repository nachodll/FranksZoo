from FranksZooPlayer import Player
from FranksZooState import State, PlayerState
from random import random, randint, randrange
from sys import exit

class SelfPlayer( Player ):
    def __init__( self, cardlist ):
        super().__init__( cardlist, self.__class__.__name__ )
    def play( self, lastplay, possible, state ):
        print( "----------------------------------------" )
        print( "HISTORY:" )
        if len( state.history ) <= 0:
            print( "None", "\n" )
        else:
            print( state.str_history(), "\n" )
        print( "PLAYERS (name, handsize, score):" )
        print( state.str_players(), "\n" )
        print( "HAND:" )
        print( str( self.hand ), "\n" )
        print( "LAST PLAY:" )
        print( str( lastplay ), "\n" )
        print( "POSSIBLE PLAYS:" )
        for i in range( len( possible ) ):
            print( f"{i}. {str( possible[i] )}" )
        print()
        
        while True:
            nr = input( "PLAY (X to exit): " )
            if nr == "X":
                exit()
            try:
                nr = int( nr )
            except:
                print( "Please enter an integer (or X)" )
                continue
            if nr < 0 or nr >= len( possible ):
                print( "Please enter the number of a possible play" )
                continue
            break

        return possible[nr]
