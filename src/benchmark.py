"""
Benchmarking utilities for hash table performance analysis.
"""

import time
import random
import statistics
from typing import List, Dict, Any, Callable, Tuple
from .hash_tables import HashTableOpenAddressing, HashTableSeparateChaining
from .hash_functions import (
    division_hash,
    multiplication_hash,
    string_hash_polynomial,
    string_hash_simple,
    bad_hash_clustering
)


def benchmark_insert(
    hash_table: Any,
    keys: List[int],
    values: List[Any] = None
) -> float:
    """
    Benchmark insertion operations.
    
    Args:
        hash_table: Hash table instance
        keys: List of keys to insert
        values: Optional list of values (defaults to same as keys)
        
    Returns:
        Time taken in seconds
    """
    if values is None:
        values = keys
    
    start = time.perf_counter()
    for key, value in zip(keys, values):
        hash_table.insert(key, value)
    end = time.perf_counter()
    
    return end - start


def benchmark_search(
    hash_table: Any,
    keys: List[int]
) -> Tuple[float, int]:
    """
    Benchmark search operations.
    
    Args:
        hash_table: Hash table instance
        keys: List of keys to search for
        
    Returns:
        Tuple of (time taken in seconds, number of successful searches)
    """
    start = time.perf_counter()
    found = 0
    for key in keys:
        if hash_table.search(key) is not None:
            found += 1
    end = time.perf_counter()
    
    return end - start, found


def benchmark_delete(
    hash_table: Any,
    keys: List[int]
) -> Tuple[float, int]:
    """
    Benchmark delete operations.
    
    Args:
        hash_table: Hash table instance
        keys: List of keys to delete
        
    Returns:
        Tuple of (time taken in seconds, number of successful deletions)
    """
    start = time.perf_counter()
    deleted = 0
    for key in keys:
        if hash_table.delete(key):
            deleted += 1
    end = time.perf_counter()
    
    return end - start, deleted


def generate_test_data(n: int, key_range: Tuple[int, int] = None) -> List[int]:
    """
    Generate test data for benchmarking.
    
    Args:
        n: Number of keys to generate
        key_range: Optional tuple (min, max) for key range
        
    Returns:
        List of random keys
    """
    if key_range is None:
        key_range = (0, n * 10)
    
    random.seed(42)  # For reproducibility
    return [random.randint(key_range[0], key_range[1]) for _ in range(n)]


def benchmark_hash_functions(
    hash_funcs: Dict[str, Callable],
    keys: List[int],
    table_size: int
) -> Dict[str, Dict[str, Any]]:
    """
    Benchmark different hash functions.
    
    Args:
        hash_funcs: Dictionary mapping function names to hash functions
        keys: List of keys to hash
        table_size: Size of hash table
        
    Returns:
        Dictionary with benchmark results including collision counts
    """
    results = {}
    
    for name, hash_func in hash_funcs.items():
        start = time.perf_counter()
        hash_values = [hash_func(k, table_size) for k in keys]
        end = time.perf_counter()
        
        # Count collisions
        collision_count = len(keys) - len(set(hash_values))
        collision_rate = collision_count / len(keys) if keys else 0
        
        # Calculate distribution (variance of bucket sizes)
        bucket_counts = {}
        for hv in hash_values:
            bucket_counts[hv] = bucket_counts.get(hv, 0) + 1
        
        bucket_sizes = list(bucket_counts.values())
        if bucket_sizes:
            avg_bucket_size = sum(bucket_sizes) / len(bucket_sizes)
            variance = sum((x - avg_bucket_size) ** 2 for x in bucket_sizes) / len(bucket_sizes)
        else:
            variance = 0
        
        results[name] = {
            'time': end - start,
            'collisions': collision_count,
            'collision_rate': collision_rate,
            'variance': variance,
            'buckets_used': len(bucket_counts),
            'max_chain_length': max(bucket_sizes) if bucket_sizes else 0
        }
    
    return results


def benchmark_open_addressing_vs_chaining(
    sizes: List[int],
    probe_types: List[str] = ['linear', 'quadratic', 'double']
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Compare open addressing (different probe types) vs separate chaining.
    
    Args:
        sizes: List of data sizes to test
        probe_types: List of probe types to test
        
    Returns:
        Dictionary with benchmark results
    """
    results = {
        'open_addressing': {pt: [] for pt in probe_types},
        'separate_chaining': []
    }
    
    for size in sizes:
        keys = generate_test_data(size)
        table_size = int(size * 1.5)  # Start with 1.5x load factor
        
        # Test open addressing with different probe types
        for probe_type in probe_types:
            ht = HashTableOpenAddressing(table_size, probe_type=probe_type)
            
            insert_time = benchmark_insert(ht, keys)
            search_time, found = benchmark_search(ht, keys[:size//2])
            delete_time, deleted = benchmark_delete(ht, keys[:size//4])
            
            load_factor = ht._load_factor()
            
            results['open_addressing'][probe_type].append({
                'size': size,
                'insert_time': insert_time,
                'search_time': search_time,
                'delete_time': delete_time,
                'load_factor': load_factor,
                'found': found,
                'deleted': deleted
            })
        
        # Test separate chaining
        ht = HashTableSeparateChaining(table_size)
        
        insert_time = benchmark_insert(ht, keys)
        search_time, found = benchmark_search(ht, keys[:size//2])
        delete_time, deleted = benchmark_delete(ht, keys[:size//4])
        
        chain_lengths = ht.get_chain_lengths()
        avg_chain_length = sum(chain_lengths) / len(chain_lengths) if chain_lengths else 0
        max_chain_length = max(chain_lengths) if chain_lengths else 0
        
        results['separate_chaining'].append({
            'size': size,
            'insert_time': insert_time,
            'search_time': search_time,
            'delete_time': delete_time,
            'load_factor': ht._load_factor(),
            'found': found,
            'deleted': deleted,
            'avg_chain_length': avg_chain_length,
            'max_chain_length': max_chain_length
        })
    
    return results


def benchmark_load_factor_impact(
    initial_size: int,
    max_elements: int,
    probe_type: str = 'linear',
    num_runs: int = 5
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Benchmark performance at different load factors with multiple runs for statistical accuracy.
    
    Args:
        initial_size: Initial hash table size
        max_elements: Maximum number of elements to insert
        probe_type: Probe type for open addressing
        num_runs: Number of runs per load factor for averaging
        
    Returns:
        Dictionary with results for open addressing and separate chaining
    """
    results = {
        'open_addressing': [],
        'separate_chaining': []
    }
    
    num_samples = 10
    batch_size = max_elements // num_samples
    
    # Test open addressing
    for i in range(0, max_elements, batch_size):
        if i + batch_size > max_elements:
            continue
        
        # Run multiple times to get statistical averages
        insert_times = []
        search_times = []
        load_factors = []
        
        for run in range(num_runs):
            keys = generate_test_data(max_elements)
            ht_oa = HashTableOpenAddressing(initial_size, probe_type=probe_type)
            inserted_keys_oa = []
            
            # Insert up to (but not including) current batch
            for j in range(0, i, batch_size):
                batch_keys = keys[j:j+batch_size]
                if not batch_keys:
                    continue
                for key in batch_keys:
                    ht_oa.insert(key, key)
                inserted_keys_oa.extend(batch_keys)
            
            # Measure insert time for this batch (normalized per element)
            batch_keys = keys[i:i+batch_size]
            if batch_keys:
                batch_start = time.perf_counter()
                for key in batch_keys:
                    ht_oa.insert(key, key)
                batch_end = time.perf_counter()
                insert_time_per_element = (batch_end - batch_start) / len(batch_keys)
                insert_times.append(insert_time_per_element)
                inserted_keys_oa.extend(batch_keys)
            
            # Benchmark search on a sample of ALL inserted keys
            search_sample_size = min(100, len(inserted_keys_oa))
            search_keys = inserted_keys_oa[:search_sample_size] if inserted_keys_oa else []
            if search_keys:
                search_time, _ = benchmark_search(ht_oa, search_keys)
                search_time_per_element = search_time / len(search_keys)
                search_times.append(search_time_per_element)
            
            load_factors.append(ht_oa._load_factor())
        
        # Compute statistics
        if insert_times and search_times:
            import statistics
            avg_insert = statistics.mean(insert_times)
            std_insert = statistics.stdev(insert_times) if len(insert_times) > 1 else 0
            avg_search = statistics.mean(search_times)
            std_search = statistics.stdev(search_times) if len(search_times) > 1 else 0
            avg_load_factor = statistics.mean(load_factors)
            
            results['open_addressing'].append({
                'elements': i + batch_size,
                'load_factor': avg_load_factor,
                'insert_time': avg_insert,
                'insert_time_std': std_insert,
                'search_time': avg_search,
                'search_time_std': std_search
            })
    
    # Test separate chaining
    for i in range(0, max_elements, batch_size):
        if i + batch_size > max_elements:
            continue
        
        # Run multiple times to get statistical averages
        insert_times = []
        search_times = []
        load_factors = []
        chain_lengths_list = []
        
        for run in range(num_runs):
            keys = generate_test_data(max_elements)
            ht_sc = HashTableSeparateChaining(initial_size)
            inserted_keys_sc = []
            
            # Insert up to (but not including) current batch
            for j in range(0, i, batch_size):
                batch_keys = keys[j:j+batch_size]
                if not batch_keys:
                    continue
                for key in batch_keys:
                    ht_sc.insert(key, key)
                inserted_keys_sc.extend(batch_keys)
            
            # Measure insert time for this batch (normalized per element)
            batch_keys = keys[i:i+batch_size]
            if batch_keys:
                batch_start = time.perf_counter()
                for key in batch_keys:
                    ht_sc.insert(key, key)
                batch_end = time.perf_counter()
                insert_time_per_element = (batch_end - batch_start) / len(batch_keys)
                insert_times.append(insert_time_per_element)
                inserted_keys_sc.extend(batch_keys)
            
            # Benchmark search on a sample of ALL inserted keys
            search_sample_size = min(100, len(inserted_keys_sc))
            search_keys = inserted_keys_sc[:search_sample_size] if inserted_keys_sc else []
            if search_keys:
                search_time, _ = benchmark_search(ht_sc, search_keys)
                search_time_per_element = search_time / len(search_keys)
                search_times.append(search_time_per_element)
            
            chain_lengths = ht_sc.get_chain_lengths()
            # Calculate average chain length only for non-empty buckets
            non_empty_lengths = [l for l in chain_lengths if l > 0]
            avg_chain_length = sum(non_empty_lengths) / len(non_empty_lengths) if non_empty_lengths else 0
            chain_lengths_list.append(avg_chain_length)
            
            load_factors.append(ht_sc._load_factor())
        
        # Compute statistics
        if insert_times and search_times:
            avg_insert = statistics.mean(insert_times)
            std_insert = statistics.stdev(insert_times) if len(insert_times) > 1 else 0
            avg_search = statistics.mean(search_times)
            std_search = statistics.stdev(search_times) if len(search_times) > 1 else 0
            avg_load_factor = statistics.mean(load_factors)
            avg_chain_length = statistics.mean(chain_lengths_list)
            
            results['separate_chaining'].append({
                'elements': i + batch_size,
                'load_factor': avg_load_factor,
                'insert_time': avg_insert,
                'insert_time_std': std_insert,
                'search_time': avg_search,
                'search_time_std': std_search,
                'avg_chain_length': avg_chain_length
            })
    
    return results


def benchmark_load_factor_impact_probes(
    initial_size: int,
    max_elements: int,
    probe_type: str = 'linear',
    num_runs: int = 10
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Benchmark probe counts and comparisons at different load factors.
    Uses deterministic metrics instead of timing for smooth theoretical curves.
    
    Args:
        initial_size: Initial hash table size
        max_elements: Maximum number of elements to insert
        probe_type: Probe type for open addressing
        num_runs: Number of runs per load factor for averaging
        
    Returns:
        Dictionary with results for open addressing and separate chaining
    """
    results = {
        'open_addressing': [],
        'separate_chaining': []
    }
    
    num_samples = 10
    batch_size = max_elements // num_samples
    
    # Test open addressing
    for i in range(0, max_elements, batch_size):
        if i + batch_size > max_elements:
            continue
        
        # Run multiple times to get statistical averages
        insert_probes = []
        search_probes = []
        insert_comparisons = []
        search_comparisons = []
        load_factors = []
        search_sample_size = 100  # Fixed sample size for normalization
        
        for run in range(num_runs):
            keys = generate_test_data(max_elements)
            ht_oa = HashTableOpenAddressing(initial_size, probe_type=probe_type)
            inserted_keys_oa = []
            
            # Insert up to (but not including) current batch
            for j in range(0, i, batch_size):
                batch_keys = keys[j:j+batch_size]
                if not batch_keys:
                    continue
                for key in batch_keys:
                    ht_oa.insert(key, key)
                inserted_keys_oa.extend(batch_keys)
            
            # Reset counters before measuring current batch
            ht_oa.reset_counts()
            
            # Measure insert probes/comparisons for this batch
            batch_keys = keys[i:i+batch_size]
            if batch_keys:
                for key in batch_keys:
                    ht_oa.insert(key, key)
                inserted_keys_oa.extend(batch_keys)
                
                insert_probes.append(ht_oa.get_probe_count())
                insert_comparisons.append(ht_oa.get_comparison_count())
            
            # Reset counters for search
            ht_oa.reset_counts()
            
            # Benchmark search on a sample of ALL inserted keys
            actual_search_size = min(search_sample_size, len(inserted_keys_oa))
            search_keys = inserted_keys_oa[:actual_search_size] if inserted_keys_oa else []
            if search_keys:
                for key in search_keys:
                    ht_oa.search(key)
                
                search_probes.append(ht_oa.get_probe_count())
                search_comparisons.append(ht_oa.get_comparison_count())
            
            load_factors.append(ht_oa._load_factor())
        
        # Compute statistics
        if insert_probes and search_probes:
            # Normalize by batch size and search sample size (fixed at 100)
            avg_insert_probes = statistics.mean(insert_probes) / batch_size if insert_probes and batch_size > 0 else 0
            avg_search_probes = statistics.mean(search_probes) / search_sample_size if search_probes and search_sample_size > 0 else 0
            avg_insert_comparisons = statistics.mean(insert_comparisons) / batch_size if insert_comparisons and batch_size > 0 else 0
            avg_search_comparisons = statistics.mean(search_comparisons) / search_sample_size if search_comparisons and search_sample_size > 0 else 0
            avg_load_factor = statistics.mean(load_factors)
            
            results['open_addressing'].append({
                'elements': i + batch_size,
                'load_factor': avg_load_factor,
                'insert_probes_per_element': avg_insert_probes,
                'search_probes_per_element': avg_search_probes,
                'insert_comparisons_per_element': avg_insert_comparisons,
                'search_comparisons_per_element': avg_search_comparisons
            })
    
    # Test separate chaining
    for i in range(0, max_elements, batch_size):
        if i + batch_size > max_elements:
            continue
        
        # Run multiple times to get statistical averages
        insert_comparisons = []
        search_comparisons = []
        load_factors = []
        chain_lengths_list = []
        search_sample_size = 100  # Fixed sample size for normalization
        
        for run in range(num_runs):
            keys = generate_test_data(max_elements)
            ht_sc = HashTableSeparateChaining(initial_size)
            inserted_keys_sc = []
            
            # Insert up to (but not including) current batch
            for j in range(0, i, batch_size):
                batch_keys = keys[j:j+batch_size]
                if not batch_keys:
                    continue
                for key in batch_keys:
                    ht_sc.insert(key, key)
                inserted_keys_sc.extend(batch_keys)
            
            # Reset counters before measuring current batch
            ht_sc.reset_counts()
            
            # Measure insert comparisons for this batch
            batch_keys = keys[i:i+batch_size]
            if batch_keys:
                for key in batch_keys:
                    ht_sc.insert(key, key)
                inserted_keys_sc.extend(batch_keys)
                
                insert_comparisons.append(ht_sc.get_comparison_count())
            
            # Reset counters for search
            ht_sc.reset_counts()
            
            # Benchmark search on a sample of ALL inserted keys
            actual_search_size = min(search_sample_size, len(inserted_keys_sc))
            search_keys = inserted_keys_sc[:actual_search_size] if inserted_keys_sc else []
            if search_keys:
                for key in search_keys:
                    ht_sc.search(key)
                
                search_comparisons.append(ht_sc.get_comparison_count())
            
            chain_lengths = ht_sc.get_chain_lengths()
            # Calculate average chain length only for non-empty buckets
            non_empty_lengths = [l for l in chain_lengths if l > 0]
            avg_chain_length = sum(non_empty_lengths) / len(non_empty_lengths) if non_empty_lengths else 0
            chain_lengths_list.append(avg_chain_length)
            
            load_factors.append(ht_sc._load_factor())
        
        # Compute statistics
        if insert_comparisons and search_comparisons:
            # Normalize by batch size and search sample size (fixed at 100)
            avg_insert_comparisons = statistics.mean(insert_comparisons) / batch_size if insert_comparisons and batch_size > 0 else 0
            avg_search_comparisons = statistics.mean(search_comparisons) / search_sample_size if search_comparisons and search_sample_size > 0 else 0
            avg_load_factor = statistics.mean(load_factors)
            avg_chain_length = statistics.mean(chain_lengths_list)
            
            results['separate_chaining'].append({
                'elements': i + batch_size,
                'load_factor': avg_load_factor,
                'insert_comparisons_per_element': avg_insert_comparisons,
                'search_comparisons_per_element': avg_search_comparisons,
                'avg_chain_length': avg_chain_length
            })
    
    return results

