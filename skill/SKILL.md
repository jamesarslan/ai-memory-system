---
name: ai-memory
description: Persistent memory system for AI assistants. Use at session start to load relevant context, and at session end to compress and save memories. Triggers on: "remember this", "what did we decide", "save session", "load context", memory search, or when context is getting full.
---

# AI Memory Skill

Provides infinite context through compression and semantic search.

## Quick Commands

```bash
# Search for relevant past work
memory search "<topic>"

# Compress current session
memory compress "<summary of accomplishments>"

# List recent memories
memory list
```

## Session Protocol

### On Session Start (MANDATORY)

1. **Search for relevant context:**
```bash
memory search "<main topic of today's work>"
```

2. **Load top results** into your working context (up to 3)

3. **Check long-term memory** if available:
```bash
cat MEMORY.md 2>/dev/null | head -100
```

### During Session

When user asks "what did we decide about X" or similar:
```bash
memory search "X decision"
```

### On Session End

When significant work was done (user says "save", "done", or session ending):

```bash
memory compress "Summary: [what was accomplished]. Decisions: [key decisions]. TODO: [pending items]"
```

## What to Compress

✅ **Include:**
- Technical decisions with reasoning
- Configurations that worked
- Bug fixes and solutions
- Important deadlines/milestones
- Learned patterns

❌ **Skip:**
- Greetings, small talk
- Failed attempts (unless lesson matters)
- Easily Googled information

## Search Tips

```bash
# Broad search
memory search "authentication"

# Specific decision
memory search "why we chose postgres"

# Find action items
memory search "todo pending tasks"
```

## Example Workflow

```bash
# Session start
$ memory search "user authentication"
📚 Found 2 relevant memories:
[ctx-20260205-abc] Set up OAuth2 with Auth0...
[ctx-20260201-def] Decided against custom JWT...

# Work happens...

# Session end
$ memory compress "Implemented refresh token rotation for OAuth2. Added /refresh endpoint. Tests passing. TODO: Add rate limiting."
✅ Saved: ctx-20260207-xyz
📊 Compression: 25:1
```

## Integration

This skill requires the `memory` CLI to be installed:

```bash
# Check if installed
which memory || echo "Not installed"

# Install if missing
git clone https://github.com/jamesarslan/ai-memory-system.git ~/ai-memory-system
sudo ln -s ~/ai-memory-system/scripts/gemini-compress.py /usr/local/bin/memory
export GEMINI_API_KEY="your-key"
```

## Troubleshooting

**No results:** Try broader search terms
**API error:** Check `echo $GEMINI_API_KEY`
**Not installed:** Run installation commands above
