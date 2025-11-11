from FranksZooGame import Hand
from FranksZooPlayer import Player
from FranksZooGame import Play

class PlayerState():
    def __init__( self, name, score=0, handsize=0 ):
        self.name = name
        self.score = score
        self.handsize = handsize
    def __str__( self ):
        s = f"{self.name},{self.handsize},{self.score:.3f}"
        return s

class State():
    def __init__( self, players ):
        self.history = []
        self.update( None, players )

    def update( self, curplay, players ):
        if curplay != None:
            histplay = Play( curplay.cards, curplay.player.name, curplay.opening, curplay.out )
            self.history.append( histplay )
        self.players = []
        #if curplay != None and len( curplay ) <= 0:
        #    return
        for player in players:
            name = player.name
            score = player.score()
            handsize = len( player.hand )
            self.players.append( PlayerState( name, score, handsize ) )
            
    def str_history( self ):
        s = []
        for h in self.history:
            s.append( str( h ) )
        return "\n".join( s )
        
    def str_players( self ):
        s = []
        for p in self.players:
            s.append( str( p ) )
        return "\n".join( s )
        
    def __str__( self ):
        s = []
        for player in self.players:
            s.append( str( player ) )
        return "-".join( s )
