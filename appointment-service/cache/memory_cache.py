# Implements fast in-memory LRU cache (using custom logic). Ideal for frequent local lookups

# Add code(Dictionary + DLL) for implementing LRU Cache here

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.dict = {}  # key -> node
        # Dummy head and tail
        self.head = Node(0, 0)  # Least recently used
        self.tail = Node(0, 0)  # Most recently used
        self.head.next = self.tail
        self.tail.prev = self.head

    # === DLL Helpers ===

    def _add_to_tail(self, node):
        """Add a new node just before tail (most recently used)."""
        prev = self.tail.prev
        prev.next = node
        node.prev = prev
        node.next = self.tail
        self.tail.prev = node

    def _remove_node(self, node):
        """Remove a node from DLL."""
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev

    def _move_to_tail(self, node):
        """Move a node to the tail (MRU position)."""
        self._remove_node(node)
        self._add_to_tail(node)

    # === Core LRU Methods ===

    def get(self, key):
        if key not in self.dict:
            return None  # Cache miss
        node = self.dict[key]
        self._move_to_tail(node)
        return node.value

    def put(self, key, value):
        if key in self.dict:
            node = self.dict[key]
            node.value = value
            self._move_to_tail(node)
        else:
            if len(self.dict) >= self.capacity:
                # Evict LRU node
                lru_node = self.head.next
                self._remove_node(lru_node)
                del self.dict[lru_node.key]
            # Insert new node
            new_node = Node(key, value)
            self.dict[key] = new_node
            self._add_to_tail(new_node)

    def delete(self, key):
        """Remove from cache entirely (e.g., when deleted from DB)."""
        if key in self.dict:
            node = self.dict[key]
            self._remove_node(node)
            del self.dict[key]
