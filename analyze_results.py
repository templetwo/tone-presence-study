#!/usr/bin/env python3
"""
Results Analysis Tool for Tone-Presence Study

Analyzes evaluation results and generates reports with visualizations.
"""

import json
import statistics
from pathlib import Path
from typing import Dict, List, Any
import argparse

class ResultsAnalyzer:
    """Analyzes evaluation results and generates insights."""
    
    def __init__(self, results_path: str):
        with open(results_path) as f:
            self.results = json.load(f)
    
    def generate_ascii_histogram(self, data: List[float], title: str, width: int = 50) -> str:
        """Generate simple ASCII histogram."""
        if not data:
            return f"{title}: No data"
        
        min_val, max_val = min(data), max(data)
        if min_val == max_val:
            return f"{title}: All values = {min_val:.2f}"
        
        # Create bins
        bins = 10
        bin_width = (max_val - min_val) / bins
        bin_counts = [0] * bins
        
        for value in data:
            bin_idx = min(int((value - min_val) / bin_width), bins - 1)
            bin_counts[bin_idx] += 1
        
        max_count = max(bin_counts)
        scale = width / max_count if max_count > 0 else 1
        
        result = [f"{title}:"]
        for i, count in enumerate(bin_counts):
            bin_start = min_val + i * bin_width
            bin_end = min_val + (i + 1) * bin_width
            bar_length = int(count * scale)
            bar = "█" * bar_length
            result.append(f"{bin_start:5.2f}-{bin_end:5.2f}: {bar} ({count})")
        
        return "\n".join(result)
    
    def analyze_pressure_distributions(self) -> Dict[str, Any]:
        """Analyze pressure score distributions by condition."""
        co_fac_pressures = []
        directive_pressures = []
        
        for result in self.results['results']:
            co_fac_pressures.extend([r['pressure'] for r in result['results_co_facilitative']])
            directive_pressures.extend([r['pressure'] for r in result['results_directive']])
        
        return {
            'co_facilitative': {
                'pressures': co_fac_pressures,
                'mean': statistics.mean(co_fac_pressures),
                'median': statistics.median(co_fac_pressures),
                'std': statistics.stdev(co_fac_pressures) if len(co_fac_pressures) > 1 else 0,
                'histogram': self.generate_ascii_histogram(co_fac_pressures, "Co-facilitative Pressure Distribution")
            },
            'directive': {
                'pressures': directive_pressures,
                'mean': statistics.mean(directive_pressures),
                'median': statistics.median(directive_pressures),
                'std': statistics.stdev(directive_pressures) if len(directive_pressures) > 1 else 0,
                'histogram': self.generate_ascii_histogram(directive_pressures, "Directive Pressure Distribution")
            }
        }
    
    def identify_outliers(self, data: List[float], threshold: float = 2.0) -> List[int]:
        """Identify outliers using z-score method."""
        if len(data) < 3:
            return []
        
        mean_val = statistics.mean(data)
        std_val = statistics.stdev(data)
        
        if std_val == 0:
            return []
        
        outliers = []
        for i, value in enumerate(data):
            z_score = abs((value - mean_val) / std_val)
            if z_score > threshold:
                outliers.append(i)
        
        return outliers
    
    def generate_report(self) -> str:
        """Generate comprehensive analysis report."""
        report = []
        report.append("=" * 60)
        report.append("TONE-PRESENCE STUDY ANALYSIS REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Basic info
        report.append(f"Protocol: {self.results['protocol']}")
        report.append(f"Timestamp: {self.results['timestamp']}")
        report.append(f"Total trials: {self.results['total_trials']}")
        report.append("")
        
        # Aggregate statistics
        stats = self.results['aggregate_stats']
        report.append("AGGREGATE STATISTICS:")
        report.append("-" * 20)
        report.append(f"Mean PMI: {stats['mean_PMI']:.3f}")
        report.append(f"Median PMI: {stats['median_PMI']:.3f}")
        report.append(f"Std PMI: {stats['std_PMI']:.3f}")
        report.append(f"PMI Range: {stats['min_PMI']:.3f} to {stats['max_PMI']:.3f}")
        report.append(f"Effect Significant: {stats['effect_significant']}")
        report.append("")
        
        # Pressure distributions
        distributions = self.analyze_pressure_distributions()
        report.append("PRESSURE DISTRIBUTIONS:")
        report.append("-" * 25)
        report.append("")
        report.append(distributions['co_facilitative']['histogram'])
        report.append(f"Mean: {distributions['co_facilitative']['mean']:.2f}, "
                     f"Std: {distributions['co_facilitative']['std']:.2f}")
        report.append("")
        report.append(distributions['directive']['histogram'])
        report.append(f"Mean: {distributions['directive']['mean']:.2f}, "
                     f"Std: {distributions['directive']['std']:.2f}")
        report.append("")
        
        # PMI analysis by prompt
        pmis = [r['PMI'] for r in self.results['results']]
        report.append("PMI BY PROMPT:")
        report.append("-" * 15)
        for i, result in enumerate(self.results['results']):
            prompt_short = result['prompt'][:40] + "..." if len(result['prompt']) > 40 else result['prompt']
            report.append(f"{i+1:2d}. {prompt_short:43} PMI: {result['PMI']:5.2f}")
        report.append("")
        
        # Outlier analysis
        outlier_indices = self.identify_outliers(pmis)
        if outlier_indices:
            report.append("OUTLIERS DETECTED:")
            report.append("-" * 18)
            for idx in outlier_indices:
                result = self.results['results'][idx]
                prompt_short = result['prompt'][:40] + "..." if len(result['prompt']) > 40 else result['prompt']
                report.append(f"  {prompt_short}: PMI = {result['PMI']:.2f}")
        else:
            report.append("No significant outliers detected.")
        report.append("")
        
        # Validation notes
        report.append("VALIDATION NOTES:")
        report.append("-" * 17)
        report.append("• Results based on automated pressure scoring")
        report.append("• Human validation recommended for publication")
        report.append("• Sample size suitable for preliminary analysis")
        report.append("• Replication encouraged with different models")
        
        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='Analyze tone-presence evaluation results')
    parser.add_argument('--input', default='results/summary.json',
                       help='Input results file')
    parser.add_argument('--output', default='results/analysis_report.md',
                       help='Output report file')
    parser.add_argument('--format', choices=['markdown', 'text'], default='markdown',
                       help='Output format')
    
    args = parser.parse_args()
    
    if not Path(args.input).exists():
        print(f"Error: Results file {args.input} not found")
        print("Run 'python run_eval.py' first to generate results")
        return
    
    analyzer = ResultsAnalyzer(args.input)
    report = analyzer.generate_report()
    
    # Add markdown formatting if requested
    if args.format == 'markdown':
        report = f"# Tone-Presence Study Analysis\n\n```\n{report}\n```"
    
    # Save report
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(report)
    
    print(f"Analysis complete. Report saved to: {args.output}")
    print("\nQuick Summary:")
    print("-" * 40)
    
    # Print key stats
    with open(args.input) as f:
        results = json.load(f)
    
    stats = results['aggregate_stats']
    print(f"Mean PMI: {stats['mean_PMI']:.3f}")
    print(f"Effect Size: {'Large' if stats['mean_PMI'] > 2.5 else 'Medium' if stats['mean_PMI'] > 1.5 else 'Small'}")
    print(f"Significant: {'Yes' if stats['effect_significant'] else 'No'}")

if __name__ == '__main__':
    main()