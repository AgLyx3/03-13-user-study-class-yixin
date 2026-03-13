---
name: interview-synthesizer
description: Use when synthesizing product user interviews, extracting insights from interview transcripts, identifying pain points and patterns across multiple interviews, or creating research reports from customer conversations.
---

# Interview Synthesizer

Synthesize customer and user interview transcripts into evidence-backed product insights.
This skill is best for first-pass clustering and synthesis. A researcher should still review the output before making decisions.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Core Workflow](#core-workflow)
- [Tools Reference](#tools-reference)
- [Synthesis Framework](#synthesis-framework)
- [Output Formats](#output-formats)
- [Common Pitfalls](#common-pitfalls)
- [Best Practices](#best-practices)

---

## Quick Start

### Analyze a Single Interview
```bash
python scripts/interview_synthesizer.py transcript.txt
```

### Analyze Multiple Interviews
```bash
python scripts/interview_synthesizer.py interviews/ --aggregate
```

### Export as JSON
```bash
python scripts/interview_synthesizer.py transcript.txt --json
```

### Generate Synthesis Report
```bash
python scripts/interview_synthesizer.py interviews/ --aggregate --report
```

---

## Core Workflow

```
Transcribe -> Analyze -> Cross-Reference -> Synthesize -> Prioritize -> Report
```

### Step 1: Prepare Transcripts
- One `.txt` file per interview
- Include participant metadata at top (role, segment, date) if available
- Clean up filler words only if they obscure meaning

### Step 2: Analyze Individual Interviews
```bash
python scripts/interview_synthesizer.py transcript.txt
```

Extracts per interview:
- Participant-only pain points with severity
- Solution signals and adoption concerns
- Workflow descriptions and current workarounds
- Evidence-backed findings grouped into research buckets
- Supporting quotes ranked by insight value
- Light tool mention detection

### Step 3: Cross-Reference Across Interviews
```bash
python scripts/interview_synthesizer.py interviews/ --aggregate
```

Aggregation produces:
- Cross-interview findings with evidence counts
- Solution signals grouped by type
- Strong patterns (3+ interviews) vs weaker signals
- Sentiment distribution across the cohort
- Tool mentions from participant responses

### Step 4: Synthesize into Insights

Use the `--report` flag to generate a PM-style synthesis:

| Section | Content |
|---------|---------|
| **Executive Summary** | Strong patterns, sentiment, participant count |
| **Key Findings** | Evidence-backed themes across interviews |
| **Weaker Signals** | Less-supported but notable themes |
| **Solution Signals** | What participants appear to want, grouped by type |
| **Tools Mentioned** | Existing tools named by participants |
| **Recommended Next Steps** | Follow-up research actions |
| **Limitations** | Heuristic and sample caveats |

### Step 5: Prioritize Findings

The tool prioritizes findings by:
- **Cross-interview support**: How many interviews contain the theme
- **Evidence density**: How many supporting snippets were captured
- **Research usefulness**: Whether the finding implies a meaningful next question

---

## Tools Reference

### Interview Synthesizer Script

**Capabilities:**
- Speaker-aware transcript parsing
- Participant-first evidence extraction
- Pain point extraction with severity assessment
- Solution signal identification
- Workflow and workaround identification
- Research-bucket clustering for stronger findings
- Multi-interview aggregation with evidence counts
- Structured PM-style report generation

**Commands:**
```bash
# Single interview analysis
python scripts/interview_synthesizer.py transcript.txt

# JSON output
python scripts/interview_synthesizer.py transcript.txt --json

# Analyze directory of transcripts
python scripts/interview_synthesizer.py interviews/ --aggregate

# Full synthesis report
python scripts/interview_synthesizer.py interviews/ --aggregate --report

# Filter by severity
python scripts/interview_synthesizer.py transcript.txt --min-severity medium
```

---

## Synthesis Framework

### Pain Point Severity Assessment

| Severity | Indicators | Example Language |
|----------|-----------|-----------------|
| **High** | very, extremely, really, totally, completely, absolutely | "This is extremely frustrating" |
| **Medium** | Default when pain indicator present without modifier | "It's a bit of a problem" |
| **Low** | somewhat, bit, little, slightly, minor | "It's slightly annoying" |

### Solution Signal Classification

| Type | Indicators |
|------|-----------|
| **clarity** | visible, clearer, lightweight, less chaotic |
| **workflow_fit** | inside the chat, same place we already talk |
| **trust** | accurate, trust, outdated, guessed wrong |
| **general** | Default |

---

## Output Formats

### Text Report (default)
Human-readable synthesis with findings, evidence, implications, and next steps.

### JSON (`--json`)
Machine-readable output for integration with other tools:
```json
{
  "pain_points": [{"quote": "...", "indicator": "...", "severity": "high"}],
  "feature_requests": [{"quote": "...", "type": "new_feature", "priority": "high"}],
  "sentiment_score": {"score": 0.25, "label": "positive"},
  "key_themes": ["coordination_visibility_gap", "chat_buries_decisions"],
  "quotes": ["..."],
  "workflows": [{"quote": "...", "type": "current_process"}],
  "competitors_mentioned": ["Notion"],
  "findings": [{"theme": "...", "evidence_count": 4, "implication": "..."}]
}
```

### Aggregated Report (`--aggregate --report`)
Cross-interview synthesis with:
- Strong patterns supported by multiple interviews
- Weaker signals worth follow-up
- Solution signals and tool mentions
- Limitations and next-step recommendations

---

## Common Pitfalls

| Pitfall | Description | Prevention |
|---------|-------------|------------|
| **Cherry-Picking Quotes** | Selecting quotes that confirm existing hypotheses | Use cross-interview support, not isolated quotes |
| **Ignoring Outliers** | Dismissing insights from 1-2 participants | Flag unique insights separately; they may signal emerging needs |
| **Conflating Requests with Needs** | Taking feature requests at face value | Map requests back to underlying pain points and JTBD |
| **Recency Bias** | Over-weighting the last interview analyzed | Always aggregate before drawing conclusions |
| **Using Interviewer Prompts as Evidence** | Mistaking the interviewer’s framing for the participant’s needs | Analyze participant turns separately |
| **Sentiment Oversimplification** | Reducing nuanced feedback to positive/negative | Treat sentiment as weak signal only |

---

## Best Practices

**Interview Preparation:**
- Use semi-structured format (consistent questions, flexible follow-ups)
- Focus on past behavior, not future intentions
- Ask "why" five times to find root cause
- Avoid leading questions ("Wouldn't you love if...")

**Transcript Quality:**
- Include speaker labels (Interviewer/Participant)
- Note non-verbal cues [laughs], [sighs], [long pause]
- Preserve exact wording for pain points and feature requests
- Add participant metadata header (role, company size, segment)

**Synthesis Quality:**
- Minimum 5 interviews before drawing patterns
- 3+ mentions = pattern worth investigating
- Always pair quantitative signals with verbatim quotes
- Separate observation from interpretation
- Cross-reference with quantitative data (analytics, surveys) when available
- Treat the script output as a first-pass synthesis, not the final readout

**Sharing Results:**
- Lead with top 3 actionable insights
- Include direct quotes as evidence
- Show frequency data alongside qualitative findings
- Make recommendations specific and testable
