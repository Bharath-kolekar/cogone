"""
Baseline performance measurement before refactoring
This establishes the metrics we must maintain or improve
"""

import time
import tracemalloc
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def measure_original_performance():
    """Measure performance of original monolithic file"""
    
    print("\n" + "="*60)
    print("BASELINE PERFORMANCE MEASUREMENT")
    print("="*60)
    
    # Start memory tracking
    tracemalloc.start()
    
    # Measure import time
    import_start = time.time()
    from app.services.smart_coding_ai_optimized import SmartCodingAIOptimized
    import_end = time.time()
    
    # Measure initialization time
    init_start = time.time()
    service = SmartCodingAIOptimized()
    init_end = time.time()
    
    # Get memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Calculate metrics
    metrics = {
        "import_time": import_end - import_start,
        "init_time": init_end - init_start,
        "total_time": (import_end - import_start) + (init_end - init_start),
        "memory_current_mb": current / 1024 / 1024,
        "memory_peak_mb": peak / 1024 / 1024
    }
    
    # Display results
    print(f"\nImport Time: {metrics['import_time']:.3f} seconds")
    print(f"Init Time: {metrics['init_time']:.3f} seconds")
    print(f"Total Time: {metrics['total_time']:.3f} seconds")
    print(f"Current Memory: {metrics['memory_current_mb']:.2f} MB")
    print(f"Peak Memory: {metrics['memory_peak_mb']:.2f} MB")
    
    # Save baseline for comparison
    with open("baseline_metrics.txt", "w") as f:
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")
    
    print("\nBaseline saved to baseline_metrics.txt")
    print("="*60)
    
    return metrics


def measure_refactored_performance():
    """Measure performance of refactored modular structure"""
    
    print("\n" + "="*60)
    print("REFACTORED PERFORMANCE MEASUREMENT")
    print("="*60)
    
    # Start memory tracking
    tracemalloc.start()
    
    # Measure import time
    import_start = time.time()
    from app.services.smart_coding_ai import SmartCodingAIOptimized
    import_end = time.time()
    
    # Measure initialization time
    init_start = time.time()
    service = SmartCodingAIOptimized()
    init_end = time.time()
    
    # Get memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Calculate metrics
    metrics = {
        "import_time": import_end - import_start,
        "init_time": init_end - init_start,
        "total_time": (import_end - import_start) + (init_end - init_start),
        "memory_current_mb": current / 1024 / 1024,
        "memory_peak_mb": peak / 1024 / 1024
    }
    
    # Display results
    print(f"\nImport Time: {metrics['import_time']:.3f} seconds")
    print(f"Init Time: {metrics['init_time']:.3f} seconds")
    print(f"Total Time: {metrics['total_time']:.3f} seconds")
    print(f"Current Memory: {metrics['memory_current_mb']:.2f} MB")
    print(f"Peak Memory: {metrics['memory_peak_mb']:.2f} MB")
    
    return metrics


def compare_performance():
    """Compare original vs refactored performance"""
    
    # Read baseline
    baseline = {}
    try:
        with open("baseline_metrics.txt", "r") as f:
            for line in f:
                key, value = line.strip().split(": ")
                baseline[key] = float(value)
    except FileNotFoundError:
        print("No baseline found. Run measure_original_performance() first.")
        return
    
    # Measure refactored
    refactored = measure_refactored_performance()
    
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON")
    print("="*60)
    
    # Compare metrics
    for key in baseline:
        original = baseline[key]
        new = refactored[key]
        diff = new - original
        percent = (diff / original) * 100 if original != 0 else 0
        
        if percent < 0:
            status = "IMPROVED"
            symbol = "↓"
        elif percent > 5:
            status = "DEGRADED"
            symbol = "↑"
        else:
            status = "MAINTAINED"
            symbol = "→"
        
        print(f"\n{key}:")
        print(f"  Original: {original:.3f}")
        print(f"  Refactored: {new:.3f}")
        print(f"  Change: {diff:+.3f} ({percent:+.1f}%) {symbol} {status}")
    
    print("\n" + "="*60)
    
    # Overall assessment
    if all(refactored[k] <= baseline[k] * 1.05 for k in baseline):
        print("✓ PASS: Performance maintained or improved!")
    else:
        print("✗ FAIL: Performance degradation detected!")
    
    print("="*60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "baseline":
        measure_original_performance()
    elif len(sys.argv) > 1 and sys.argv[1] == "compare":
        compare_performance()
    else:
        # Default: measure baseline
        measure_original_performance()
