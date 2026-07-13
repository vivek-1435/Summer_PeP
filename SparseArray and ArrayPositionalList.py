"""
Sparse Array and Array-based Positional List ADT
-------------------------------------------------
P-1: SparseArray implementation using a list for efficient storage
P-2: Array-based implementation of Positional List ADT
"""

# =========================== P-1: SparseArray ===========================

class SparseArray:
    """
    Efficient representation of a sparse array using O(m) storage,
    where m is the number of nonempty entries.
    
    Uses a dictionary (hash table) to store only non-None entries,
    providing O(1) average time for get and set operations.
    
    Time Complexity Analysis:
    - __getitem__: O(1) average - dictionary lookup
    - __setitem__: O(1) average - dictionary insertion/deletion
    - Space: O(m) where m is number of non-None entries
    """
    
    def __init__(self, length):
        """
        Initialize sparse array of given length.
        
        Args:
            length: The logical length of the array
        """
        self._length = length
        self._data = {}  # Dictionary mapping index to non-None values
    
    def __len__(self):
        """Return the logical length of the array."""
        return self._length
    
    def __getitem__(self, j):
        """
        Return the element at index j, or None if empty.
        
        Time Complexity: O(1) average
        
        Args:
            j: Index to access (0-based)
        
        Returns:
            The element at index j, or None
        
        Raises:
            IndexError: If index is out of bounds
        """
        if not (0 <= j < self._length):
            raise IndexError(f'Index {j} out of range [0, {self._length-1}]')
        return self._data.get(j, None)
    
    def __setitem__(self, j, e):
        """
        Set the element at index j to e.
        
        Time Complexity: O(1) average
        
        Args:
            j: Index to set (0-based)
            e: Element to store, or None to clear the cell
        
        Raises:
            IndexError: If index is out of bounds
        """
        if not (0 <= j < self._length):
            raise IndexError(f'Index {j} out of range [0, {self._length-1}]')
        
        if e is None:
            # Remove from dictionary to maintain sparsity
            self._data.pop(j, None)
        else:
            self._data[j] = e
    
    def fill(self, sequence):
        """
        Fill the sparse array from a sequence.
        
        Args:
            sequence: Sequence of values to fill with
        
        Raises:
            ValueError: If sequence length doesn't match array length
        """
        if len(sequence) != self._length:
            raise ValueError('Sequence length must match array length')
        
        self._data.clear()
        for j, value in enumerate(sequence):
            if value is not None:
                self._data[j] = value
    
    def nonempty_count(self):
        """Return the number of nonempty (non-None) entries."""
        return len(self._data)
    
    def __iter__(self):
        """Iterate through (index, element) pairs for nonempty entries."""
        for j in sorted(self._data.keys()):
            yield j, self._data[j]
    
    def __str__(self):
        """Return string representation showing all entries."""
        elements = []
        for j in range(self._length):
            elements.append(str(self._data.get(j, 'None')))
        return '[' + ', '.join(elements) + ']'


# =========================== P-2: ArrayPositionalList ===========================

class ArrayPositionalList:
    """
    Array-based implementation of the Positional List ADT using composition.
    
    Stores items in a dynamic array where each item tracks its current index.
    When elements are shifted due to insertions/deletions, the tracked indices
    are updated to maintain position validity.
    
    Efficiency Analysis:
    - len(), is_empty(): O(1)
    - first(), last(): O(1)
    - before(p), after(p): O(1) - uses stored index
    - add_last(e): O(1)* amortized (like Python list append)
    - add_first(e): O(n) - requires shifting all elements
    - add_before(p, e), add_after(p, e): O(n) - requires shifting
    - delete(p): O(n) - requires shifting to fill gap
    - replace(p, e): O(1)
    
    *Amortized due to occasional array resizing
    """
    
    class _Item:
        """Stores an element and its current index in the array."""
        __slots__ = '_element', '_index'
        
        def __init__(self, element, index):
            self._element = element
            self._index = index
    
    class Position:
        """Position abstraction wrapping an _Item."""
        __slots__ = '_container', '_item'
        
        def __init__(self, container, item):
            self._container = container
            self._item = item
        
        def element(self):
            return self._item._element
        
        def __eq__(self, other):
            return type(other) is type(self) and other._item is self._item
        
        def __ne__(self, other):
            return not (self == other)
    
    def _validate(self, p):
        """Validate and return the position's item."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._item._index == -1:  # Convention for deprecated items
            raise ValueError('p is no longer valid')
        return p._item
    
    def _make_position(self, item):
        """Create a Position from an item, or None."""
        if item is None:
            return None
        return self.Position(self, item)
    
    def __init__(self):
        """Initialize empty positional list."""
        self._data = []  # List of _Item objects in sequence order
    
    def __len__(self):
        """Return number of elements in the list."""
        return len(self._data)
    
    def is_empty(self):
        """Return True if list is empty."""
        return len(self._data) == 0
    
    def first(self):
        """Return the first position, or None if empty."""
        if self.is_empty():
            return None
        return self._make_position(self._data[0])
    
    def last(self):
        """Return the last position, or None if empty."""
        if self.is_empty():
            return None
        return self._make_position(self._data[-1])
    
    def before(self, p):
        """Return the position before p, or None if p is first."""
        item = self._validate(p)
        idx = item._index
        if idx > 0:
            return self._make_position(self._data[idx - 1])
        return None
    
    def after(self, p):
        """Return the position after p, or None if p is last."""
        item = self._validate(p)
        idx = item._index
        if idx < len(self._data) - 1:
            return self._make_position(self._data[idx + 1])
        return None
    
    def __iter__(self):
        """Generate a forward iteration of elements."""
        for item in self._data:
            yield item._element
    
    def _reindex(self, start=0):
        """Update stored indices for items from start to end."""
        for i in range(start, len(self._data)):
            self._data[i]._index = i
    
    def _insert_at(self, index, e):
        """
        Insert element at specified index.
        
        Time Complexity: O(n) due to shifting elements
        
        Args:
            index: Position to insert at
            e: Element to insert
        
        Returns:
            Position of the new element
        """
        item = self._Item(e, index)
        self._data.insert(index, item)
        self._reindex(index)  # Update indices of shifted items
        return self._make_position(item)
    
    def add_first(self, e):
        """Insert element at the front. O(n)"""
        return self._insert_at(0, e)
    
    def add_last(self, e):
        """Insert element at the end. O(1) amortized"""
        return self._insert_at(len(self._data), e)
    
    def add_before(self, p, e):
        """Insert element before position p. O(n)"""
        item = self._validate(p)
        return self._insert_at(item._index, e)
    
    def add_after(self, p, e):
        """Insert element after position p. O(n)"""
        item = self._validate(p)
        return self._insert_at(item._index + 1, e)
    
    def delete(self, p):
        """
        Remove and return element at position p. O(n)
        
        Args:
            p: Position to delete
        
        Returns:
            The element that was removed
        """
        item = self._validate(p)
        idx = item._index
        
        # Remove item and shift subsequent items
        del self._data[idx]
        self._reindex(idx)  # Update indices of shifted items
        
        element = item._element
        
        # Deprecate the item
        item._index = -1
        item._element = None
        
        return element
    
    def replace(self, p, e):
        """
        Replace element at position p with e. O(1)
        
        Args:
            p: Position to replace
            e: New element
        
        Returns:
            The old element
        """
        item = self._validate(p)
        old = item._element
        item._element = e
        return old


# Demonstration
if __name__ == "__main__":
    print("SparseArray and ArrayPositionalList Demo")
    print("=" * 50)
    
    # Test SparseArray
    print("\n1. SparseArray Demo:")
    arr = SparseArray(10)
    arr[2] = 'A'
    arr[5] = 'B'
    arr[9] = 'C'
    
    print(f"Array: {arr}")
    print(f"arr[2] = {arr[2]}")
    print(f"arr[5] = {arr[5]}")
    print(f"arr[7] = {arr[7]}")  # Should be None
    print(f"Nonempty entries: {arr.nonempty_count()}")
    
    arr[2] = None  # Clear an entry
    print(f"After clearing arr[2]: {arr}")
    print(f"Nonempty entries: {arr.nonempty_count()}")
    
    # Test ArrayPositionalList
    print("\n2. ArrayPositionalList Demo:")
    apl = ArrayPositionalList()
    
    p1 = apl.add_last(10)
    p2 = apl.add_last(20)
    p3 = apl.add_after(p1, 15)
    
    print(f"List: {list(apl)}")  # [10, 15, 20]
    
    print(f"First element: {apl.first().element()}")
    print(f"Last element: {apl.last().element()}")
    print(f"Element after p1: {apl.after(p1).element()}")
    
    apl.delete(p2)
    print(f"After deleting 20: {list(apl)}")  # [10, 15]
    
    apl.replace(p1, 100)
    print(f"After replacing 10 with 100: {list(apl)}")  # [100, 15]