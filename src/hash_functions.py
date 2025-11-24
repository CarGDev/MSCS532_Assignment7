"""
Hash Functions Module

This module implements various hash functions, including good and bad examples
to demonstrate the impact of hash function design on hash table performance.
"""

import hashlib
from typing import Any, Callable, Optional


def division_hash(key: int, table_size: int) -> int:
    """
    Division method hash function: h(k) = k mod m
    
    Simple and fast, but requires careful choice of table size (preferably prime).
    
    Args:
        key: The key to hash
        table_size: Size of the hash table
        
    Returns:
        Hash value in range [0, table_size-1]
    """
    return key % table_size


def multiplication_hash(key: int, table_size: int, A: float = 0.6180339887) -> int:
    """
    Multiplication method hash function: h(k) = floor(m * (kA mod 1))
    
    A good choice of A (often (sqrt(5)-1)/2) helps distribute keys uniformly.
    
    Args:
        key: The key to hash
        table_size: Size of the hash table
        A: Multiplier constant (default: (sqrt(5)-1)/2)
        
    Returns:
        Hash value in range [0, table_size-1]
    """
    return int(table_size * ((key * A) % 1))


def universal_hash(key: int, table_size: int, a: int, b: int, p: int) -> int:
    """
    Universal hash function: h(k) = ((a*k + b) mod p) mod m
    
    Part of a universal class of hash functions that minimizes collisions
    for any set of keys.
    
    Args:
        key: The key to hash
        table_size: Size of the hash table
        a: Random parameter (1 <= a < p)
        b: Random parameter (0 <= b < p)
        p: Large prime number (p > max_key)
        
    Returns:
        Hash value in range [0, table_size-1]
    """
    return ((a * key + b) % p) % table_size


def string_hash_simple(key: str, table_size: int) -> int:
    """
    Simple string hash function (BAD EXAMPLE - prone to collisions).
    
    This is a naive implementation that sums character values.
    Poor distribution for similar strings.
    
    Args:
        key: String key to hash
        table_size: Size of the hash table
        
    Returns:
        Hash value in range [0, table_size-1]
    """
    hash_value = 0
    for char in key:
        hash_value += ord(char)
    return hash_value % table_size


def string_hash_polynomial(key: str, table_size: int, base: int = 31) -> int:
    """
    Polynomial rolling hash function (GOOD EXAMPLE).
    
    Uses polynomial accumulation: h(s) = (s[0]*b^(n-1) + s[1]*b^(n-2) + ... + s[n-1]) mod m
    
    Better distribution than simple summation.
    
    Args:
        key: String key to hash
        table_size: Size of the hash table
        base: Base for polynomial (default: 31)
        
    Returns:
        Hash value in range [0, table_size-1]
    """
    hash_value = 0
    for char in key:
        hash_value = (hash_value * base + ord(char)) % table_size
    return hash_value


def string_hash_djb2(key: str, table_size: int) -> int:
    """
    DJB2 hash function - a popular string hash function.
    
    Known for good distribution properties.
    
    Args:
        key: String key to hash
        table_size: Size of the hash table
        
    Returns:
        Hash value in range [0, table_size-1]
    """
    hash_value = 5381
    for char in key:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)
    return hash_value % table_size


def md5_hash(key: str, table_size: int) -> int:
    """
    MD5-based hash function (cryptographically secure but slower).
    
    Provides excellent distribution but computationally expensive.
    Demonstrates trade-off between speed and quality.
    
    Args:
        key: String key to hash
        table_size: Size of the hash table
        
    Returns:
        Hash value in range [0, table_size-1]
    """
    md5_hash_obj = hashlib.md5(key.encode('utf-8'))
    hash_int = int(md5_hash_obj.hexdigest(), 16)
    return hash_int % table_size


def bad_hash_clustering(key: int, table_size: int) -> int:
    """
    BAD EXAMPLE: Hash function that causes clustering.
    
    This function uses a poor multiplier that causes many collisions
    and clustering behavior.
    
    Args:
        key: The key to hash
        table_size: Size of the hash table
        
    Returns:
        Hash value (poorly distributed)
    """
    # Poor choice: using table_size as multiplier causes clustering
    return (key * table_size) % table_size


def get_hash_function(hash_type: str) -> Callable:
    """
    Get a hash function by name.
    
    Args:
        hash_type: Type of hash function ('division', 'multiplication', 'universal', etc.)
        
    Returns:
        Hash function callable
    """
    hash_functions = {
        'division': division_hash,
        'multiplication': multiplication_hash,
        'string_simple': string_hash_simple,
        'string_polynomial': string_hash_polynomial,
        'string_djb2': string_hash_djb2,
        'md5': md5_hash,
        'bad_clustering': bad_hash_clustering,
    }
    return hash_functions.get(hash_type, division_hash)

