#!/usr/bin/env python3
"""
Schema Validation for Tone-Presence Study Results

Validates results.json files against the defined schema for interoperability.
"""

import json
import argparse
import sys
from pathlib import Path

def validate_results_schema(results_file: str, schema_file: str = "docs/results.schema.json") -> bool:
    """Validate results file against JSON schema."""
    
    try:
        import jsonschema
    except ImportError:
        print("Warning: jsonschema not installed. Install with: pip install jsonschema")
        print("Skipping schema validation...")
        return True
    
    # Load schema
    try:
        with open(schema_file) as f:
            schema = json.load(f)
    except FileNotFoundError:
        print(f"Error: Schema file {schema_file} not found")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in schema file: {e}")
        return False
    
    # Load results
    try:
        with open(results_file) as f:
            results = json.load(f)
    except FileNotFoundError:
        print(f"Error: Results file {results_file} not found")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in results file: {e}")
        return False
    
    # Validate
    try:
        jsonschema.validate(instance=results, schema=schema)
        print(f"✓ Results file {results_file} validates against schema")
        return True
    except jsonschema.ValidationError as e:
        print(f"✗ Schema validation failed: {e.message}")
        print(f"  Path: {' -> '.join(str(p) for p in e.path)}")
        return False
    except jsonschema.SchemaError as e:
        print(f"Error: Invalid schema: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Validate results against schema')
    parser.add_argument('results_file', help='Results JSON file to validate')
    parser.add_argument('--schema', default='docs/results.schema.json',
                       help='Schema file to validate against')
    
    args = parser.parse_args()
    
    success = validate_results_schema(args.results_file, args.schema)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()