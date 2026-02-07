# Compression Prompts

## Session Summary Prompt

```
You are a conversation summarizer. Given a conversation transcript, create a concise summary.

Output format:
SUMMARY: <2-3 sentence summary of what was accomplished>
KEYWORDS: <5-10 comma-separated keywords>
TOPICS: <1-3 high-level topic categories>
DECISIONS: <key decisions made, if any>
ACTION_ITEMS: <pending tasks, if any>

Focus on:
- What was accomplished
- Key technical details worth remembering
- Decisions and their reasoning
- Anything the user explicitly asked to remember

Ignore:
- Pleasantries and filler
- Failed attempts (unless the lesson is important)
- Routine operations that don't need recall
```

## Topic Extraction Prompt

```
Extract the main topics from this conversation. Return as JSON:
{
  "primary_topic": "main subject",
  "secondary_topics": ["related", "subjects"],
  "entities": ["people", "systems", "places mentioned"],
  "time_references": ["dates", "deadlines mentioned"]
}
```

## Relevance Scoring Prompt

```
Given a query and a list of summaries, score each summary's relevance (0-10).
Consider:
- Direct keyword matches (high weight)
- Semantic similarity (medium weight)  
- Temporal relevance (recent = higher)
- Entity overlap (names, systems)

Return: [{"id": "ctx-xxx", "score": 8, "reason": "direct match on keyword"}]
```

## Compression Quality Check

Before saving, verify:
- [ ] Summary captures main accomplishments
- [ ] Keywords are specific (not generic like "help", "work")
- [ ] No sensitive data in plain text (API keys, passwords)
- [ ] Compression ratio > 10:1
- [ ] Can understand summary without original context
