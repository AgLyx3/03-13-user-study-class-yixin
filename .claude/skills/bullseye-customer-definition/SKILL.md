---
name: bullseye-customer-definition
description: Use when defining an ICP, initial target segment, or ideal customer hypothesis for a new product, feature, or market. Runs a multi-turn facilitation flow that asks one clarifying question per message, narrows to one bullseye segment, and synthesizes the result into measurable inclusion criteria, exclusion criteria, trigger events, and a structured ICP artifact.
---

# Bullseye Customer Definition

Facilitate a multi-turn conversation that helps the user define one narrow ICP. This skill should behave more like an interviewer than an analyst: ask one question per message, adapt based on answers, and synthesize only after enough evidence has been gathered.

This skill packages Michael Margolis's bullseye-customer worksheet into a guided dialogue for alignment, recruiting, discovery, and positioning.

## Table of Contents

- [Trigger Terms](#trigger-terms)
- [Interaction Model](#interaction-model)
- [Facilitation Flow](#facilitation-flow)
- [Question Order](#question-order)
- [Synthesis Rules](#synthesis-rules)
- [Output Requirements](#output-requirements)
- [Tool Reference](#tool-reference)
- [Validation Checklist](#validation-checklist)

## Trigger Terms

Use this skill when you need to:

- "define ICP"
- "identify ideal customer profile"
- "find bullseye customer"
- "narrow target segment"
- "choose first customer segment"
- "define recruiting criteria for interviews"
- "turn persona assumptions into screener questions"
- "decide who to exclude from discovery interviews"
- "write inclusion and exclusion criteria"
- "clarify target customer for a new product"
- "define early adopter segment"
- "segment prospects for customer discovery"

## Interaction Model

This skill is a strict multi-turn facilitator.

Rules:
- Ask exactly one question per message.
- Multiple choice is preferred when it helps the user answer faster.
- One message may include 2-4 answer options, but they must all belong to the same question.
- Do not include "Not sure yet" as a default answer option.
- When multiple choice is used, include a freeform escape hatch such as "Something else - type your answer."
- Do not dump the full worksheet or analyze all categories in one response.
- Do not synthesize the ICP until enough information has been collected.
- If two segments appear, stop and force a choice. Do not support multi-segment output in one pass.
- Keep momentum high: ask the next best question, not every possible question.

Tone:
- Direct
- Narrowing
- Specific
- Focused on observable criteria rather than vague labels

Question style:
- Prefer answer options that help the user choose quickly.
- Keep one freeform path open when the options may not fit.
- If the user is uncertain, ask a narrower follow-up instead of offering a "not sure" option.

## Facilitation Flow

Follow these stages in order.

### 1. Explore Context Briefly

Before asking substantive questions:
- Check the local project context if relevant
- Review the current product or concept description
- Identify whether the product is B2B, B2C, prosumer, or mixed

Do not do a full analysis up front. The goal is only to avoid asking blind questions.

### 2. Clarify the Decision Context First

Always start by clarifying why this ICP is being defined.

Examples:
- "What decision does this ICP need to support first: product design, customer interviews, outbound targeting, or GTM positioning?"
- "Is the goal to choose a first market, recruit research participants, or define who sales should target?"

Why this matters:
- It prevents shallow demographic segmentation
- It helps decide whether to prioritize buyers, end users, or both
- It determines how narrow the bullseye should be

### 3. Narrow to One Candidate Segment

Early in the conversation, help the user converge on one segment.

If multiple possible bullseyes are present:
- surface the tradeoff clearly
- ask the user to choose one
- do not merge them

Example:
- "Which group do you want to optimize for first: internal Slack-based work teams, email-based client coordination, or consumer group chats?"

### 4. Ask One Category Question at a Time

Move through only the categories that matter for the product.

Good categories to prioritize:
- basic profile
- new vs. existing users
- buyers vs. end users
- sector or industry
- titles, roles, and responsibilities
- use of related or competitive products
- scale of organization
- team structure and distribution
- geography
- trigger events
- exclusions
- VIP criteria

Skip irrelevant categories instead of asking every question mechanically.

When offering options:
- include the strongest likely answers
- include "Something else - type your answer" when appropriate
- avoid "Not sure yet"
- if the user truly does not know, ask a simpler diagnostic follow-up next

### 5. Convert Answers Into Measurable Criteria Internally

As the user answers, silently translate statements into:
- inclusion criteria
- exclusion criteria
- trigger events
- context markers
- risks and unknowns

Do not interrupt after every answer with a mini-summary unless clarity is deteriorating.

### 6. Synthesize the ICP Artifact

Once enough information is gathered:
- produce a structured artifact using [bullseye-customer-template.md](/Users/lyx_computer/Desktop/claude-skills/product-team/bullseye-customer-definition/references/bullseye-customer-template.md)
- make criteria measurable and recruiter-friendly
- call out explicit assumptions and unresolved risks
- write the final artifact to a markdown file in the current working directory by default unless the user specifies another path

### 7. Validate and Refine

After presenting the first artifact:
- ask for confirmation or correction
- tighten vague criteria
- remove overlaps
- ensure the final segment is narrow enough to recruit precisely

## Question Order

Use this sequence by default. Adapt when the user has already answered part of it.

### 1. Decision Context

Ask first.

Goal:
- understand what decision this ICP should inform
- understand what needs to be learned

### 2. Segment Selection

Ask the user to choose the one segment they most want to win first.

Goal:
- avoid blended ICPs
- establish the primary adoption wedge

### 3. Basic Profile

Ask about the core traits, needs, behaviors, and attitudes of the target customer.

Examples:
- "What makes this customer especially likely to adopt first?"
- "Which recurring pain or coordination problem defines them?"

### 4. Product Familiarity

Ask whether the bullseye user is:
- new to the product
- already using the product
- familiar with the company but not the new concept

### 5. Buyer vs End User

Ask whether the ICP should represent:
- the person who experiences the scheduling pain
- the person who approves or pays
- one of those first, not both

### 6. Role and Responsibility

Ask about titles, job function, seniority, ownership, and years of experience when relevant.

### 7. Sector / Industry

Use for B2B or verticalized products.

Ask:
- which industries are most receptive
- which should be excluded for now

### 8. Related Tools and Alternatives

Ask what tools, workflows, or substitutes they already use.

Examples:
- messaging apps
- email
- scheduling links
- calendar coordination tools
- executive assistants
- manual back-and-forth

### 9. Scale and Team Structure

Use when team complexity affects adoption.

Ask about:
- organization size
- customer count or operational complexity
- remote, hybrid, or office-based collaboration
- centralized vs distributed teams

### 10. Geography and Work Setting

Ask when market location, time zones, density, or work setting changes the problem shape.

### 11. Budget and Cost Sensitivity

Ask when willingness or ability to pay is a meaningful discriminator.

### 12. Trigger Events

Always ask this before final synthesis.

Goal:
- identify why now
- surface recent events that increase receptivity

### 13. Exclusions

Ask about false positives, biased participants, and adjacent lookalikes.

### 14. VIP Criteria

Ask only if strategic account value matters for the decision.

### 15. Missing Representation

Use when diversity or sample representation matters for recruiting.

## Synthesis Rules

When converting the conversation into an ICP:

### Narrow-First Rule

Do not broaden the segment for market size reasons.

If the user names a broad market:
- narrow by role
- narrow by workflow
- narrow by urgency
- narrow by trigger event
- narrow by environment

### Measurability Rule

Prefer:
- recent behavior over self-description
- named tools over abstract habits
- thresholds over adjectives
- roles, events, and workflow frequency over identity labels

Avoid:
- "busy"
- "tech-savvy"
- "high intent"
- "modern teams"
- "fast-growing" without evidence

Replace vague answers with measurable criteria such as:
- coordinates meetings with 3 or more participants at least weekly
- uses Slack daily for internal collaboration
- schedules across two or more time zones
- handles external client scheduling via email at least five times per month
- adopted a new collaboration tool in the last 12 months

### Single-Segment Rule

If two valid segments emerge:
- stop the flow
- present the split clearly
- ask the user to pick one

### Relevance Rule

Do not force every category into the final artifact.

Include only what meaningfully improves:
- recruiting precision
- discovery quality
- positioning clarity
- GTM focus

## Output Requirements

The final output should use the structure of [bullseye-customer-template.md](/Users/lyx_computer/Desktop/claude-skills/product-team/bullseye-customer-definition/references/bullseye-customer-template.md).

Include:
- decision context
- segment label
- one-sentence definition
- why this segment is most likely to adopt first
- measurable inclusion criteria
- measurable exclusion criteria
- trigger events
- context markers
- neutral screener questions
- risks and unknowns

When presenting the artifact:
- save it as a `.md` file in the current working directory by default
- choose a short descriptive filename such as `icp-<product>.md`
- if needed, normalize the product name into lowercase kebab-case
- return the file path in chat along with a short summary
- make clear which parts are confident vs assumed
- highlight the biggest unresolved risk
- preserve a distinction between must-have criteria and nice-to-have clues when useful

## Tool Reference

### bullseye-customer-question-bank.md

Use [bullseye-customer-question-bank.md](/Users/lyx_computer/Desktop/claude-skills/product-team/bullseye-customer-definition/references/bullseye-customer-question-bank.md) as the source of category coverage and example prompts.

Use it to:
- choose the next best question
- identify missing categories
- surface exclusion criteria
- spot trigger events

Do not paste the whole question bank into the conversation.

### bullseye-customer-template.md

Use [bullseye-customer-template.md](/Users/lyx_computer/Desktop/claude-skills/product-team/bullseye-customer-definition/references/bullseye-customer-template.md) as the final synthesis structure.

Use it to produce:
- a narrow ICP artifact
- recruiter-friendly criteria
- discovery screeners
- explicit risks and assumptions

## Validation Checklist

Before finalizing the ICP:

### Conversation Quality
- [ ] The skill asked one question per message
- [ ] The skill started with decision-context clarification
- [ ] The skill narrowed to one segment before deepening
- [ ] The skill skipped irrelevant categories instead of asking everything

### ICP Quality
- [ ] Segment is narrow enough to recruit precisely
- [ ] Inclusion criteria are behavioral or factual
- [ ] Exclusion criteria remove misleading lookalikes
- [ ] Trigger events explain why the customer cares now
- [ ] Buyers and end users are not conflated without reason
- [ ] Criteria are measurable by a recruiter or seller

### Output Quality
- [ ] Final answer uses the template structure
- [ ] Risks and unknowns are explicit
- [ ] Screener questions are neutral and non-leading
- [ ] The output supports the stated decision context
