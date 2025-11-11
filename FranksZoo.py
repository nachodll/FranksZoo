# Frank's Zoo main program

import random
import importlib
import sys
from datetime import datetime
from os import listdir
from os.path import isfile
from FranksZooGame import FranksZooDeck, CardList, Hand, Animal, Play
from FranksZooPlayer import Player
from FranksZooState import State

DEFAULTLENGTH = 1
DEFAULTAIS = ["FranksZooSelfPlay"]
#DEFAULTAIS = []
DEFAULTDECK = ""

MAXPLAYERS = 4
DOTDISPLAY = min( max( int( DEFAULTLENGTH / 10 ), 1 ), 1000 )

# A game consists of shuffling and dealing the cards,
# and has methods to play out the game.
class Game():

    def __init__( self, length, players, cardlist ):
        self.length = length
        self.players = players
        self.cardlist = cardlist

    def startGame( self, selectedplayers ):
        for player in self.players:
            player.reset()
        self.deck = FranksZooDeck( self.cardlist )
        for player in selectedplayers:
            player.startGame()
        handsize = int( len( self.deck.cards ) / len( selectedplayers ) )
        for player in selectedplayers:
            for i in range( handsize ):
                player.addCard( self.deck.popCard() )
        if not self.deck.isEmpty():
            print( 'ERROR! Deck should be empty!' )

    def endGame( self, selectedplayers, state ):   
        for player in selectedplayers:
            player.endGame( state )

    def __str__( self ):
        s = ''
        for player in self.players:
            s += str( player ) + '\n'
        return s

    # Plays a complete game
    def playRound( self, selectedplayers, number ):
        state = State( selectedplayers )
        # print state
        lastplay = None # last cards played (not passes)
        curplayer = 0 # index in selectedplayers
        points = len( selectedplayers ) # Points starts at 4 (with 4 players)
        opening = True
        while True:
            opening = (lastplay == None)
            player = selectedplayers[curplayer] # This is a player that should be able to play as they have cards
            if lastplay == None: # This means that it is an opening hand; lastplay is None at the start, and also is set to None if we get back to the player without anyone else playing
                possible = player.hand.playOpening()
                lastplay = None
            else:
                possible = player.hand.playAnswers( lastplay )
            if lastplay != None:
                lastplayer = lastplay.player
                lastplay.player = lastplayer.name # remove player from lastplay so that the play method cannot access it

            start = datetime.now()
        
            play = player.play( lastplay, possible, state ) # Ask the player for a play
       
            end = datetime.now()
            duration = end - start
            player.timeused += duration.total_seconds()

            if lastplay != None:
                lastplay.player = lastplayer
            play.sort() # The play is sorted so that we can be sure it should be in possible
            correct = False
            for possibleplay in possible: # check if there is a play in possible equal to play
                if len( play.cards ) != len( possibleplay.cards ):
                    continue
                for i in range( len( play.cards ) ):
                    if play.cards[i] != possibleplay.cards[i]:
                        break
                else:
                    correct = True
                    break
            if not correct: # if something was played that should not work
                if lastplay == None:
                    print( f"Player {player.name} erroneously played {str(play)} as an opening" )
                else:
                    print( f"Player {player.name} erroneously played {str(play)} in answer to {str(lastplay)}" )
                play = possible[random.randrange(0,len( possible ))]
            if len( play.cards ) > 0: # not a pass, so lastplay changes
                lastplay = play
            play.player = player
            play.opening = opening
            for card in play.cards: # remove the played cards from the player's hand
                player.removeCard( card )
            if len( player.hand ) <= 0:
                play.out = True
            state.update( play, selectedplayers ) # add it to history, and update player info
            if len( player.hand ) <= 0: # the player got rid of all their cards, so gets points. This player should never get a turn again this round
                player.totalscore += points
                points -= 1
            if points <= 1: # only one player is left, they get zero points
                break
            while True: # Look for the next player, who should be someone who has cards
                curplayer = (curplayer+1)%len( selectedplayers )
                if lastplay != None and lastplay.player == selectedplayers[curplayer]: # we get back to the player who played the last card
                    lastplay = None # so they may open again; if they have no cards we automatically go to the next player with cards
                if len( selectedplayers[curplayer].hand ) > 0: # only a player with cards may play
                    break
        # round is over
        # print( state.str_history(), "\n" )
        return state

    def statistics( self ):
        print( "NAME                   GAMES  AVERAGE        SECS   SECS/GAME" )
        players.sort()
        for player in self.players:
            print( f"{player.name:20s} {player.games:7d} {player.score():8.3f} {player.timeused:-11.6f} {player.timeused/player.games:-11.6f}" )

    def run( self ):
        for i in range( self.length ):
            if i % DOTDISPLAY == 0:
                print( '.', end="" )
            selectedplayers = []
            if len( self.players ) < MAXPLAYERS:
                selectedplayers = self.players
            else:
                while len( selectedplayers ) < MAXPLAYERS:
                    p = self.players[random.randrange( len(self.players) )]
                    if p not in selectedplayers:
                        selectedplayers.append( p )
            self.startGame( selectedplayers )
            state = self.playRound( selectedplayers, i+1 )
            for player in selectedplayers:
                player.games += 1
            self.endGame( selectedplayers, state )
        print()

# Loads the competitors from the command line arguments
def getCompetitors(argv):
	competitors = []
	for request in argv:
		if '.' in request:
			filename, classname = request.split('.')
		else:
			filename, classname = request, None
		module = importlib.import_module(filename)
		if classname:
			competitors.append(getattr(module, classname))
		else:
			for b in dir(module):
				if hasattr(module, '__all__') and not b in module.__all__: 
					continue
				if b.startswith('__') or b == 'Player': 
					continue
				cls = getattr(module, b)
				try:
					if issubclass(cls, Player):
						competitors.append(cls)
				except TypeError:
					pass
	return competitors

def importBot( filename, argv ):
    bots = []
    modulename = filename
    if '.' in filename:
        modulename, ext = filename.split( '.' )
        if ext != "py":
            return []
        if filename == argv[0]:
            return []
    module = importlib.import_module( modulename )
    for b in dir( module ):
        if hasattr( module, '__all__' ) and not b in module.__all__: 
            continue
        if b.startswith( '__' ) or b == 'Player': 
            continue
        cls = getattr( module, b )
        try:
            if issubclass( cls, Player ) and cls not in bots:
                bots.append( cls )
        except TypeError:
            pass
    return bots
    
def getBots( argv ):
    bots = []
    files = listdir( '.' )
    for filename in files:
        if not isfile( filename ):
            continue
        botlist = importBot( filename, argv )
        for b in botlist:
            if b not in bots:
                bots.append( b )
    return bots

if __name__ == '__main__':

    print( "FRANK'S ZOO 2.0" )
    length = DEFAULTLENGTH
    cardfile = DEFAULTDECK
    competitors = [] # is a list of the classes that compete

    if len(sys.argv) > 1:
        try:
            length = int(sys.argv[1])
        except:
            print( "Usage: FranksZoo.py [<number of games> [<cardfile> [[<botfiles>]]]" )
            sys.exit(1)

    if len(sys.argv) > 2:
        cardfile = sys.argv[2]
        if not isfile( cardfile ):
            print( "Usage: FranksZoo.py [<number of games> [<cardfile> [[<botfiles>]]]" )
            sys.exit(1)

    if len( sys.argv ) > 3:
        for i, arg in enumerate(sys.argv[2:]):
            if '/' not in arg: 
                continue
            sys.path.append(arg)
            del sys.argv[2+i]
        competitors = getCompetitors(sys.argv[3:])

    if len(competitors) <= 0:
        if len( DEFAULTAIS ) > 0:
            competitors = getCompetitors( DEFAULTAIS )
        else:
            competitors = getBots( sys.argv )

    if cardfile != "":
        cardlist = CardList( cardfile )
    else:
        cardlist = CardList( DEFAULTDECK )
        
    print( "Deck:" )
    for card in cardlist.cards:
        pred = []
        for c in card.predator:
            pred.append( c.name )
        pred = ",".join( pred )
        if pred == "":
            pred = "none"
        sub = []
        for c in card.substitute:
            sub.append( c.name )
        sub = ",".join( sub )
        if sub == "":
            sub = "none"
        print( f"{card.number} x {card.name} ({card.id}), prey:{pred}, subs:{sub}" )

    players = [] # is a list of instances of competing classes
    print( "AIs:" )
    for competitor in competitors:
        print( f"{competitor.__name__}" )
        c = competitor( cardlist )
        players.append( competitor( c ) )

    game = Game( length, players, cardlist )
    # print game
    game.run()
    game.statistics()
