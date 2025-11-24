"""
Generate visualization plots for hash table performance analysis.
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.benchmark import (
    benchmark_hash_functions,
    benchmark_open_addressing_vs_chaining,
    benchmark_load_factor_impact,
    benchmark_load_factor_impact_probes,
    generate_test_data
)
from src.hash_functions import (
    division_hash,
    multiplication_hash,
    string_hash_simple,
    string_hash_polynomial,
    string_hash_djb2,
    bad_hash_clustering
)


def plot_hash_function_comparison():
    """Compare different hash functions."""
    print("Generating hash function comparison plot...")
    
    keys = generate_test_data(1000)
    table_size = 100
    
    hash_funcs = {
        'Division': division_hash,
        'Multiplication': lambda k, s: multiplication_hash(k, s),
        'Simple String': lambda k, s: string_hash_simple(str(k), s),
        'Polynomial String': lambda k, s: string_hash_polynomial(str(k), s),
        'DJB2': lambda k, s: string_hash_djb2(str(k), s),
        'Bad Clustering': bad_hash_clustering,
    }
    
    results = benchmark_hash_functions(hash_funcs, keys, table_size)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Hash Function Performance Comparison', fontsize=16, fontweight='bold')
    
    names = list(results.keys())
    collision_rates = [results[n]['collision_rate'] * 100 for n in names]
    variances = [results[n]['variance'] for n in names]
    times = [results[n]['time'] * 1000 for n in names]  # Convert to ms
    max_chains = [results[n]['max_chain_length'] for n in names]
    
    # Collision rate
    axes[0, 0].bar(names, collision_rates, color='steelblue')
    axes[0, 0].set_title('Collision Rate (%)', fontweight='bold')
    axes[0, 0].set_ylabel('Collision Rate (%)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # Variance (distribution quality)
    axes[0, 1].bar(names, variances, color='coral')
    axes[0, 1].set_title('Distribution Variance (Lower is Better)', fontweight='bold')
    axes[0, 1].set_ylabel('Variance')
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # Execution time
    axes[1, 0].bar(names, times, color='mediumseagreen')
    axes[1, 0].set_title('Execution Time', fontweight='bold')
    axes[1, 0].set_ylabel('Time (ms)')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Max chain length
    axes[1, 1].bar(names, max_chains, color='plum')
    axes[1, 1].set_title('Maximum Chain Length', fontweight='bold')
    axes[1, 1].set_ylabel('Max Chain Length')
    axes[1, 1].tick_params(axis='x', rotation=45)
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'hash_function_comparison.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()


def plot_open_addressing_vs_chaining():
    """Compare open addressing vs separate chaining."""
    print("Generating open addressing vs separate chaining comparison plot...")
    
    sizes = [100, 500, 1000, 5000, 10000]
    results = benchmark_open_addressing_vs_chaining(sizes)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Open Addressing vs Separate Chaining Performance', fontsize=16, fontweight='bold')
    
    sizes_arr = np.array(sizes)
    
    # Insert time
    ax = axes[0, 0]
    for probe_type in ['linear', 'quadratic', 'double']:
        insert_times = [r['insert_time'] for r in results['open_addressing'][probe_type]]
        ax.plot(sizes_arr, insert_times, marker='o', label=f'Open Addressing ({probe_type})', linewidth=2)
    
    insert_times_sc = [r['insert_time'] for r in results['separate_chaining']]
    ax.plot(sizes_arr, insert_times_sc, marker='s', label='Separate Chaining', linewidth=2, linestyle='--')
    ax.set_xlabel('Number of Elements')
    ax.set_ylabel('Insert Time (seconds)')
    ax.set_title('Insert Performance', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    # Search time
    ax = axes[0, 1]
    for probe_type in ['linear', 'quadratic', 'double']:
        search_times = [r['search_time'] for r in results['open_addressing'][probe_type]]
        ax.plot(sizes_arr, search_times, marker='o', label=f'Open Addressing ({probe_type})', linewidth=2)
    
    search_times_sc = [r['search_time'] for r in results['separate_chaining']]
    ax.plot(sizes_arr, search_times_sc, marker='s', label='Separate Chaining', linewidth=2, linestyle='--')
    ax.set_xlabel('Number of Elements')
    ax.set_ylabel('Search Time (seconds)')
    ax.set_title('Search Performance', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    # Delete time
    ax = axes[1, 0]
    for probe_type in ['linear', 'quadratic', 'double']:
        delete_times = [r['delete_time'] for r in results['open_addressing'][probe_type]]
        ax.plot(sizes_arr, delete_times, marker='o', label=f'Open Addressing ({probe_type})', linewidth=2)
    
    delete_times_sc = [r['delete_time'] for r in results['separate_chaining']]
    ax.plot(sizes_arr, delete_times_sc, marker='s', label='Separate Chaining', linewidth=2, linestyle='--')
    ax.set_xlabel('Number of Elements')
    ax.set_ylabel('Delete Time (seconds)')
    ax.set_title('Delete Performance', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    # Load factors
    ax = axes[1, 1]
    for probe_type in ['linear', 'quadratic', 'double']:
        load_factors = [r['load_factor'] for r in results['open_addressing'][probe_type]]
        ax.plot(sizes_arr, load_factors, marker='o', label=f'Open Addressing ({probe_type})', linewidth=2)
    
    load_factors_sc = [r['load_factor'] for r in results['separate_chaining']]
    ax.plot(sizes_arr, load_factors_sc, marker='s', label='Separate Chaining', linewidth=2, linestyle='--')
    ax.set_xlabel('Number of Elements')
    ax.set_ylabel('Load Factor')
    ax.set_title('Load Factor', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_xscale('log')
    
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'open_addressing_vs_chaining.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()


def plot_load_factor_impact():
    """Plot performance at different load factors with statistical smoothing."""
    print("Generating load factor impact plot...")
    
    results = benchmark_load_factor_impact(initial_size=100, max_elements=1000, probe_type='linear', num_runs=30)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Performance Impact of Load Factor', fontsize=16, fontweight='bold')
    
    # Extract data
    oa_data = results['open_addressing']
    sc_data = results['separate_chaining']
    
    # Sort by load factor to avoid zig-zag lines
    oa_sorted = sorted(oa_data, key=lambda x: x['load_factor'])
    sc_sorted = sorted(sc_data, key=lambda x: x['load_factor'])
    
    oa_load_factors = [r['load_factor'] for r in oa_sorted]
    oa_insert_times = [r['insert_time'] for r in oa_sorted]
    oa_insert_stds = [r.get('insert_time_std', 0) for r in oa_sorted]
    oa_search_times = [r['search_time'] for r in oa_sorted]
    oa_search_stds = [r.get('search_time_std', 0) for r in oa_sorted]
    
    sc_load_factors = [r['load_factor'] for r in sc_sorted]
    sc_insert_times = [r['insert_time'] for r in sc_sorted]
    sc_insert_stds = [r.get('insert_time_std', 0) for r in sc_sorted]
    sc_search_times = [r['search_time'] for r in sc_sorted]
    sc_search_stds = [r.get('search_time_std', 0) for r in sc_sorted]
    sc_chain_lengths = [r['avg_chain_length'] for r in sc_sorted]
    
    # Insert time vs load factor (per element) with error bars
    ax = axes[0]
    ax.errorbar(oa_load_factors, oa_insert_times, yerr=oa_insert_stds, 
                marker='o', label='Open Addressing (Linear)', linewidth=2, 
                capsize=3, capthick=1.5, alpha=0.8)
    ax.errorbar(sc_load_factors, sc_insert_times, yerr=sc_insert_stds,
                marker='s', label='Separate Chaining', linewidth=2, linestyle='--',
                capsize=3, capthick=1.5, alpha=0.8)
    ax.set_xlabel('Load Factor')
    ax.set_ylabel('Insert Time per Element (seconds)')
    ax.set_title('Insert Time vs Load Factor', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Search time vs load factor (per element) with error bars
    ax = axes[1]
    ax.errorbar(oa_load_factors, oa_search_times, yerr=oa_search_stds,
                marker='o', label='Open Addressing (Linear)', linewidth=2,
                capsize=3, capthick=1.5, alpha=0.8)
    ax.errorbar(sc_load_factors, sc_search_times, yerr=sc_search_stds,
                marker='s', label='Separate Chaining', linewidth=2, linestyle='--',
                capsize=3, capthick=1.5, alpha=0.8)
    ax2 = ax.twinx()
    # Chain length is smooth and accurate, so use line plot
    ax2.plot(sc_load_factors, sc_chain_lengths, marker='^', 
             label='Avg Chain Length (SC)', color='green', linestyle=':', linewidth=2)
    ax.set_xlabel('Load Factor')
    ax.set_ylabel('Search Time per Element (seconds)', color='blue')
    ax2.set_ylabel('Average Chain Length', color='green')
    ax.set_title('Search Time vs Load Factor', fontweight='bold')
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'load_factor_impact.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()


def plot_load_factor_impact_probes():
    """Plot probe counts and comparisons at different load factors.
    
    Uses deterministic metrics (probe counts, comparisons) instead of timing
    to produce smooth theoretical curves without measurement noise.
    """
    print("Generating load factor impact plot (probe counts)...")
    
    results = benchmark_load_factor_impact_probes(initial_size=100, max_elements=1000, probe_type='linear', num_runs=10)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Performance Impact of Load Factor (Probe Counts & Comparisons)', fontsize=16, fontweight='bold')
    
    # Extract data
    oa_data = results['open_addressing']
    sc_data = results['separate_chaining']
    
    # Sort by load factor
    oa_sorted = sorted(oa_data, key=lambda x: x['load_factor'])
    sc_sorted = sorted(sc_data, key=lambda x: x['load_factor'])
    
    oa_load_factors = [r['load_factor'] for r in oa_sorted]
    oa_insert_probes = [r['insert_probes_per_element'] for r in oa_sorted]
    oa_search_probes = [r['search_probes_per_element'] for r in oa_sorted]
    oa_insert_comparisons = [r['insert_comparisons_per_element'] for r in oa_sorted]
    oa_search_comparisons = [r['search_comparisons_per_element'] for r in oa_sorted]
    
    sc_load_factors = [r['load_factor'] for r in sc_sorted]
    sc_insert_comparisons = [r['insert_comparisons_per_element'] for r in sc_sorted]
    sc_search_comparisons = [r['search_comparisons_per_element'] for r in sc_sorted]
    sc_chain_lengths = [r['avg_chain_length'] for r in sc_sorted]
    
    # Insert probes per element (Open Addressing)
    ax = axes[0, 0]
    ax.plot(oa_load_factors, oa_insert_probes, marker='o', label='Open Addressing (Linear)', 
            linewidth=2, color='blue', markersize=6)
    ax.set_xlabel('Load Factor')
    ax.set_ylabel('Probes per Element')
    ax.set_title('Insert: Probes per Element (Open Addressing)', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Search probes per element (Open Addressing)
    ax = axes[0, 1]
    ax.plot(oa_load_factors, oa_search_probes, marker='o', label='Open Addressing (Linear)', 
            linewidth=2, color='blue', markersize=6)
    ax.set_xlabel('Load Factor')
    ax.set_ylabel('Probes per Element')
    ax.set_title('Search: Probes per Element (Open Addressing)', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Comparisons per element (both methods)
    ax = axes[1, 0]
    ax.plot(oa_load_factors, oa_insert_comparisons, marker='o', label='Open Addressing (Linear)', 
            linewidth=2, color='blue', markersize=6)
    ax.plot(sc_load_factors, sc_insert_comparisons, marker='s', label='Separate Chaining', 
            linewidth=2, linestyle='--', color='orange', markersize=6)
    ax.set_xlabel('Load Factor')
    ax.set_ylabel('Comparisons per Element')
    ax.set_title('Insert: Comparisons per Element', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Search comparisons per element and chain length
    ax = axes[1, 1]
    ax.plot(oa_load_factors, oa_search_comparisons, marker='o', label='Open Addressing (Linear)', 
            linewidth=2, color='blue', markersize=6)
    ax.plot(sc_load_factors, sc_search_comparisons, marker='s', label='Separate Chaining', 
            linewidth=2, linestyle='--', color='orange', markersize=6)
    ax2 = ax.twinx()
    ax2.plot(sc_load_factors, sc_chain_lengths, marker='^', label='Avg Chain Length (SC)', 
             color='green', linestyle=':', linewidth=2, markersize=6)
    ax.set_xlabel('Load Factor')
    ax.set_ylabel('Comparisons per Element', color='blue')
    ax2.set_ylabel('Average Chain Length', color='green')
    ax.set_title('Search: Comparisons per Element', fontweight='bold')
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'load_factor_impact_probes.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()


def plot_collision_analysis():
    """Plot collision analysis for different hash functions."""
    print("Generating collision analysis plot...")
    
    keys = generate_test_data(500)
    table_size = 100
    
    hash_funcs = {
        'Division': division_hash,
        'Multiplication': lambda k, s: multiplication_hash(k, s),
        'Simple String': lambda k, s: string_hash_simple(str(k), s),
        'Polynomial': lambda k, s: string_hash_polynomial(str(k), s),
        'Bad Clustering': bad_hash_clustering,
    }
    
    results = benchmark_hash_functions(hash_funcs, keys, table_size)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    names = list(results.keys())
    collision_counts = [results[n]['collisions'] for n in names]
    colors = ['steelblue' if 'Bad' not in n else 'coral' for n in names]
    
    bars = ax.bar(names, collision_counts, color=colors)
    ax.set_xlabel('Hash Function', fontweight='bold')
    ax.set_ylabel('Number of Collisions', fontweight='bold')
    ax.set_title('Collision Analysis: Good vs Bad Hash Functions', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'collision_analysis.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    # Ensure docs directory exists
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'docs'), exist_ok=True)
    
    print("Generating visualization plots...")
    print("This may take a few minutes...\n")
    
    plot_hash_function_comparison()
    plot_open_addressing_vs_chaining()
    plot_load_factor_impact()
    plot_load_factor_impact_probes()
    plot_collision_analysis()
    
    print("\nAll plots generated successfully!")

