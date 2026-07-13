"""
Card Hand Implementation using Positional List with "Fingers"
--------------------------------------------------------------
Uses a single positional list to store cards grouped by suit,
with four "finger" positions (one per suit) marking the last
card of each suit's block for O(1) operations.
"""

class PositionalList:
    """Doubly linked list implementation of the Positional List ADT."""
    
    class _Node:
        __slots__ = '_element', '_prev', '_next'
        
        def __init__(self, element, prev, next):
            self._element = element
            self._prev = prev
            self._next = next
    
    class Position:
        __slots__ = '_container', '_node'
        
        def __init__(self, container, node):
            self._container = container
            self._node = node
        
        def element(self):
            return self._node._element
        
        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node
        
        def __ne__(self, other):
            return not (self == other)
    
    def _validate(self, p):
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._next is None:
            raise ValueError('p is no longer valid')
        return p._node
    
    def _make_position(self, node):
        if node is self._header or node is self._trailer:
            return None
        return self.Position(self, node)
    
    def __init__(self):
        self._header = self._Node(None, None, None)
        self._trailer = self._Node(None, None, None)
        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._size = 0
    
    def __len__(self):
        return self._size
    
    def is_empty(self):
        return self._size == 0
    
    def first(self):
        return self._make_position(self._header._next)
    
    def last(self):
        return self._make_position(self._trailer._prev)
    
    def before(self, p):
        node = self._validate(p)
        return self._make_position(node._prev)
    
    def after(self, p):
        node = self._validate(p)
        return self._make_position(node._next)
    
    def __iter__(self):
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)
    
    def _insert_between(self, e, predecessor, successor):
        newest = self._Node(e, predecessor, successor)
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return self._make_position(newest)
    
    def add_first(self, e):
        return self._insert_between(e, self._header, self._header._next)
    
    def add_last(self, e):
        return self._insert_between(e, self._trailer._prev, self._trailer)
    
    def add_before(self, p, e):
        original = self._validate(p)
        return self._insert_between(e, original._prev, original)
    
    def add_after(self, p, e):
        original = self._validate(p)
        return self._insert_between(e, original, original._next)
    
    def delete(self, p):
        node = self._validate(p)
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element
        node._prev = node._next = node._element = None
        return element
    
    def replace(self, p, e):
        node = self._validate(p)
        old_value = node._element
        node._element = e
        return old_value


class Card:
    """Represents a playing card with rank and suit."""
    
    __slots__ = 'rank', 'suit'
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def __repr__(self):
        return f'{self.rank}{self.suit}'
    
    def __str__(self):
        return f'{self.rank}{self.suit}'


class CardHand:
    """
    Represents a hand of cards using a single positional list.
    
    Cards are grouped by suit within the list. Four "finger" positions
    track the last card of each suit's block, enabling O(1) insertion
    and removal of cards by suit.
    
    Layout Example:
    [H-A, H-K, H-3, C-Q, S-2, D-J, D-5]
          ↑finger_H     ↑finger_C ↑finger_S       ↑finger_D
    
    Operations:
    - add_card(r, s): O(1) - Insert card at end of its suit block
    - play(s): O(1) - Remove last card of specified suit
    - __iter__(): O(n) - Forward iteration through all cards
    - all_of_suit(s): O(k) - Iterate through k cards of suit s
    """
    
    SUITS = ('H', 'C', 'S', 'D')  # Hearts, Clubs, Spades, Diamonds
    
    def __init__(self):
        """Initialize empty hand with four finger positions."""
        self._hand = PositionalList()
        # Each finger points to the LAST card of its suit
        self._finger = {suit: None for suit in self.SUITS}
    
    def add_card(self, r, s):
        """
        Add a new card with rank r and suit s to the hand. O(1)
        
        Args:
            r: Card rank (e.g., 'A', 'K', '2')
            s: Card suit ('H', 'C', 'S', 'D')
        
        Raises:
            ValueError: If suit is invalid
        """
        if s not in self._finger:
            raise ValueError(f'Invalid suit: {s}')
        
        card = Card(r, s)
        finger = self._finger[s]
        
        if finger is None:
            # First card of this suit - append to end of hand
            new_position = self._hand.add_last(card)
        else:
            # Insert after the last card of this suit
            new_position = self._hand.add_after(finger, card)
        
        # Update finger to point to the new last card of this suit
        self._finger[s] = new_position
    
    def play(self, s):
        """
        Remove and return a card of suit s from the hand. O(1)
        
        If no card of suit s exists, remove and return an arbitrary card.
        
        Args:
            s: Suit to play ('H', 'C', 'S', 'D')
        
        Returns:
            Card object if hand is not empty, None otherwise
        """
        # Try to play a card of the requested suit
        finger = self._finger.get(s)
        
        if finger is not None:
            return self._remove_card_at_finger(s, finger)
        
        # No card of requested suit - play arbitrary card
        for suit, finger_pos in self._finger.items():
            if finger_pos is not None:
                return self._remove_card_at_finger(suit, finger_pos)
        
        return None  # Hand is empty
    
    def _remove_card_at_finger(self, suit, finger_pos):
        """
        Helper: Remove the card at a finger position. O(1)
        
        Args:
            suit: The suit of the finger
            finger_pos: Position of the finger
        
        Returns:
            The removed card
        """
        card = finger_pos.element()
        before_pos = self._hand.before(finger_pos)
        
        # Update finger for this suit
        if before_pos is not None and before_pos.element().suit == suit:
            # There are more cards of this suit
            self._finger[suit] = before_pos
        else:
            # This was the only card of this suit
            self._finger[suit] = None
        
        # Remove the card from the hand
        self._hand.delete(finger_pos)
        return card
    
    def __iter__(self):
        """Iterate through all cards currently in the hand."""
        for card in self._hand:
            yield card
    
    def all_of_suit(self, s):
        """
        Iterate through all cards of suit s currently in the hand.
        
        Args:
            s: Suit to iterate ('H', 'C', 'S', 'D')
        
        Yields:
            Card objects of the specified suit in order
        """
        finger = self._finger.get(s)
        if finger is None:
            return
        
        # Collect cards by walking backward from finger
        cards = []
        current = finger
        while current is not None and current.element().suit == s:
            cards.append(current.element())
            current = self._hand.before(current)
        
        # Yield in forward order
        for card in reversed(cards):
            yield card
    
    def __len__(self):
        """Return the number of cards in the hand."""
        return len(self._hand)
    
    def __str__(self):
        """Return string representation of the hand."""
        return '[' + ', '.join(str(card) for card in self._hand) + ']'
    
    def display_structure(self):
        """
        Display the internal structure showing suit blocks and fingers.
        Useful for debugging.
        """
        print(f"Hand: {self}")
        for suit in self.SUITS:
            finger = self._finger[suit]
            if finger is not None:
                print(f"  finger_{suit} -> {finger.element()}")
            else:
                print(f"  finger_{suit} -> None")


# Demonstration
if __name__ == "__main__":
    print("CardHand Demo")
    print("=" * 50)
    
    hand = CardHand()
    
    # Add some cards
    print("\nAdding cards to hand:")
    hand.add_card('A', 'H')  # Ace of Hearts
    hand.add_card('K', 'H')  # King of Hearts
    hand.add_card('Q', 'C')  # Queen of Clubs
    hand.add_card('2', 'S')  # 2 of Spades
    hand.add_card('3', 'H')  # 3 of Hearts
    hand.add_card('J', 'D')  # Jack of Diamonds
    
    print(f"Complete hand: {hand}")
    hand.display_structure()
    
    # Iterate through all hearts
    print(f"\nAll hearts: {list(hand.all_of_suit('H'))}")
    
    # Play cards
    print("\nPlaying cards:")
    card1 = hand.play('C')  # Play a club
    print(f"Played: {card1}")
    print(f"Hand now: {hand}")
    
    card2 = hand.play('H')  # Play a heart
    print(f"Played: {card2}")
    print(f"Hand now: {hand}")
    
    card3 = hand.play('C')  # No clubs left, will play arbitrary card
    print(f"Played (no clubs): {card3}")
    print(f"Hand now: {hand}")
    
    # Test iteration
    print("\nIterating through remaining cards:")
    for card in hand:
        print(f"  {card}")
    
    # Test all_of_suit with empty suit
    print(f"\nAll spades: {list(hand.all_of_suit('S'))}")