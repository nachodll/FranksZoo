from collections import Counter
from random import randrange
from FranksZooGame import Hand, Play
from FranksZooPlayer import Player


class NachoAI(Player):
    def __init__(self, cardlist):
        # here we can analyze the deck
        super().__init__(cardlist, self.__class__.__name__)
        # TODO: adjust weights based on deck analysis
        self.base_weights = {
            11: 2,   # elephant
            12: 8,   # whale
            9: 14,   # polar bear
            10: 18,  # crocodile
            7: 30,   # seal
            6: 40,   # fox
            2: 46,   # mouse
            8: 48,   # lion
            4: 62,   # hedgehog
            5: 70,   # perch
            1: 76,   # mosquito
            3: 84,   # fish
            0: 0,    # chameleon (joker)
        }

    def play(self, lastplay, possible, state):
        # Step 0: only one possible play
        if len(possible) == 1:
            return possible[0]

        # Step 1: play winning move if available
        for play in possible:
            if self._is_winning_move(play, self.hand):
                return play

        # Step 2: remove losing moves
        filtered = [p for p in possible if not self._is_losing_move(p, self.hand)]
        if len(filtered) == 0:
            filtered = possible
        

        # Step 3: check winning sequences
        opponent_counts = self._opponent_card_counts(state) # total count of cards opponents may have
        for play in filtered:
            if len(play.cards) == 0:
                continue
            if self._starts_winning_sequence(self.hand, play, opponent_counts):
                return play

        # Step 4: move weights
        played_cards = sum(len(play.cards) for play in state.history)
        num_players = len(state.players)
        lower = 15 - (played_cards * num_players) / 10
        upper = 30 - (played_cards * num_players) / 5

        candidates = []
        preferred = None
        best_weight = float("-inf")
        for play in filtered:
            weight = self._move_weight(play)
            if weight < lower:
                continue
            candidates.append(play)
            if weight > upper and weight > best_weight:
                preferred = play
                best_weight = weight

        if preferred:
            return preferred
        if len(candidates) > 0:
            return candidates[randrange(0, len(candidates))]
        return possible[0]

    def _opponent_card_counts(self, state):
        # 1. Initial counts based on full deck
        counts = {card: card.number for card in self.cardlist.cards}
        # 2. Substract cards in own hand
        for card in self.hand.cards:
            counts[card] -= 1
        # 3. Substract cards played
        for hist_play in state.history:
            for card in hist_play.cards:
                counts[card] -= 1
        return counts

    def _is_winning_move(self, play, hand):
        # Check if play uses all cards in hand
        return len(play.cards) > 0 and len(play.cards) == len(hand.cards)

    def _is_losing_move(self, play, hand):
        # TODO: generalize. So far it assumes only one chameleon per deck and id 0
        has_chameleon = any(card.id == 0 for card in hand.cards)
        if not has_chameleon or len(play.cards) <= 0:
            return False
        plays_chameleon = any(card.id == 0 for card in play.cards)
        if plays_chameleon:
            return False
        # If there is a chameleon in hand and it is not played, and all other cards are played
        return len(play.cards) == len(hand.cards) - 1

    def _starts_winning_sequence(self, hand, play, opponent_counts):
        # TODO: memoization to avoid recomputing for same hand states
        # A winning sequence is either a winning move ...
        if self._is_winning_move(play, hand):
            return True
        # ... or an undefeatable move that leads to a winning sequence
        if not self._is_undefeatable(play, opponent_counts):
            return False
        next_hand = self._hand_after_play(hand, play)
        # Check if possible openings after our undeafeatable play lead to winning sequences
        for opening in next_hand.playOpening():
            if len(opening.cards) == 0:
                continue
            if self._starts_winning_sequence(next_hand, opening, opponent_counts):
                return True
        return False

    def _hand_after_play(self, hand, play):
        # Return a new Hand object with cards remaining after play
        remaining = list(hand.cards)
        for card in play.cards:
            if card in remaining:
                remaining.remove(card)
        return Hand(remaining)

    def _is_undefeatable(self, play, opponent_counts):
        simplified = play.simplifiedPlay()
        if simplified is None or len(simplified.cards) == 0:
            return False
        animal = simplified.cards[0]
        needed = len(simplified.cards)
        # Check if opponents could defeat this play with the same animal + 1 
        if self._available_for_opponents(animal, needed + 1, opponent_counts):
            return False
        # Check if opponents could defeat this play with any predator
        for predator in animal.predator:
            if self._available_for_opponents(predator, needed, opponent_counts):
                return False
        return True

    def _available_for_opponents(self, card, needed, counts):
        # Check if opponents could potentially have enough of 'card' (including substitutes)
        base = counts.get(card, 0)
        subs = sum(counts.get(sub, 0) for sub in card.substitute)
        if base <= 0:
            return False
        return base + subs >= needed

    def _move_weight(self, play):
        simplified = play.simplifiedPlay()
        if simplified is None or len(simplified.cards) == 0:
            return 0
        animal = simplified.cards[0]
        base = self.base_weights.get(animal.id, 0)
        # Check if play contains all copies of the animal in hand
        animal_in_play = play.cards.count(animal)
        animal_in_hand = self.hand.cards.count(animal)
        if animal_in_play < len(play.cards) or (animal_in_hand - animal_in_play) > 0:
            base = base / 4.0 # this number is emperically chosen
        return base
