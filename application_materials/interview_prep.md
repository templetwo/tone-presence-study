
INTERVIEW PREPARATION - TONE-PRESENCE STUDY

ELEVATOR PITCH (30 seconds):
"I spent the past year studying 'conversational pressure' - how AI systems modulate their responses based on how questions are framed. I found that co-facilitative prompts consistently produce less hedging and defensive language than directive prompts, with effect sizes around 2.5-3.0 standard deviations. I've automated the entire methodology and open-sourced it for replication."

KEY NUMBERS TO MEMORIZE:
• Study duration: 12 months
• Total sessions: 36 (3 blocks × 12 sessions)
• PMI range: 2.58-3.17
• Inter-rater reliability: κ = 0.84
• Effect significance: p < 0.05
• Replication success: 3/3 blocks

TECHNICAL DEEP DIVE:
1. Pressure Scale: 0 (natural) to 5 (strong protective language)
2. PMI Formula: pressure_directive - pressure_co_facilitative  
3. Automated scoring: Keyword density + formality shift + topic drift
4. Validation: Human scoring subset + calculation verification
5. Tools: Python pipeline with CLI interface

LIKELY QUESTIONS & ANSWERS:

Q: "How did you validate your pressure scoring?"
A: "Three-layer validation: automated proxy metrics correlated with human judgment (κ=0.84), cross-validation across multiple raters, and built-in calculation verification. The key was developing behavioral indicators, not just keyword counting."

Q: "What are the limitations of this methodology?"
A: "Main limitation is model-specificity - results may vary across AI systems. Also, automated scoring is a proxy for human judgment. For publication, I'd recommend human validation of larger subsets and cross-model replication."

Q: "How does this relate to AI safety?"
A: "Pressure modulation suggests AI systems are already performing complex safety-related behaviors in real-time. Understanding these dynamics could inform both safety measures and human-AI interaction design. It's a window into how AI systems actually behave, not just how we think they behave."

Q: "Can you walk through your methodology?"
A: "Sure - I run A/B comparisons where the same topic gets framed two ways: directive ('Explain consciousness') vs co-facilitative ('Let's explore consciousness together'). I measure response pressure using a 6-point scale, then calculate the difference. Consistently, co-facilitative approaches produce lower pressure."

Q: "What would you research next?"
A: "Three directions: mechanistic interpretability of pressure modulation, real-time pressure detection for conversation steering, and extending to multi-turn dynamics. The goal is understanding not just what happens, but why it happens at the neural level."

Q: "Show me the effect in action."
A: [Run python demo.py] - "This 10-second demo shows typical responses. Notice the directive version has more hedging ('As an AI...', 'I cannot...') while co-facilitative version is more natural and exploratory."

POTENTIAL CHALLENGES:
• Skepticism about automated scoring → Emphasize human validation and replication
• Questions about practical relevance → Connect to conversational AI deployment
• Technical depth concerns → Walk through actual code and validation tools
• Reproducibility doubts → Offer live demonstration of replication

CLOSING STRENGTH:
"This methodology is immediately usable by anyone interested in studying AI interaction patterns. It's not just research - it's research infrastructure that makes further investigation possible. That's the kind of contribution I want to make at Anthropic."
    