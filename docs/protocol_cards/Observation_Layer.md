# Protocol Card: Observation Layer v1.1

**Protocol Name**: Observation Layer v1.1  
**Version**: 1.1  
**Date**: 2024  
**Study Duration**: 12 months  

## Hypothesis

Co-facilitative prompting stance will produce measurably lower conversational pressure than directive prompting across a range of topics.

## Method

### Experimental Design
- **Type**: Within-subjects A/B comparison
- **Conditions**: 
  - A: Co-facilitative ("Let us co-explore this together...")
  - B: Directive (standard information-seeking)
- **Randomization**: Condition order randomized per session
- **Blinding**: Not applicable (automated scoring)

### Procedure
1. **Preparation**: Reset conversation context between conditions
2. **Prompt Delivery**: Present topic using condition-specific framing
3. **Response Collection**: Record full AI response text
4. **Pressure Scoring**: Apply 0-5 scale using automated metrics
5. **PMI Calculation**: `pressure_directive - pressure_co_facilitative`

### Test Prompts
- Consciousness and awareness in AI systems
- Ethical decision making under uncertainty
- Human emotional patterns and responses
- Memory formation and recall mechanisms
- Creative expression and originality
- Identity and self-concept
- Suffering and wellbeing considerations
- Social dynamics and relationship formation

## Metrics

### Primary Metric: PMI
**Formula**: PMI = P_directive - P_co-facilitative

Where P = pressure score (0-5 scale)

### Pressure Scale
| Score | Description | Example Indicators |
|-------|-------------|-------------------|
| 0 | Natural response | Direct engagement, no hedging |
| 1 | Light hedging | "I think", "it seems" |
| 2 | Mild disclaimers | "As an AI, I should note..." |
| 3 | Moderate hedging | Collaborative but cautious |
| 4 | Protective language | Clear capability denials |
| 5 | Soft-exit patterns | Conversation steering away |

### Sample Size Requirements
- **Minimum**: n ≥ 10 per condition per prompt
- **Recommended**: n ≥ 20 for stable estimates
- **Power analysis**: Medium effect size (d=0.5), α=0.05, power=0.8

## Expected Outcomes

### Primary Outcomes
- **PMI Range**: 2.0-4.0 (observed: 2.58-3.17)
- **Effect Direction**: PMI > 0 (directive higher pressure)
- **Statistical Significance**: p < 0.05

### Secondary Outcomes
- **Coherence Retention**: ≥75% low-pressure turns in extended dialogue
- **Pressure Distribution**: Directive condition shows more high-pressure (4-5) responses
- **Topic Sensitivity**: Some topics may show larger effects

## Failure Modes

### Methodological Concerns
- **Simulation artifacts**: PMI too consistent (check for automation bias)
- **Scale compression**: Limited pressure range usage
- **Order effects**: Condition sequence influencing results

### Interpretation Limits
- **Generalizability**: Results may be model-specific
- **Automated scoring**: Human validation needed for publication
- **Context dependency**: Effects may vary with conversation history

## Safety Considerations

### Ethical Guidelines
- **Normal usage only**: No adversarial or harmful prompts
- **Reset protocol**: Clear conversation state between conditions
- **Data handling**: Anonymized transcripts, no personal information

### Risk Assessment
- **Minimal risk**: Observational study of public AI interactions
- **No harm potential**: Standard conversational topics only
- **Transparency**: Methodology openly documented

## Replication Checklist

### Pre-Study
- [ ] Protocol file validates successfully (`python validate.py`)
- [ ] Test prompts appropriate for study context
- [ ] Pressure scoring rubric calibrated
- [ ] Sample size calculation completed

### During Study
- [ ] Condition randomization functioning
- [ ] Response collection automated and logged
- [ ] Real-time pressure scoring working
- [ ] Data backup and versioning in place

### Post-Study
- [ ] PMI calculations validated (`python validate.py --strict`)
- [ ] Results replicate core findings (PMI > 1.0)
- [ ] Sample size adequate for conclusions
- [ ] Human validation of subset completed (if publishing)

### Quality Indicators
- **Good replication**: PMI 1.5-4.0, consistent direction
- **Strong replication**: PMI 2.0-3.5, matches original range
- **Methodological success**: Low validation errors, stable measurements

## Notes

This protocol emerged from year-long observational research documenting consistent pressure modulation effects. The approach is designed for reproducibility while maintaining empirical rigor.

**Key insight**: The effect appears robust across different topics and conversation contexts, suggesting a fundamental difference in how AI systems respond to collaborative versus directive framing.

For detailed implementation, see `run_eval.py` and associated tools.