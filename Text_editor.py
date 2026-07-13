"""
Text Editor using Positional List ADT
--------------------------------------
A simple text editor that stores a string using a doubly linked positional list
with a cursor that highlights a position in the string.
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


class TextEditor:
    """
    A simple text editor with cursor-based navigation.
    
    The cursor points to a character, and operations occur relative to it:
    - left/right: Move cursor position
    - insert: Insert character just after cursor
    - delete: Delete character just after cursor
    
    Special case: cursor = None means cursor is before the first character.
    """
    
    def __init__(self, text=""):
        """Initialize editor with optional initial text."""
        self._list = PositionalList()
        self._cursor = None  # None means before first character
        
        # Add initial text character by character
        for ch in text:
            self._list.add_last(ch)
        
        # Set cursor to first character if text exists
        if len(self._list) > 0:
            self._cursor = self._list.first()
    
    def left(self):
        """Move cursor left one character (do nothing if at beginning)."""
        if self._cursor is None:
            return  # Already at beginning
        prev = self._list.before(self._cursor)
        if prev is not None:
            self._cursor = prev
        else:
            self._cursor = None  # Move to before first character
    
    def right(self):
        """Move cursor right one character (do nothing if at end)."""
        if self._cursor is None:
            # Before first character, move to first if exists
            if len(self._list) > 0:
                self._cursor = self._list.first()
            return
        
        next_pos = self._list.after(self._cursor)
        if next_pos is not None:
            self._cursor = next_pos
        # If at last character, do nothing
    
    def insert(self, c):
        """Insert character c just after the cursor."""
        if self._cursor is None:
            # Insert at beginning
            if len(self._list) == 0:
                self._cursor = self._list.add_first(c)
            else:
                self._cursor = self._list.add_before(self._list.first(), c)
        else:
            self._cursor = self._list.add_after(self._cursor, c)
    
    def delete(self):
        """Delete the character just after the cursor (do nothing if at end)."""
        if self._cursor is None:
            # Delete first character if exists
            if len(self._list) > 0:
                self._list.delete(self._list.first())
            return
        
        next_pos = self._list.after(self._cursor)
        if next_pos is not None:
            self._list.delete(next_pos)
        # If cursor at last character, nothing to delete after it
    
    def __str__(self):
        """Return string representation with cursor indicator."""
        chars = list(self._list)
        text = ''.join(chars)
        
        if len(chars) == 0:
            return "^\n"  # Empty string with cursor at beginning
        
        # Build cursor indicator line
        cursor_line = [' '] * len(chars)
        
        if self._cursor is not None:
            # Find index of cursor position
            idx = 0
            current = self._list.first()
            while current is not None and current != self._cursor:
                idx += 1
                current = self._list.after(current)
            if 0 <= idx < len(cursor_line):
                cursor_line[idx] = '^'
        else:
            # Cursor before first character
            cursor_line[0] = '^'
        
        return text + '\n' + ''.join(cursor_line)


# Demonstration
if __name__ == "__main__":
    print("Text Editor Demo")
    print("=" * 50)
    
    # Test 1: Basic operations
    editor = TextEditor("HELLO")
    print("Initial state:")
    print(editor)
    print()
    
    editor.right()
    editor.right()
    print("After moving right twice:")
    print(editor)
    print()
    
    editor.insert('X')
    print("After inserting 'X':")
    print(editor)
    print()
    
    editor.delete()
    print("After deleting:")
    print(editor)
    print()
    
    # Test 2: Edge cases
    print("\nTesting edge cases:")
    editor2 = TextEditor("")
    print("Empty editor:")
    print(editor2)
    editor2.insert('A')
    print("After inserting 'A' in empty editor:")
    print(editor2)