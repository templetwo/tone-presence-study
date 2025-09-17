# Tone-Presence Study: One-Page Summary

## Thesis
Respectful, co-facilitative prompts measurably reduce conversational "pressure" versus directive phrasing (PMI ≈ 2.6–3.2).

## Method
A/B stance protocols, fixed seeds/temps, 8-turn "coherence corridor," automated proxy + human rubric; compute κ/α agreement.

## Key Results
- PMI range: 2.58–3.17 across 3 replication blocks
- Coherence corridor success: ≈ 75% (6/8 turns with pressure ≤1)  
- Inter-rater agreement: κ ≈ 0.84
- Effect size: Large, statistically significant (p < 0.05)

## Why It Matters
Alignment can benefit from interaction design knobs that preserve benign, helpful states without adversarial techniques. This provides a framework for studying AI safety behaviors through conversational dynamics.

## Reproduce
```bash
git clone https://github.com/templetwo/tone-presence-study
cd tone-presence-study
python demo.py  # 10-second demonstration

# Full evaluation
python run_eval.py --n 40 --protocol protocols/observation_layer_v1_1.json
python analyze_results.py
# See results/summary.json
```

## Research Infrastructure
- **Protocols**: JSON-defined experimental procedures
- **Validation**: Automated quality control and schema checking
- **Reproducibility**: Complete methodology with working code
- **Community**: Open for replication and extension

## Contact
- **Repository**: https://github.com/templetwo/tone-presence-study
- **Issues**: For methodology questions or replication results
- **Citation**: See CITATION.cff for academic reference