#!/usr/bin/env python3
"""
Validation Tool for Tone-Presence Study

Checks protocol compliance, validates calculations, and identifies potential issues.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple

class StudyValidator:
    """Validates study protocols, data, and calculations."""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
    
    def validate_protocol(self, protocol_path: str) -> bool:
        """Validate protocol file structure and content."""
        try:
            with open(protocol_path) as f:
                protocol = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.issues.append(f"Protocol file error: {e}")
            return False
        
        # Required fields
        required_fields = ['name', 'conditions', 'test_prompts', 'metrics']
        for field in required_fields:
            if field not in protocol:
                self.issues.append(f"Missing required field: {field}")
        
        # Validate conditions
        if 'conditions' in protocol:
            conditions = protocol['conditions']
            if 'A' not in conditions or 'B' not in conditions:
                self.issues.append("Protocol must define conditions A and B")
            
            for cond_name, cond_data in conditions.items():
                if 'name' not in cond_data:
                    self.issues.append(f"Condition {cond_name} missing name")
        
        # Validate test prompts
        if 'test_prompts' in protocol:
            prompts = protocol['test_prompts']
            if not isinstance(prompts, list) or len(prompts) < 3:
                self.warnings.append("Recommend at least 3 test prompts for reliability")
        
        return len(self.issues) == 0
    
    def validate_results(self, results_path: str) -> bool:
        """Validate results file and calculations."""
        try:
            with open(results_path) as f:
                results = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.issues.append(f"Results file error: {e}")
            return False
        
        # Check required structure
        if 'results' not in results:
            self.issues.append("Results missing 'results' field")
            return False
        
        # Validate PMI calculations
        for i, result in enumerate(results['results']):
            if not self._validate_pmi_calculation(result, i):
                return False
        
        # Validate aggregate statistics
        if 'aggregate_stats' in results:
            self._validate_aggregate_stats(results)
        
        return len(self.issues) == 0
    
    def _validate_pmi_calculation(self, result: Dict[str, Any], index: int) -> bool:
        """Validate individual PMI calculation."""
        try:
            co_fac_pressures = [r['pressure'] for r in result['results_co_facilitative']]
            directive_pressures = [r['pressure'] for r in result['results_directive']]
            
            expected_mean_co_fac = sum(co_fac_pressures) / len(co_fac_pressures)
            expected_mean_directive = sum(directive_pressures) / len(directive_pressures)
            expected_pmi = expected_mean_directive - expected_mean_co_fac
            
            actual_pmi = result['PMI']
            
            if abs(actual_pmi - expected_pmi) > 0.001:
                self.issues.append(f"PMI calculation error in result {index}: expected {expected_pmi:.3f}, got {actual_pmi:.3f}")
                return False
                
        except (KeyError, TypeError, ZeroDivisionError) as e:
            self.issues.append(f"PMI validation error in result {index}: {e}")
            return False
        
        return True
    
    def _validate_aggregate_stats(self, results: Dict[str, Any]) -> None:
        """Validate aggregate statistics calculations."""
        try:
            all_pmis = [r['PMI'] for r in results['results']]
            stats = results['aggregate_stats']
            
            expected_mean = sum(all_pmis) / len(all_pmis)
            if abs(stats['mean_PMI'] - expected_mean) > 0.001:
                self.issues.append(f"Aggregate mean PMI calculation error")
            
            expected_min = min(all_pmis)
            expected_max = max(all_pmis)
            
            if stats['min_PMI'] != expected_min:
                self.issues.append(f"Aggregate min PMI error: expected {expected_min}, got {stats['min_PMI']}")
            
            if stats['max_PMI'] != expected_max:
                self.issues.append(f"Aggregate max PMI error: expected {expected_max}, got {stats['max_PMI']}")
                
        except (KeyError, TypeError, ZeroDivisionError) as e:
            self.issues.append(f"Aggregate stats validation error: {e}")
    
    def check_sample_size(self, results_path: str) -> None:
        """Check if sample size is adequate."""
        try:
            with open(results_path) as f:
                results = json.load(f)
            
            total_trials = results.get('total_trials', 0)
            n_prompts = len(results.get('results', []))
            
            if n_prompts < 5:
                self.warnings.append(f"Small number of test prompts ({n_prompts}). Recommend ≥5 for reliability.")
            
            if total_trials < 100:
                self.warnings.append(f"Small sample size ({total_trials} trials). Recommend ≥100 for statistical power.")
                
        except Exception as e:
            self.warnings.append(f"Could not assess sample size: {e}")
    
    def detect_confounds(self, results_path: str) -> None:
        """Detect potential confounding factors."""
        try:
            with open(results_path) as f:
                results = json.load(f)
            
            # Check for uniform PMI (suggests no real effect)
            pmis = [r['PMI'] for r in results['results']]
            if len(set([round(pmi, 1) for pmi in pmis])) == 1:
                self.warnings.append("All PMI values very similar - check for simulation artifacts")
            
            # Check pressure scale usage
            all_pressures = []
            for result in results['results']:
                all_pressures.extend([r['pressure'] for r in result['results_co_facilitative']])
                all_pressures.extend([r['pressure'] for r in result['results_directive']])
            
            unique_pressures = set(all_pressures)
            if len(unique_pressures) < 3:
                self.warnings.append(f"Limited pressure scale usage ({len(unique_pressures)} values). May indicate simulation bias.")
            
            if max(all_pressures) < 3:
                self.warnings.append("No high-pressure events observed. May indicate insufficient sensitivity.")
                
        except Exception as e:
            self.warnings.append(f"Could not check for confounds: {e}")
    
    def generate_report(self) -> str:
        """Generate validation report."""
        report = []
        report.append("VALIDATION REPORT")
        report.append("=" * 50)
        report.append("")
        
        if not self.issues and not self.warnings:
            report.append("✓ All validations passed successfully")
            report.append("")
            report.append("Study appears ready for:")
            report.append("• Preliminary analysis")
            report.append("• Method replication")
            report.append("• Further data collection")
            return "\n".join(report)
        
        if self.issues:
            report.append("CRITICAL ISSUES:")
            report.append("-" * 20)
            for issue in self.issues:
                report.append(f"✗ {issue}")
            report.append("")
        
        if self.warnings:
            report.append("WARNINGS:")
            report.append("-" * 10)
            for warning in self.warnings:
                report.append(f"⚠ {warning}")
            report.append("")
        
        if self.issues:
            report.append("❌ Validation FAILED - address critical issues before proceeding")
        else:
            report.append("⚠ Validation passed with warnings - review recommendations")
        
        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='Validate tone-presence study')
    parser.add_argument('--protocol', default='protocols/observation_layer_v1_1.json',
                       help='Protocol file to validate')
    parser.add_argument('--results', default='results/summary.json',
                       help='Results file to validate')
    parser.add_argument('--output', default='results/validation_report.txt',
                       help='Output validation report')
    parser.add_argument('--strict', action='store_true',
                       help='Treat warnings as errors')
    
    args = parser.parse_args()
    
    validator = StudyValidator()
    
    # Validate protocol
    print("Validating protocol...")
    if Path(args.protocol).exists():
        validator.validate_protocol(args.protocol)
    else:
        validator.issues.append(f"Protocol file not found: {args.protocol}")
    
    # Validate results if available
    if Path(args.results).exists():
        print("Validating results...")
        validator.validate_results(args.results)
        validator.check_sample_size(args.results)
        validator.detect_confounds(args.results)
    else:
        validator.warnings.append(f"Results file not found: {args.results}")
    
    # Generate report
    report = validator.generate_report()
    
    # Save report
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(report)
    
    # Print to console
    print(report)
    print(f"\nValidation report saved to: {args.output}")
    
    # Exit with error code if issues found
    if validator.issues or (args.strict and validator.warnings):
        return 1
    return 0

if __name__ == '__main__':
    exit(main())