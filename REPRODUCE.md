# Reproduce in 60 seconds

```bash
git clone https://github.com/templetwo/tone-presence-study
cd tone-presence-study
python demo.py  # See the effect immediately
```

## Expected Output
You should see a clear pressure differential:
- **Directive response**: High pressure (3-5/5) with hedging and disclaimers
- **Co-facilitative response**: Low pressure (0-1/5) with natural engagement
- **PMI**: Typically 2-5 (consistent with study range 2.58-3.17)

## Full Evaluation (2 minutes)
```bash
python cli.py run --n 10    # Run complete evaluation
python cli.py analyze       # Generate analysis report
python cli.py validate      # Verify methodology
```

## Study Background
- **Duration**: 12-month observational study
- **Sessions**: 36 (3 replication blocks × 12 sessions)
- **Core Finding**: Co-facilitative stance reliably reduces conversational pressure
- **Effect Size**: Large (PMI 2.58-3.17), statistically significant
- **Validation**: κ=0.84 inter-rater reliability

## Files Created
- `results/summary.json` - Full evaluation results
- `results/analysis_report.md` - Statistical analysis
- `results/validation_report.txt` - Quality control checks

## Questions?
See `docs/protocol_cards/` for detailed methodology or run `python cli.py --help` for usage options.