"""
Tests for hash table implementations.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.hash_tables import (
    DirectAddressTable,
    HashTableOpenAddressing,
    HashTableSeparateChaining
)
from src.hash_functions import division_hash


class TestDirectAddressTable:
    """Tests for direct-address table."""
    
    def test_insert_and_search(self):
        """Test basic insert and search operations."""
        table = DirectAddressTable(100)
        table.insert(5, "value1")
        table.insert(42, "value2")
        
        assert table.search(5) == "value1"
        assert table.search(42) == "value2"
        assert table.search(10) is None
    
    def test_delete(self):
        """Test delete operation."""
        table = DirectAddressTable(100)
        table.insert(5, "value1")
        table.delete(5)
        assert table.search(5) is None
    
    def test_out_of_range_key(self):
        """Test handling of out-of-range keys."""
        table = DirectAddressTable(100)
        with pytest.raises(ValueError):
            table.insert(100, "value")  # Out of range
        assert table.search(100) is None


class TestHashTableOpenAddressing:
    """Tests for open addressing hash table."""
    
    def test_insert_and_search_linear(self):
        """Test insert and search with linear probing."""
        ht = HashTableOpenAddressing(10, probe_type='linear')
        ht.insert(10, "value1")
        ht.insert(22, "value2")
        ht.insert(31, "value3")
        
        assert ht.search(10) == "value1"
        assert ht.search(22) == "value2"
        assert ht.search(31) == "value3"
        assert ht.search(99) is None
    
    def test_insert_and_search_quadratic(self):
        """Test insert and search with quadratic probing."""
        ht = HashTableOpenAddressing(10, probe_type='quadratic')
        ht.insert(10, "value1")
        ht.insert(22, "value2")
        
        assert ht.search(10) == "value1"
        assert ht.search(22) == "value2"
    
    def test_insert_and_search_double(self):
        """Test insert and search with double hashing."""
        ht = HashTableOpenAddressing(10, probe_type='double')
        ht.insert(10, "value1")
        ht.insert(22, "value2")
        
        assert ht.search(10) == "value1"
        assert ht.search(22) == "value2"
    
    def test_delete(self):
        """Test delete operation."""
        ht = HashTableOpenAddressing(10, probe_type='linear')
        ht.insert(10, "value1")
        ht.insert(22, "value2")
        
        assert ht.delete(10) is True
        assert ht.search(10) is None
        assert ht.search(22) == "value2"
        assert ht.delete(99) is False
    
    def test_update_existing_key(self):
        """Test updating an existing key."""
        ht = HashTableOpenAddressing(10, probe_type='linear')
        ht.insert(10, "value1")
        ht.insert(10, "value2")  # Update
        assert ht.search(10) == "value2"
    
    def test_resize(self):
        """Test automatic resizing."""
        ht = HashTableOpenAddressing(5, probe_type='linear', load_factor_threshold=0.7)
        # Insert enough to trigger resize
        for i in range(10):
            ht.insert(i, f"value{i}")
        
        # All should still be searchable
        for i in range(10):
            assert ht.search(i) == f"value{i}"


class TestHashTableSeparateChaining:
    """Tests for separate chaining hash table."""
    
    def test_insert_and_search(self):
        """Test basic insert and search operations."""
        ht = HashTableSeparateChaining(10)
        ht.insert(10, "value1")
        ht.insert(22, "value2")
        ht.insert(31, "value3")
        
        assert ht.search(10) == "value1"
        assert ht.search(22) == "value2"
        assert ht.search(31) == "value3"
        assert ht.search(99) is None
    
    def test_delete(self):
        """Test delete operation."""
        ht = HashTableSeparateChaining(10)
        ht.insert(10, "value1")
        ht.insert(22, "value2")
        
        assert ht.delete(10) is True
        assert ht.search(10) is None
        assert ht.search(22) == "value2"
        assert ht.delete(99) is False
    
    def test_update_existing_key(self):
        """Test updating an existing key."""
        ht = HashTableSeparateChaining(10)
        ht.insert(10, "value1")
        ht.insert(10, "value2")  # Update
        assert ht.search(10) == "value2"
    
    def test_collision_handling(self):
        """Test that collisions are handled correctly."""
        ht = HashTableSeparateChaining(5)  # Small table to force collisions
        keys = [10, 15, 20, 25, 30]
        for key in keys:
            ht.insert(key, f"value{key}")
        
        # All should be searchable
        for key in keys:
            assert ht.search(key) == f"value{key}"
    
    def test_chain_lengths(self):
        """Test chain length reporting."""
        ht = HashTableSeparateChaining(5)
        for i in range(10):
            ht.insert(i, f"value{i}")
        
        chain_lengths = ht.get_chain_lengths()
        # After inserting 10 items, table will resize (load factor > 1.0)
        # So chain lengths should match current table size, not initial size
        assert len(chain_lengths) == ht.size
        assert sum(chain_lengths) == 10
    
    def test_resize(self):
        """Test automatic resizing."""
        ht = HashTableSeparateChaining(5, load_factor_threshold=1.0)
        # Insert enough to trigger resize
        for i in range(20):
            ht.insert(i, f"value{i}")
        
        # All should still be searchable
        for i in range(20):
            assert ht.search(i) == f"value{i}"


class TestHashTableComparison:
    """Tests comparing different hash table implementations."""
    
    def test_same_operations_different_implementations(self):
        """Test that different implementations handle same operations."""
        keys = [10, 22, 31, 4, 15, 28, 17, 88, 59]
        
        ht_oa = HashTableOpenAddressing(20, probe_type='linear')
        ht_sc = HashTableSeparateChaining(20)
        
        # Insert same keys
        for key in keys:
            ht_oa.insert(key, f"value{key}")
            ht_sc.insert(key, f"value{key}")
        
        # Both should find all keys
        for key in keys:
            assert ht_oa.search(key) == f"value{key}"
            assert ht_sc.search(key) == f"value{key}"
        
        # Both should delete successfully
        for key in keys[:5]:
            assert ht_oa.delete(key) is True
            assert ht_sc.delete(key) is True
            assert ht_oa.search(key) is None
            assert ht_sc.search(key) is None

