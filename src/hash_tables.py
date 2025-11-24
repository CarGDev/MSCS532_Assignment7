"""
Hash Tables Module

This module implements various hash table data structures including:
- Direct-address tables
- Open addressing (linear probing, quadratic probing, double hashing)
- Separate chaining
"""

from typing import Any, Optional, Tuple, List, Callable
from .hash_functions import division_hash, get_hash_function


class DirectAddressTable:
    """
    Direct-address table implementation.
    
    Assumes keys are integers in a small range [0, m-1].
    Provides O(1) operations but requires keys to be in a known range.
    """
    
    def __init__(self, size: int):
        """
        Initialize direct-address table.
        
        Args:
            size: Maximum key value (keys must be in range [0, size-1])
        """
        self.size = size
        self.table: List[Optional[Any]] = [None] * size
    
    def insert(self, key: int, value: Any) -> None:
        """
        Insert key-value pair.
        
        Args:
            key: Integer key (must be in range [0, size-1])
            value: Value to store
        """
        if not (0 <= key < self.size):
            raise ValueError(f"Key {key} out of range [0, {self.size-1}]")
        self.table[key] = value
    
    def search(self, key: int) -> Optional[Any]:
        """
        Search for value by key.
        
        Args:
            key: Integer key to search for
            
        Returns:
            Value if found, None otherwise
        """
        if not (0 <= key < self.size):
            return None
        return self.table[key]
    
    def delete(self, key: int) -> None:
        """
        Delete key-value pair.
        
        Args:
            key: Integer key to delete
        """
        if 0 <= key < self.size:
            self.table[key] = None


class HashTableOpenAddressing:
    """
    Hash table using open addressing with multiple probing strategies.
    
    Supports linear probing, quadratic probing, and double hashing.
    """
    
    DELETED = object()  # Sentinel for deleted entries
    
    def __init__(
        self,
        size: int,
        hash_func: Optional[Callable] = None,
        probe_type: str = 'linear',
        load_factor_threshold: float = 0.75
    ):
        """
        Initialize hash table with open addressing.
        
        Args:
            size: Initial size of hash table
            hash_func: Hash function to use (default: division method)
            probe_type: Type of probing ('linear', 'quadratic', 'double')
            load_factor_threshold: Maximum load factor before resizing
        """
        self.size = size
        self.count = 0
        self.table: List[Optional[Tuple[int, Any]]] = [None] * size
        self.hash_func = hash_func or (lambda k, s: division_hash(k, s))
        self.probe_type = probe_type
        self.load_factor_threshold = load_factor_threshold
        self._probe_count = 0
        self._comparison_count = 0
    
    def _load_factor(self) -> float:
        """Calculate current load factor."""
        return self.count / self.size
    
    def _linear_probe(self, key: int, i: int) -> int:
        """Linear probing: h(k,i) = (h'(k) + i) mod m"""
        h1 = self.hash_func(key, self.size)
        return (h1 + i) % self.size
    
    def _quadratic_probe(self, key: int, i: int) -> int:
        """Quadratic probing: h(k,i) = (h'(k) + c1*i + c2*i^2) mod m"""
        h1 = self.hash_func(key, self.size)
        c1, c2 = 1, 1
        return (h1 + c1 * i + c2 * i * i) % self.size
    
    def _double_hash(self, key: int, i: int) -> int:
        """Double hashing: h(k,i) = (h1(k) + i*h2(k)) mod m"""
        h1 = self.hash_func(key, self.size)
        # Second hash function: h2(k) = 1 + (k mod (m-1))
        h2 = 1 + (key % (self.size - 1))
        return (h1 + i * h2) % self.size
    
    def _probe(self, key: int, i: int) -> int:
        """Get probe sequence index based on probe type."""
        if self.probe_type == 'linear':
            return self._linear_probe(key, i)
        elif self.probe_type == 'quadratic':
            return self._quadratic_probe(key, i)
        elif self.probe_type == 'double':
            return self._double_hash(key, i)
        else:
            raise ValueError(f"Unknown probe type: {self.probe_type}")
    
    def _resize(self) -> None:
        """Resize table when load factor exceeds threshold."""
        old_table = self.table
        old_size = self.size
        self.size *= 2
        self.count = 0
        self.table = [None] * self.size
        
        # Rehash all existing entries
        for entry in old_table:
            if entry is not None and entry is not self.DELETED:
                key, value = entry
                self.insert(key, value)
    
    def insert(self, key: int, value: Any) -> None:
        """
        Insert key-value pair using open addressing.
        
        Args:
            key: Key to insert
            value: Value to store
        """
        if self._load_factor() >= self.load_factor_threshold:
            self._resize()
        
        i = 0
        while i < self.size:
            index = self._probe(key, i)
            self._probe_count += 1
            entry = self.table[index]
            
            if entry is None or entry is self.DELETED:
                self.table[index] = (key, value)
                self.count += 1
                return
            elif entry[0] == key:
                self._comparison_count += 1
                # Update existing key
                self.table[index] = (key, value)
                return
            else:
                self._comparison_count += 1
            
            i += 1
        
        raise RuntimeError("Hash table is full")
    
    def search(self, key: int) -> Optional[Any]:
        """
        Search for value by key.
        
        Args:
            key: Key to search for
            
        Returns:
            Value if found, None otherwise
        """
        i = 0
        while i < self.size:
            index = self._probe(key, i)
            self._probe_count += 1
            entry = self.table[index]
            
            if entry is None:
                return None
            elif entry is not self.DELETED and entry[0] == key:
                self._comparison_count += 1
                return entry[1]
            else:
                self._comparison_count += 1
            
            i += 1
        
        return None
    
    def get_probe_count(self) -> int:
        """Get total number of probes performed."""
        return self._probe_count
    
    def get_comparison_count(self) -> int:
        """Get total number of key comparisons performed."""
        return self._comparison_count
    
    def reset_counts(self) -> None:
        """Reset probe and comparison counters."""
        self._probe_count = 0
        self._comparison_count = 0
    
    def delete(self, key: int) -> bool:
        """
        Delete key-value pair.
        
        Args:
            key: Key to delete
            
        Returns:
            True if deleted, False if not found
        """
        i = 0
        while i < self.size:
            index = self._probe(key, i)
            entry = self.table[index]
            
            if entry is None:
                return False
            elif entry is not self.DELETED and entry[0] == key:
                self.table[index] = self.DELETED
                self.count -= 1
                return True
            
            i += 1
        
        return False


class HashTableSeparateChaining:
    """
    Hash table using separate chaining for collision resolution.
    
    Each bucket contains a linked list of key-value pairs.
    """
    
    class Node:
        """Node for linked list in separate chaining."""
        def __init__(self, key: int, value: Any):
            self.key = key
            self.value = value
            self.next: Optional['HashTableSeparateChaining.Node'] = None
    
    def __init__(
        self,
        size: int,
        hash_func: Optional[Callable] = None,
        load_factor_threshold: float = 1.0
    ):
        """
        Initialize hash table with separate chaining.
        
        Args:
            size: Initial size of hash table
            hash_func: Hash function to use (default: division method)
            load_factor_threshold: Maximum load factor before resizing
        """
        self.size = size
        self.count = 0
        self.buckets: List[Optional[self.Node]] = [None] * size
        self.hash_func = hash_func or (lambda k, s: division_hash(k, s))
        self.load_factor_threshold = load_factor_threshold
        self._comparison_count = 0
    
    def _load_factor(self) -> float:
        """Calculate current load factor."""
        return self.count / self.size
    
    def _resize(self) -> None:
        """Resize table when load factor exceeds threshold."""
        old_buckets = self.buckets
        old_size = self.size
        self.size *= 2
        self.count = 0
        self.buckets = [None] * self.size
        
        # Rehash all existing entries
        for head in old_buckets:
            current = head
            while current is not None:
                self.insert(current.key, current.value)
                current = current.next
    
    def insert(self, key: int, value: Any) -> None:
        """
        Insert key-value pair.
        
        Args:
            key: Key to insert
            value: Value to store
        """
        if self._load_factor() >= self.load_factor_threshold:
            self._resize()
        
        index = self.hash_func(key, self.size)
        
        # Check if key already exists
        current = self.buckets[index]
        while current is not None:
            self._comparison_count += 1
            if current.key == key:
                current.value = value  # Update existing key
                return
            current = current.next
        
        # Insert new node at head of chain
        new_node = self.Node(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.count += 1
    
    def search(self, key: int) -> Optional[Any]:
        """
        Search for value by key.
        
        Args:
            key: Key to search for
            
        Returns:
            Value if found, None otherwise
        """
        index = self.hash_func(key, self.size)
        current = self.buckets[index]
        
        while current is not None:
            self._comparison_count += 1
            if current.key == key:
                return current.value
            current = current.next
        
        return None
    
    def get_comparison_count(self) -> int:
        """Get total number of key comparisons performed."""
        return self._comparison_count
    
    def reset_counts(self) -> None:
        """Reset comparison counter."""
        self._comparison_count = 0
    
    def delete(self, key: int) -> bool:
        """
        Delete key-value pair.
        
        Args:
            key: Key to delete
            
        Returns:
            True if deleted, False if not found
        """
        index = self.hash_func(key, self.size)
        current = self.buckets[index]
        
        if current is None:
            return False
        
        # Check if key is at head
        if current.key == key:
            self.buckets[index] = current.next
            self.count -= 1
            return True
        
        # Search in chain
        prev = current
        current = current.next
        while current is not None:
            if current.key == key:
                prev.next = current.next
                self.count -= 1
                return True
            prev = current
            current = current.next
        
        return False
    
    def get_chain_lengths(self) -> List[int]:
        """
        Get lengths of all chains for analysis.
        
        Returns:
            List of chain lengths
        """
        lengths = []
        for head in self.buckets:
            length = 0
            current = head
            while current is not None:
                length += 1
                current = current.next
            lengths.append(length)
        return lengths

