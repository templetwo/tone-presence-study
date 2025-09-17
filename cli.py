#!/usr/bin/env python3
"""
Interactive CLI Tool for Tone-Presence Study

Provides convenient command-line interface for running evaluations, analysis, and validation.
"""

import argparse
import sys
import time
from pathlib import Path
import subprocess

# ANSI color codes for output formatting
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_colored(text: str, color: str = Colors.WHITE) -> None:
    """Print text with color formatting."""
    print(f"{color}{text}{Colors.END}")

def print_header(text: str) -> None:
    """Print formatted header."""
    print_colored(f"\n{'='*60}", Colors.CYAN)
    print_colored(f"{text.center(60)}", Colors.BOLD + Colors.CYAN)
    print_colored(f"{'='*60}", Colors.CYAN)

def show_spinner(duration: float = 1.0) -> None:
    """Show simple ASCII spinner."""
    spinner = "|/-\\"
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{spinner[i % len(spinner)]}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print("\r ", end="", flush=True)

def run_command(cmd: list, description: str = "", show_progress: bool = True) -> tuple:
    """Run subprocess command with optional progress indicator."""
    if description:
        print_colored(f"⚡ {description}...", Colors.YELLOW)
    
    if show_progress:
        show_spinner(0.5)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if description:
            print_colored(f"✓ {description} completed", Colors.GREEN)
        return True, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        if description:
            print_colored(f"✗ {description} failed", Colors.RED)
        return False, e.stdout, e.stderr
    except FileNotFoundError:
        print_colored(f"✗ Command not found: {cmd[0]}", Colors.RED)
        return False, "", f"Command not found: {cmd[0]}"

def cmd_demo(args) -> int:
    """Run quick demonstration."""
    print_header("TONE-PRESENCE EFFECT DEMO")
    
    success, stdout, stderr = run_command(
        ['python', 'demo.py'],
        "Running demonstration",
        show_progress=True
    )
    
    if success:
        print(stdout)
        print_colored("\\n🎯 Demo completed successfully!", Colors.GREEN)
        print_colored("Next steps: Try 'python cli.py run' for full evaluation", Colors.CYAN)
        return 0
    else:
        print_colored(f"Demo failed: {stderr}", Colors.RED)
        return 1

def cmd_run(args) -> int:
    """Run evaluation with specified parameters."""
    print_header("RUNNING EVALUATION")
    
    # Build command
    cmd = ['python', 'run_eval.py']
    
    if args.protocol:
        cmd.extend(['--protocol', args.protocol])
    if args.n:
        cmd.extend(['--n', str(args.n)])
    if args.output:
        cmd.extend(['--output', args.output])
    if args.seed:
        cmd.extend(['--seed', str(args.seed)])
    if args.verbose:
        cmd.append('--verbose')
    
    # Show parameters
    print_colored(f"Protocol: {args.protocol or 'default'}", Colors.CYAN)
    print_colored(f"Trials per condition: {args.n or 10}", Colors.CYAN)
    print_colored(f"Output: {args.output or 'results/summary.json'}", Colors.CYAN)
    
    success, stdout, stderr = run_command(
        cmd,
        f"Running evaluation with {args.n or 10} trials",
        show_progress=True
    )
    
    if success:
        print(stdout)
        print_colored("\\n🎯 Evaluation completed successfully!", Colors.GREEN)
        print_colored("Next steps: Run 'python cli.py analyze' to see results", Colors.CYAN)
        return 0
    else:
        print_colored(f"Evaluation failed: {stderr}", Colors.RED)
        return 1

def cmd_analyze(args) -> int:
    """Run analysis on existing results."""
    print_header("ANALYZING RESULTS")
    
    input_file = args.input or 'results/summary.json'
    
    if not Path(input_file).exists():
        print_colored(f"Results file not found: {input_file}", Colors.RED)
        print_colored("Run evaluation first: python cli.py run", Colors.YELLOW)
        return 1
    
    cmd = ['python', 'analyze_results.py']
    if args.input:
        cmd.extend(['--input', args.input])
    if args.output:
        cmd.extend(['--output', args.output])
    if args.format:
        cmd.extend(['--format', args.format])
    
    success, stdout, stderr = run_command(
        cmd,
        "Analyzing results",
        show_progress=True
    )
    
    if success:
        print(stdout)
        print_colored("\\n📊 Analysis completed successfully!", Colors.GREEN)
        return 0
    else:
        print_colored(f"Analysis failed: {stderr}", Colors.RED)
        return 1

def cmd_validate(args) -> int:
    """Run validation checks."""
    print_header("VALIDATING STUDY")
    
    cmd = ['python', 'validate.py']
    
    if args.protocol:
        cmd.extend(['--protocol', args.protocol])
    if args.results:
        cmd.extend(['--results', args.results])
    if args.output:
        cmd.extend(['--output', args.output])
    if args.strict:
        cmd.append('--strict')
    
    success, stdout, stderr = run_command(
        cmd,
        "Running validation checks",
        show_progress=True
    )
    
    print(stdout)
    
    if success:
        print_colored("\\n✅ Validation completed!", Colors.GREEN)
        return 0
    else:
        print_colored("\\n⚠️  Validation completed with issues", Colors.YELLOW)
        return 1 if args.strict else 0

def cmd_report(args) -> int:
    """Generate comprehensive report."""
    print_header("GENERATING COMPREHENSIVE REPORT")
    
    steps = [
        ("Running evaluation", ['python', 'run_eval.py', '--n', str(args.n or 10)]),
        ("Analyzing results", ['python', 'analyze_results.py']),
        ("Validating study", ['python', 'validate.py'])
    ]
    
    for description, cmd in steps:
        success, stdout, stderr = run_command(cmd, description)
        if not success:
            print_colored(f"Report generation failed at: {description}", Colors.RED)
            print_colored(f"Error: {stderr}", Colors.RED)
            return 1
    
    # Copy results to output directory if specified
    if args.output and Path(args.output).is_dir():
        import shutil
        files_to_copy = [
            'results/summary.json',
            'results/analysis_report.md',
            'results/validation_report.txt'
        ]
        
        for file_path in files_to_copy:
            if Path(file_path).exists():
                shutil.copy2(file_path, args.output)
                print_colored(f"📄 Copied {file_path} to {args.output}", Colors.CYAN)
    
    print_colored("\\n📋 Comprehensive report generated!", Colors.GREEN)
    print_colored("Files available in results/ directory", Colors.CYAN)
    return 0

def cmd_clean(args) -> int:
    """Clean temporary files."""
    print_header("CLEANING TEMPORARY FILES")
    
    patterns_to_clean = [
        'results/raw_*',
        '**/__pycache__',
        '**/*.pyc',
        '*.log'
    ]
    
    import glob
    import os
    
    cleaned_count = 0
    for pattern in patterns_to_clean:
        for file_path in glob.glob(pattern, recursive=True):
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    cleaned_count += 1
                elif os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
                    cleaned_count += 1
            except Exception as e:
                print_colored(f"Could not remove {file_path}: {e}", Colors.YELLOW)
    
    print_colored(f"🧹 Cleaned {cleaned_count} files/directories", Colors.GREEN)
    return 0

def cmd_status(args) -> int:
    """Show project status."""
    print_header("PROJECT STATUS")
    
    # Check file existence
    key_files = {
        'Protocol': 'protocols/observation_layer_v1_1.json',
        'Rubric': 'rubrics/pressure_scoring.json',
        'Evaluation Script': 'run_eval.py',
        'Demo Script': 'demo.py',
        'Analysis Script': 'analyze_results.py',
        'Validation Script': 'validate.py'
    }
    
    print_colored("Key Files:", Colors.BOLD)
    for name, path in key_files.items():
        if Path(path).exists():
            print_colored(f"  ✓ {name}: {path}", Colors.GREEN)
        else:
            print_colored(f"  ✗ {name}: {path} (missing)", Colors.RED)
    
    # Check results
    print_colored("\\nResults:", Colors.BOLD)
    results_files = [
        'results/summary.json',
        'results/analysis_report.md',
        'results/validation_report.txt'
    ]
    
    for file_path in results_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print_colored(f"  ✓ {file_path} ({size} bytes)", Colors.GREEN)
        else:
            print_colored(f"  - {file_path} (not generated)", Colors.YELLOW)
    
    # Quick validation
    print_colored("\\nQuick Validation:", Colors.BOLD)
    success, _, _ = run_command(['python', 'validate.py'], show_progress=False)
    if success:
        print_colored("  ✓ Protocol and structure valid", Colors.GREEN)
    else:
        print_colored("  ⚠ Validation issues detected", Colors.YELLOW)
    
    return 0

def main():
    parser = argparse.ArgumentParser(
        description='Interactive CLI for Tone-Presence Study',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py demo                    # Quick demonstration
  python cli.py run --n 20             # Run evaluation with 20 trials
  python cli.py analyze                # Analyze existing results
  python cli.py validate --strict      # Strict validation
  python cli.py report --output app/   # Generate full report
  python cli.py status                 # Check project status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run quick demonstration')
    demo_parser.set_defaults(func=cmd_demo)
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run evaluation')
    run_parser.add_argument('--protocol', help='Protocol file')
    run_parser.add_argument('--n', type=int, help='Trials per condition')
    run_parser.add_argument('--output', help='Output file')
    run_parser.add_argument('--seed', type=int, help='Random seed')
    run_parser.add_argument('--verbose', action='store_true', help='Verbose output')
    run_parser.set_defaults(func=cmd_run)
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze results')
    analyze_parser.add_argument('--input', help='Input results file')
    analyze_parser.add_argument('--output', help='Output report file')
    analyze_parser.add_argument('--format', choices=['markdown', 'text'], help='Output format')
    analyze_parser.set_defaults(func=cmd_analyze)
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate study')
    validate_parser.add_argument('--protocol', help='Protocol file')
    validate_parser.add_argument('--results', help='Results file')
    validate_parser.add_argument('--output', help='Output report file')
    validate_parser.add_argument('--strict', action='store_true', help='Strict mode')
    validate_parser.set_defaults(func=cmd_validate)
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate comprehensive report')
    report_parser.add_argument('--n', type=int, default=10, help='Trials per condition')
    report_parser.add_argument('--output', help='Output directory')
    report_parser.set_defaults(func=cmd_report)
    
    # Clean command
    clean_parser = subparsers.add_parser('clean', help='Clean temporary files')
    clean_parser.set_defaults(func=cmd_clean)
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show project status')
    status_parser.set_defaults(func=cmd_status)
    
    args = parser.parse_args()
    
    if not args.command:
        print_header("TONE-PRESENCE STUDY CLI")
        print_colored("Welcome to the Tone-Presence Study CLI tool!", Colors.CYAN)
        print_colored("\\nQuick start:", Colors.BOLD)
        print_colored("  python cli.py demo      # See the effect in action", Colors.WHITE)
        print_colored("  python cli.py run       # Run full evaluation", Colors.WHITE)
        print_colored("  python cli.py analyze   # Analyze results", Colors.WHITE)
        print_colored("\\nFor help: python cli.py --help", Colors.YELLOW)
        return 0
    
    if hasattr(args, 'func'):
        return args.func(args)
    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print_colored("\\n\\n⚡ Interrupted by user", Colors.YELLOW)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\\n\\n💥 Unexpected error: {e}", Colors.RED)
        sys.exit(1)