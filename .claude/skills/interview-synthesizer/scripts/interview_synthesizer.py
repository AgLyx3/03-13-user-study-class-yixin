#!/usr/bin/env python3
"""
Interview Synthesizer
Extracts evidence-backed insights from user interview transcripts.
Designed for first-pass research synthesis, not final judgment.
"""

import re
import os
import sys
import json
import argparse
from typing import Dict, List, Tuple
from collections import Counter, defaultdict


class InterviewAnalyzer:
    """Analyze interview transcripts with participant-first evidence extraction."""

    def __init__(self):
        self.speaker_pattern = re.compile(
            r'(?:\*\*)?(Interviewer|Student|Participant)(?:\*\*)?:\s*',
            re.IGNORECASE,
        )

        self.pain_indicators = [
            'frustrat', 'annoy', 'difficult', 'hard', 'confus', 'slow',
            'struggle', 'challeng', 'pain', 'waste', 'manual', 'repetitive',
            'tedious', 'time-consuming', 'complicated', 'complex', 'unclear',
            'broken', 'clunky', 'awful', 'terrible', 'horrible', 'hate',
            'workaround', 'hack', 'brittle', 'unreliable', 'inconsistent',
            'chaos', 'messy', 'buried', 'blocked', 'stale', 'uncertainty',
        ]

        self.delight_indicators = [
            'easy', 'simple', 'quick', 'helpful', 'useful', 'valuable',
            'clear', 'reliable', 'lightweight', 'accurate', 'visible',
        ]

        self.request_indicators = [
            'wish', 'hope', 'should', 'could', 'would help', 'suggest',
            'idea', 'what if', 'missing', 'lack', 'want something',
            'would want', 'it should', 'needs to', 'it could',
        ]

        self.workflow_indicators = [
            'we usually', 'what happens', 'we start', 'then', 'after that',
            'someone', 'group chat', 'shared doc', 'google doc', 'spreadsheet',
            'trello', 'notion', 'message', 'dm', 'directly', 'scrolling back',
        ]

        self.known_tools = {
            'trello', 'notion', 'slack', 'whatsapp', 'imessage',
            'groupme', 'google docs', 'google doc', 'email', 'spreadsheet',
        }

        self.research_buckets = [
            {
                'key': 'decision_confidence_gap',
                'label': 'People make visible decisions with low confidence',
                'keywords': [
                    'hard to tell', 'hard to know', 'low confidence',
                    'guessing', 'not fully convinced', 'not sure',
                    'uncertainty', 'trial and error', 'second-guessing',
                    'incomplete information', 'safer', 'risky', 'too risky',
                ],
                'implication': 'The problem is not just task completion; it is low-confidence decision-making.'
            },
            {
                'key': 'personalization_gap',
                'label': 'People struggle to map examples or advice to themselves',
                'keywords': [
                    'look like me', 'hair like mine', 'face shape', 'my face',
                    'my hair', 'applies to me', 'work on me', 'suit me',
                    'different hair', 'different texture', 'different person',
                    'map that onto themselves', 'personal and realistic',
                ],
                'implication': 'Users need help translating inspiration or advice into a personally relevant prediction.'
            },
            {
                'key': 'communication_translation_gap',
                'label': 'People struggle to translate intent into actionable language',
                'keywords': [
                    'explain', 'describe', 'vocabulary', 'the words',
                    'doesn’t mean anything', 'does not mean anything',
                    'same way', 'what i mean', 'from scratch',
                    'warnings', 'follow-up questions', 'translate all of that',
                ],
                'implication': 'Users need support turning fuzzy intent into clearer instructions or constraints.'
            },
            {
                'key': 'maintenance_routine_burden',
                'label': 'The outcome is tied to ongoing maintenance or routine burden',
                'keywords': [
                    'maintenance', 'routine', 'upkeep', 'products',
                    'style it', 'styling', 'recreate it', 'every morning',
                    'extra time', 'normal effort', 'work at home',
                    'high-maintenance', 'too much effort',
                ],
                'implication': 'The choice is not just the initial outcome; it includes the upkeep users must live with.'
            },
            {
                'key': 'trust_and_credibility_risk',
                'label': 'Trust depends on realism, specificity, and credibility',
                'keywords': [
                    'trust', 'fake', 'gimmicky', 'biased', 'upsell',
                    'specific', 'generic', 'accurate', 'reassuring',
                    'looked fake', 'don’t trust', 'do not trust',
                    'everyone’s hair is different', 'everyone says',
                ],
                'implication': 'Any solution in this space has to earn trust through realistic, specific, believable output.'
            },
            {
                'key': 'information_overload',
                'label': 'People are overwhelmed by fragmented or excessive advice',
                'keywords': [
                    'too much advice', 'too much information',
                    'overwhelming', 'million product recommendations',
                    'searching later', 'videos', 'reviews', 'threads',
                    'random articles', 'scrolling photos', 'search process',
                    'not enough confidence',
                ],
                'implication': 'The pain is not lack of content alone; it is the burden of filtering and applying it.'
            },
            {
                'key': 'current_workaround_patchwork',
                'label': 'People patch the problem with informal workarounds',
                'keywords': [
                    'screenshots', 'ask friends', 'ask my roommate',
                    'ask my sister', 'read reviews', 'pinterest',
                    'reddit', 'instagram', 'tiktok', 'save photos',
                    'google', 'more searching later',
                ],
                'implication': 'Users already assemble their own workaround stack, which signals both demand and fragmentation.'
            },
            {
                'key': 'adoption_fit',
                'label': 'Any solution will need to fit existing behavior and effort tolerance',
                'keywords': [
                    'practical', 'normal effort', 'easy to use',
                    'would help', 'feel safer', 'more confident',
                    'reactive', 'put it off', 'avoid bigger change',
                    'only works if', 'realistic',
                ],
                'implication': 'A promising concept must fit how people already decide and what effort they will actually sustain.'
            },
        ]

    def analyze_interview(self, text: str) -> Dict:
        turns = self._parse_turns(text)
        participant_turns = [t for t in turns if t['speaker'] == 'participant']
        participant_text = "\n".join(t['text'] for t in participant_turns)
        sentences = self._participant_sentences(participant_turns)

        pain_points = self._extract_pain_points(sentences)
        feature_requests = self._extract_requests(sentences)
        workflows = self._extract_workflows(sentences)
        competitors_mentioned = self._extract_competitors(participant_text)
        evidence_records = self._extract_bucketed_evidence(sentences)
        findings = self._synthesize_findings(evidence_records)

        return {
            'participant_turn_count': len(participant_turns),
            'pain_points': pain_points,
            'feature_requests': feature_requests,
            'sentiment_score': self._calculate_sentiment(participant_text.lower()),
            'key_themes': [finding['theme_key'] for finding in findings],
            'quotes': self._extract_key_quotes(sentences),
            'workflows': workflows,
            'competitors_mentioned': competitors_mentioned,
            'evidence_records': evidence_records,
            'findings': findings,
            'limitations': [
                'First-pass heuristic synthesis only; requires researcher review.',
                'Only participant turns are used as evidence for findings.',
            ],
        }

    def _parse_turns(self, text: str) -> List[Dict]:
        matches = list(self.speaker_pattern.finditer(text))
        if not matches:
            return [{'speaker': 'participant', 'text': text.strip()}] if text.strip() else []

        turns = []
        for idx, match in enumerate(matches):
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            raw_speaker = match.group(1).lower()
            speaker = 'interviewer' if raw_speaker == 'interviewer' else 'participant'
            chunk = text[start:end].strip()
            if not chunk:
                continue
            turns.append({'speaker': speaker, 'text': self._clean_chunk(chunk)})
        return turns

    def _clean_chunk(self, text: str) -> str:
        text = text.strip()
        text = re.sub(r'^\*+\s*', '', text)
        text = re.sub(r'\s*\*+$', '', text)
        text = re.sub(r'^["\']+|["\']+$', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _participant_sentences(self, turns: List[Dict]) -> List[str]:
        sentences = []
        for turn in turns:
            parts = re.split(r'(?<=[.!?])\s+', turn['text'])
            for part in parts:
                part = re.sub(r'^\*+\s*', '', part.strip())
                if len(part) >= 20:
                    sentences.append(part)
        return sentences

    def _extract_pain_points(self, sentences: List[str]) -> List[Dict]:
        pain_points = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for indicator in self.pain_indicators:
                if indicator in sentence_lower:
                    pain_points.append({
                        'quote': sentence,
                        'indicator': indicator,
                        'severity': self._assess_severity(sentence_lower),
                    })
                    break
        return pain_points[:12]

    def _extract_requests(self, sentences: List[str]) -> List[Dict]:
        requests = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if not any(indicator in sentence_lower for indicator in self.request_indicators):
                continue
            request_type = self._classify_request(sentence_lower)
            if request_type == 'general' and not self._looks_like_solution_desire(sentence_lower):
                continue
            requests.append({
                'quote': sentence,
                'type': request_type,
                'priority': self._assess_request_priority(sentence_lower),
            })
        return requests[:10]

    def _extract_workflows(self, sentences: List[str]) -> List[Dict]:
        workflows = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(indicator in sentence_lower for indicator in self.workflow_indicators):
                workflows.append({'quote': sentence, 'type': 'current_process'})
        return workflows[:10]

    def _extract_bucketed_evidence(self, sentences: List[str]) -> List[Dict]:
        evidence = []
        seen = set()
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for bucket in self.research_buckets:
                if any(keyword in sentence_lower for keyword in bucket['keywords']):
                    key = (bucket['key'], sentence_lower)
                    if key in seen:
                        continue
                    seen.add(key)
                    evidence.append({
                        'theme_key': bucket['key'],
                        'theme': bucket['label'],
                        'quote': sentence,
                        'severity': self._assess_severity(sentence_lower),
                        'implication': bucket['implication'],
                    })
        return evidence

    def _synthesize_findings(self, evidence_records: List[Dict]) -> List[Dict]:
        grouped = defaultdict(list)
        for record in evidence_records:
            grouped[record['theme_key']].append(record)

        findings = []
        for bucket in self.research_buckets:
            records = grouped.get(bucket['key'], [])
            if not records:
                continue
            representative = max(records, key=lambda r: self._severity_score(r['severity']))
            findings.append({
                'theme_key': bucket['key'],
                'theme': bucket['label'],
                'evidence_count': len(records),
                'representative_quote': representative['quote'],
                'implication': bucket['implication'],
            })

        findings.sort(key=lambda item: (-item['evidence_count'], item['theme']))
        return findings

    def _calculate_sentiment(self, text: str) -> Dict:
        positive_count = sum(1 for ind in self.delight_indicators if ind in text)
        negative_count = sum(1 for ind in self.pain_indicators if ind in text)
        total = positive_count + negative_count
        score = 0 if total == 0 else (positive_count - negative_count) / total

        if score > 0.25:
            label = 'positive'
        elif score < -0.25:
            label = 'negative'
        else:
            label = 'neutral'

        return {
            'score': round(score, 2),
            'label': label,
            'positive_signals': positive_count,
            'negative_signals': negative_count,
        }

    def _extract_key_quotes(self, sentences: List[str]) -> List[str]:
        scored = []
        for sentence in sentences:
            score = 0
            sl = sentence.lower()
            if any(ind in sl for ind in self.pain_indicators):
                score += 2
            if self._looks_like_solution_desire(sl):
                score += 2
            if 'because' in sl or 'so' in sl:
                score += 1
            if any(ind in sl for ind in self.workflow_indicators):
                score += 1
            if score > 0:
                scored.append((score, sentence))
        scored.sort(key=lambda item: (-item[0], item[1]))
        return [quote for _, quote in scored[:6]]

    def _extract_competitors(self, text: str) -> List[str]:
        text_lower = text.lower()
        found = []
        for tool in sorted(self.known_tools):
            if tool in text_lower:
                found.append(tool.title() if tool != 'imessage' else 'iMessage')
        return found

    def _looks_like_solution_desire(self, text: str) -> bool:
        return any(
            phrase in text for phrase in [
                'would help', 'want something', 'simple shared task board',
                'lightweight', 'clearer', 'visible', 'less chaotic',
                'inside the chat', 'same place we already talk',
            ]
        )

    def _classify_request(self, text: str) -> str:
        if any(w in text for w in ['inside the chat', 'group chat', 'same place we already talk']):
            return 'workflow_fit'
        if any(w in text for w in ['lightweight', 'simple', 'less chaotic', 'clearer', 'visible']):
            return 'clarity'
        if any(w in text for w in ['accurate', 'trust', 'guessed wrong', 'outdated']):
            return 'trust'
        return 'general'

    def _assess_request_priority(self, text: str) -> str:
        if any(w in text for w in ['need', 'have to', 'critical', 'blocking']):
            return 'high'
        if any(w in text for w in ['would help', 'want', 'should']):
            return 'medium'
        return 'low'

    def _assess_severity(self, text: str) -> str:
        if any(w in text for w in ['very', 'extremely', 'really', 'totally', 'completely', 'terrible', 'awful']):
            return 'high'
        if any(w in text for w in ['slightly', 'somewhat', 'a bit', 'minor']):
            return 'low'
        return 'medium'

    def _severity_score(self, severity: str) -> int:
        return {'low': 1, 'medium': 2, 'high': 3}.get(severity, 0)


def aggregate_interviews(interviews: List[Dict]) -> Dict:
    aggregated = {
        'total_interviews': len(interviews),
        'overall_sentiment': {'positive': 0, 'negative': 0, 'neutral': 0},
        'findings': [],
        'feature_requests': defaultdict(list),
        'pain_points': defaultdict(list),
        'workflows': [],
        'tools_mentioned': Counter(),
        'limitations': [
            'Heuristic first-pass synthesis; findings require researcher review.',
            'Cross-interview patterns are stronger than one-off comments.',
        ],
    }

    finding_map = defaultdict(list)

    for interview in interviews:
        sentiment = interview.get('sentiment_score', {}).get('label', 'neutral')
        aggregated['overall_sentiment'][sentiment] += 1

        seen_themes = set()
        for finding in interview.get('findings', []):
            finding_map[finding['theme_key']].append(finding)
            seen_themes.add(finding['theme_key'])

        for pain in interview.get('pain_points', []):
            aggregated['pain_points'][pain['indicator']].append(pain['quote'])

        for request in interview.get('feature_requests', []):
            aggregated['feature_requests'][request['type']].append(request['quote'])

        aggregated['workflows'].extend(interview.get('workflows', []))

        for tool in interview.get('competitors_mentioned', []):
            aggregated['tools_mentioned'][tool] += 1

    findings = []
    for theme_key, entries in finding_map.items():
        sample = entries[0]
        findings.append({
            'theme_key': theme_key,
            'theme': sample['theme'],
            'interview_count': len(entries),
            'total_evidence': sum(entry['evidence_count'] for entry in entries),
            'representative_quotes': [entry['representative_quote'] for entry in entries[:3]],
            'implication': sample['implication'],
        })

    findings.sort(key=lambda item: (-item['interview_count'], -item['total_evidence'], item['theme']))
    aggregated['findings'] = findings
    aggregated['feature_requests'] = dict(aggregated['feature_requests'])
    aggregated['pain_points'] = dict(aggregated['pain_points'])
    aggregated['tools_mentioned'] = dict(aggregated['tools_mentioned'])
    return aggregated


def format_single_analysis(analysis: Dict) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append("INTERVIEW ANALYSIS")
    lines.append("=" * 60)

    sentiment = analysis['sentiment_score']
    lines.append(f"\nSentiment: {sentiment['label'].upper()} (score: {sentiment['score']})")
    lines.append(f"Participant turns analyzed: {analysis['participant_turn_count']}")

    if analysis['findings']:
        lines.append("\n## KEY FINDINGS")
        for idx, finding in enumerate(analysis['findings'][:5], 1):
            lines.append(f"{idx}. {finding['theme']} ({finding['evidence_count']} evidence snippets)")
            lines.append(f"   Evidence: \"{finding['representative_quote'][:140]}\"")
            lines.append(f"   Implication: {finding['implication']}")

    if analysis['feature_requests']:
        lines.append("\n## SOLUTION SIGNALS")
        for request in analysis['feature_requests'][:5]:
            lines.append(f"- [{request['type']}] \"{request['quote'][:140]}\"")

    if analysis['workflows']:
        lines.append("\n## CURRENT WORKFLOWS")
        for workflow in analysis['workflows'][:4]:
            lines.append(f"- {workflow['quote'][:140]}")

    if analysis['quotes']:
        lines.append("\n## SUPPORTING QUOTES")
        for quote in analysis['quotes'][:4]:
            lines.append(f"- \"{quote}\"")

    if analysis['limitations']:
        lines.append("\n## LIMITATIONS")
        for limitation in analysis['limitations']:
            lines.append(f"- {limitation}")

    return "\n".join(lines)


def format_aggregate_report(aggregated: Dict) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append("INTERVIEW SYNTHESIS REPORT")
    lines.append(f"Total interviews analyzed: {aggregated['total_interviews']}")
    lines.append("=" * 60)

    sentiment = aggregated['overall_sentiment']
    lines.append("\n## EXECUTIVE SUMMARY")
    lines.append(
        f"- Sentiment distribution: {sentiment['positive']} positive, "
        f"{sentiment['neutral']} neutral, {sentiment['negative']} negative"
    )

    strong_findings = [finding for finding in aggregated['findings'] if finding['interview_count'] >= 3]
    weaker_findings = [finding for finding in aggregated['findings'] if finding['interview_count'] < 3]

    if strong_findings:
        lines.append("- Strong patterns (3+ interviews):")
        for finding in strong_findings[:5]:
            lines.append(
                f"  - {finding['theme']} "
                f"({finding['interview_count']}/{aggregated['total_interviews']} interviews)"
            )

    if strong_findings:
        lines.append("\n## KEY FINDINGS")
        for idx, finding in enumerate(strong_findings[:6], 1):
            lines.append(
                f"{idx}. {finding['theme']} "
                f"({finding['interview_count']} interviews, {finding['total_evidence']} evidence snippets)"
            )
            for quote in finding['representative_quotes'][:2]:
                lines.append(f"   - Evidence: \"{quote[:150]}\"")
            lines.append(f"   - Implication: {finding['implication']}")

    if weaker_findings:
        lines.append("\n## WEAKER SIGNALS")
        for finding in weaker_findings[:4]:
            lines.append(f"- {finding['theme']} ({finding['interview_count']} interview(s))")

    if aggregated['feature_requests']:
        lines.append("\n## SOLUTION SIGNALS")
        for req_type, quotes in sorted(aggregated['feature_requests'].items(), key=lambda item: len(item[1]), reverse=True):
            lines.append(f"- {req_type}: {len(quotes)} mention(s)")
            for quote in quotes[:2]:
                lines.append(f"  - \"{quote[:140]}\"")

    if aggregated['tools_mentioned']:
        lines.append("\n## TOOLS MENTIONED")
        for tool, count in sorted(aggregated['tools_mentioned'].items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"- {tool}: {count} interview(s)")

    lines.append("\n## RECOMMENDED NEXT STEPS")
    lines.append("- Validate whether the strongest pains are frequent enough to change behavior.")
    lines.append("- Test the highest-confidence assumptions with a narrower follow-up study or prototype.")
    lines.append("- Probe where current workarounds break down before solutioning further.")

    if aggregated['limitations']:
        lines.append("\n## LIMITATIONS")
        for limitation in aggregated['limitations']:
            lines.append(f"- {limitation}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Interview Synthesizer - Extract evidence-backed product insights from user interviews"
    )
    parser.add_argument("path", help="Path to interview transcript (.txt) or directory of transcripts")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--aggregate", action="store_true", help="Aggregate insights across multiple interviews")
    parser.add_argument("--report", action="store_true", help="Generate full synthesis report")
    parser.add_argument("--min-severity", choices=['low', 'medium', 'high'], help="Filter pain points by minimum severity")

    args = parser.parse_args()
    analyzer = InterviewAnalyzer()
    severity_order = {'low': 0, 'medium': 1, 'high': 2}

    if os.path.isdir(args.path):
        txt_files = sorted(
            os.path.join(args.path, filename)
            for filename in os.listdir(args.path)
            if filename.endswith('.txt')
        )
        if not txt_files:
            print(f"No .txt files found in {args.path}")
            sys.exit(1)

        print(f"Found {len(txt_files)} transcript(s) in {args.path}\n")
        all_analyses = []
        for filepath in txt_files:
            with open(filepath, 'r') as handle:
                text = handle.read()
            analysis = analyzer.analyze_interview(text)
            if args.min_severity:
                min_sev = severity_order[args.min_severity]
                analysis['pain_points'] = [
                    pain for pain in analysis['pain_points']
                    if severity_order.get(pain['severity'], 0) >= min_sev
                ]
            all_analyses.append(analysis)
            print(f"  Analyzed: {os.path.basename(filepath)}")

        if args.aggregate or args.report:
            aggregated = aggregate_interviews(all_analyses)
            if args.json:
                print(json.dumps(aggregated, indent=2, default=str))
            elif args.report:
                print("\n" + format_aggregate_report(aggregated))
            else:
                print(json.dumps(aggregated, indent=2, default=str))
        else:
            for filepath, analysis in zip(txt_files, all_analyses):
                print(f"\n--- {os.path.basename(filepath)} ---")
                if args.json:
                    print(json.dumps(analysis, indent=2))
                else:
                    print(format_single_analysis(analysis))
    elif os.path.isfile(args.path):
        with open(args.path, 'r') as handle:
            text = handle.read()
        analysis = analyzer.analyze_interview(text)
        if args.min_severity:
            min_sev = severity_order[args.min_severity]
            analysis['pain_points'] = [
                pain for pain in analysis['pain_points']
                if severity_order.get(pain['severity'], 0) >= min_sev
            ]
        if args.json:
            print(json.dumps(analysis, indent=2))
        else:
            print(format_single_analysis(analysis))
    else:
        print(f"Path not found: {args.path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
