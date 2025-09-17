#!/usr/bin/env python3
"""
Generate visualization plot from results/summary.json
"""

import json
import pathlib
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib not installed. Install with: pip install matplotlib")
    exit(1)

def main():
    # Load results
    results_path = pathlib.Path("results/summary.json")
    if not results_path.exists():
        print("No results/summary.json found. Run evaluation first: python run_eval.py")
        exit(1)
    
    d = json.loads(results_path.read_text())
    
    # Create simple bar plot
    x = ["Co-facilitative", "Directive"]
    y = [d["means"]["pressure_cofac"], d["means"]["pressure_directive"]]
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(x, y, color=['lightblue', 'lightcoral'])
    plt.title(f"Conversational Pressure by Interaction Stance\nPMI = {d['PMI']:.2f}")
    plt.ylabel("Mean Pressure Score (0-5)")
    plt.ylim(0, 5)
    
    # Add value labels on bars
    for bar, val in zip(bars, y):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{val:.2f}', ha='center', va='bottom')
    
    # Add PMI annotation
    plt.annotate(f'PMI = {d["PMI"]:.2f}\n({d["trials_per_condition"]} trials/condition)', 
                xy=(0.5, max(y)*0.8), xycoords='data',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"),
                ha='center')
    
    plt.tight_layout()
    
    # Save plot
    output_path = pathlib.Path("results/plot.png")
    output_path.parent.mkdir(exist_ok=True, parents=True)
    plt.savefig(output_path, dpi=160, bbox_inches="tight")
    
    print(f"Plot saved to: {output_path}")

if __name__ == "__main__":
    main()