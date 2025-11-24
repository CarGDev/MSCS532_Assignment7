"""
Tests for hash functions.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.hash_functions import (
    division_hash,
    multiplication_hash,
    universal_hash,
    string_hash_simple,
    string_hash_polynomial,
    string_hash_djb2,
    md5_hash,
    bad_hash_clustering
)


class TestDivisionHash:
    """Tests for division hash function."""
    
    def test_basic_division_hash(self):
        """Test basic division hash functionality."""
        assert division_hash(10, 7) == 3
        assert division_hash(22, 7) == 1
        assert division_hash(31, 7) == 3
    
    def test_hash_range(self):
        """Test that hash values are in correct range."""
        table_size = 11
        for key in range(100):
            hash_val = division_hash(key, table_size)
            assert 0 <= hash_val < table_size
    
    def test_negative_keys(self):
        """Test handling of negative keys."""
        # Division with negative keys
        assert division_hash(-10, 7) == (-10 % 7)


class TestMultiplicationHash:
    """Tests for multiplication hash function."""
    
    def test_basic_multiplication_hash(self):
        """Test basic multiplication hash functionality."""
        hash_val = multiplication_hash(10, 8)
        assert 0 <= hash_val < 8
    
    def test_hash_range(self):
        """Test that hash values are in correct range."""
        table_size = 16
        for key in range(50):
            hash_val = multiplication_hash(key, table_size)
            assert 0 <= hash_val < table_size


class TestUniversalHash:
    """Tests for universal hash function."""
    
    def test_basic_universal_hash(self):
        """Test basic universal hash functionality."""
        p = 101  # Prime larger than max key
        a, b = 3, 7
        hash_val = universal_hash(10, 11, a, b, p)
        assert 0 <= hash_val < 11
    
    def test_hash_range(self):
        """Test that hash values are in correct range."""
        table_size = 13
        p = 101
        a, b = 5, 11
        for key in range(50):
            hash_val = universal_hash(key, table_size, a, b, p)
            assert 0 <= hash_val < table_size


class TestStringHashFunctions:
    """Tests for string hash functions."""
    
    def test_string_hash_simple(self):
        """Test simple string hash function."""
        hash_val = string_hash_simple("hello", 11)
        assert 0 <= hash_val < 11
    
    def test_string_hash_polynomial(self):
        """Test polynomial string hash function."""
        hash_val = string_hash_polynomial("hello", 11)
        assert 0 <= hash_val < 11
    
    def test_string_hash_djb2(self):
        """Test DJB2 string hash function."""
        hash_val = string_hash_djb2("hello", 11)
        assert 0 <= hash_val < 11
    
    def test_string_hash_collisions(self):
        """Test that different strings can produce different hashes."""
        table_size = 100
        strings = ["hello", "world", "test", "hash", "table"]
        hashes = [string_hash_polynomial(s, table_size) for s in strings]
        # At least some should be different (not guaranteed all)
        assert len(set(hashes)) > 1
    
    def test_md5_hash(self):
        """Test MD5-based hash function."""
        hash_val = md5_hash("test", 11)
        assert 0 <= hash_val < 11


class TestBadHashFunctions:
    """Tests for bad hash functions (demonstrating poor behavior)."""
    
    def test_bad_hash_clustering(self):
        """Test bad hash function that causes clustering."""
        # This should demonstrate poor distribution
        table_size = 10
        keys = list(range(20))
        hashes = [bad_hash_clustering(k, table_size) for k in keys]
        # All hashes should be 0 (demonstrating clustering)
        assert all(h == 0 for h in hashes)


class TestHashFunctionProperties:
    """Tests for hash function properties."""
    
    def test_deterministic(self):
        """Test that hash functions are deterministic."""
        key = 42
        table_size = 11
        hash1 = division_hash(key, table_size)
        hash2 = division_hash(key, table_size)
        assert hash1 == hash2
    
    def test_distribution(self):
        """Test that good hash functions distribute keys reasonably."""
        table_size = 20
        keys = list(range(100))
        hashes = [division_hash(k, table_size) for k in keys]
        
        # Count occurrences in each bucket
        bucket_counts = {}
        for h in hashes:
            bucket_counts[h] = bucket_counts.get(h, 0) + 1
        
        # Most buckets should be used (not perfect, but reasonable)
        buckets_used = len(bucket_counts)
        assert buckets_used > table_size * 0.5  # At least 50% of buckets used

