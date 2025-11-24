"""
Hash Tables and Hash Functions Package

This package provides implementations of various hash table data structures
and hash functions for educational and research purposes.
"""

from .hash_functions import (
    division_hash,
    multiplication_hash,
    universal_hash,
    string_hash_simple,
    string_hash_polynomial,
    string_hash_djb2,
    md5_hash,
    bad_hash_clustering,
    get_hash_function
)

from .hash_tables import (
    DirectAddressTable,
    HashTableOpenAddressing,
    HashTableSeparateChaining
)

__all__ = [
    'division_hash',
    'multiplication_hash',
    'universal_hash',
    'string_hash_simple',
    'string_hash_polynomial',
    'string_hash_djb2',
    'md5_hash',
    'bad_hash_clustering',
    'get_hash_function',
    'DirectAddressTable',
    'HashTableOpenAddressing',
    'HashTableSeparateChaining',
]

