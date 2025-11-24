"""
Demonstration of hash table implementations and their usage.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.hash_tables import (
    DirectAddressTable,
    HashTableOpenAddressing,
    HashTableSeparateChaining
)
from src.hash_functions import (
    division_hash,
    string_hash_polynomial,
    string_hash_simple
)


def demo_direct_address_table():
    """Demonstrate direct-address table."""
    print("=" * 60)
    print("Direct-Address Table Demonstration")
    print("=" * 60)
    
    # Create table for keys in range [0, 99]
    table = DirectAddressTable(100)
    
    # Insert some values
    table.insert(5, "Alice")
    table.insert(42, "Bob")
    table.insert(99, "Charlie")
    
    print("\nInserted key-value pairs:")
    print("  Key 5 ->", table.search(5))
    print("  Key 42 ->", table.search(42))
    print("  Key 99 ->", table.search(99))
    
    # Search
    print("\nSearching for key 42:", table.search(42))
    print("Searching for key 10:", table.search(10))  # Not found
    
    # Delete
    table.delete(42)
    print("\nAfter deleting key 42:")
    print("  Key 42 ->", table.search(42))  # None
    print()


def demo_open_addressing():
    """Demonstrate open addressing hash table."""
    print("=" * 60)
    print("Open Addressing Hash Table Demonstration")
    print("=" * 60)
    
    # Test with linear probing
    print("\n--- Linear Probing ---")
    ht_linear = HashTableOpenAddressing(10, probe_type='linear')
    
    keys = [10, 22, 31, 4, 15, 28, 17, 88, 59]
    for key in keys:
        ht_linear.insert(key, f"Value_{key}")
    
    print(f"Inserted {len(keys)} keys")
    print(f"Load factor: {ht_linear._load_factor():.2f}")
    
    print("\nSearching for keys:")
    for key in [10, 22, 88, 99]:
        result = ht_linear.search(key)
        print(f"  Key {key}: {'Found' if result else 'Not found'}")
    
    # Test with quadratic probing
    print("\n--- Quadratic Probing ---")
    # Use larger table size for quadratic probing to avoid probe sequence issues
    ht_quad = HashTableOpenAddressing(20, probe_type='quadratic')
    
    for key in keys:
        ht_quad.insert(key, f"Value_{key}")
    
    print(f"Inserted {len(keys)} keys")
    print(f"Load factor: {ht_quad._load_factor():.2f}")
    
    # Test with double hashing
    print("\n--- Double Hashing ---")
    # Use larger table size for double hashing to ensure all keys can be inserted
    ht_double = HashTableOpenAddressing(20, probe_type='double')
    
    for key in keys:
        ht_double.insert(key, f"Value_{key}")
    
    print(f"Inserted {len(keys)} keys")
    print(f"Load factor: {ht_double._load_factor():.2f}")
    print()


def demo_separate_chaining():
    """Demonstrate separate chaining hash table."""
    print("=" * 60)
    print("Separate Chaining Hash Table Demonstration")
    print("=" * 60)
    
    ht = HashTableSeparateChaining(10)
    
    keys = [10, 22, 31, 4, 15, 28, 17, 88, 59, 71]
    for key in keys:
        ht.insert(key, f"Value_{key}")
    
    print(f"\nInserted {len(keys)} keys")
    print(f"Load factor: {ht._load_factor():.2f}")
    
    chain_lengths = ht.get_chain_lengths()
    print(f"Chain lengths: {chain_lengths}")
    print(f"Average chain length: {sum(chain_lengths) / len(chain_lengths):.2f}")
    print(f"Maximum chain length: {max(chain_lengths)}")
    
    print("\nSearching for keys:")
    for key in [10, 22, 88, 99]:
        result = ht.search(key)
        print(f"  Key {key}: {'Found' if result else 'Not found'}")
    
    # Delete some keys
    print("\nDeleting keys 22 and 88:")
    ht.delete(22)
    ht.delete(88)
    print(f"  Key 22: {'Found' if ht.search(22) else 'Not found'}")
    print(f"  Key 88: {'Found' if ht.search(88) else 'Not found'}")
    print()


def demo_hash_functions():
    """Demonstrate different hash functions."""
    print("=" * 60)
    print("Hash Function Demonstration")
    print("=" * 60)
    
    keys = [10, 22, 31, 4, 15, 28, 17, 88, 59, 71]
    table_size = 11
    
    print(f"\nKeys: {keys}")
    print(f"Table size: {table_size}\n")
    
    # Division method
    print("Division method (h(k) = k mod m):")
    for key in keys[:5]:
        hash_val = division_hash(key, table_size)
        print(f"  h({key}) = {hash_val}")
    
    # String hashing
    print("\nString hash functions:")
    string_keys = ["hello", "world", "hash", "table", "test"]
    
    print("Simple string hash (BAD - prone to collisions):")
    for key in string_keys:
        hash_val = string_hash_simple(key, table_size)
        print(f"  h('{key}') = {hash_val}")
    
    print("\nPolynomial string hash (GOOD - better distribution):")
    for key in string_keys:
        hash_val = string_hash_polynomial(key, table_size)
        print(f"  h('{key}') = {hash_val}")
    print()


def demo_collision_comparison():
    """Demonstrate collision behavior with different hash functions."""
    print("=" * 60)
    print("Collision Comparison Demonstration")
    print("=" * 60)
    
    # Generate test keys
    keys = list(range(100, 200))
    table_size = 50
    
    from src.hash_functions import (
        division_hash,
        multiplication_hash,
        string_hash_simple,
        string_hash_polynomial
    )
    
    hash_funcs = {
        'Division': division_hash,
        'Multiplication': lambda k, s: multiplication_hash(k, s),
    }
    
    print(f"\nTesting with {len(keys)} keys and table size {table_size}\n")
    
    for name, hash_func in hash_funcs.items():
        hash_values = [hash_func(k, table_size) for k in keys]
        collisions = len(keys) - len(set(hash_values))
        collision_rate = collisions / len(keys) * 100
        
        print(f"{name} method:")
        print(f"  Collisions: {collisions}")
        print(f"  Collision rate: {collision_rate:.2f}%")
        print(f"  Buckets used: {len(set(hash_values))}/{table_size}")
        print()


if __name__ == "__main__":
    demo_direct_address_table()
    demo_open_addressing()
    demo_separate_chaining()
    demo_hash_functions()
    demo_collision_comparison()

