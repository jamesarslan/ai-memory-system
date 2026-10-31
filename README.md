# AI Memory System 🧠

**Long-term memory for AI assistants: conversation compression and semantic retrieval using the Gemini API.**

Stores and searches memories that AI CLIs can use across sessions, by calling a shell command (examples: Claude Code, Codex, Cursor, Aider, OpenClaw).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Gemini API](https://img.shields.io/badge/API-Gemini-4285F4.svg)](https://ai.google.dev/)

> **Status: experimental prototype.** Interfaces and the on-disk format may change. This is a personal tool, not a production service, and it has not been security-reviewed.

> **Model update required before use.** `COMPRESS_MODEL` in `scripts/gemini-compress.py` is set to `gemini-2.0-flash`. Google's [deprecations page](https://ai.google.dev/gemini-api/docs/deprecations) lists that model with a June 1, 2026 shutdown date. Change `COMPRESS_MODEL` to a currently supported Gemini model before running the tool (the deprecations page lists `gemini-3.6-flash` as the replacement).

> **Privacy.** Text you compress, and every search query, is sent to Google's Gemini API. Only the stored index (JSON and embedding files) stays on your machine. The tool does not work offline.

---

## 🚀 30-Second Jumpstart

```bash
# 1. Clone
git clone https://github.com/jamesarslan/ai-memory-system.git
cd ai-memory-system

# 2. Set API key (create one in Google AI Studio)
export GEMINI_API_KEY="your-key-here"

# 3. Add to path
sudo ln -s $(pwd)/scripts/gemini-compress.py /usr/local/bin/memory

# 4. Use it
memory compress "We decided to use PostgreSQL instead of MySQL for the project."
memory search "database choice"
```

**That's it.** Your AI assistant can now save and search memories.

---

## 📖 Table of Contents

- [The Problem](#the-problem)
- [The Solution](#the-solution)
- [Three-Layer Memory Architecture](#-three-layer-memory-architecture)
- [Quick Start Guide](#-quick-start-guide)
- [Integration with AI CLIs](#-integration-with-ai-clis)
- [CLI Reference](#-cli-reference)
- [Configuration](#-configuration)
- [Best Practices](#-best-practices)
- [As a Skill (for OpenClaw/Codex)](#-as-a-skill)

---

## The Problem

AI assistants forget everything when a conversation ends:
- 😤 You explain the same things over and over
- 📉 Context windows fill up and old information gets lost
- 🔄 No continuity between sessions
- ❓ "What did we decide about X?" — starts from scratch

## The Solution

This system provides:
1. **Compression** — Summarize conversations into searchable memories. The `compression_ratio` field is a rough word-count estimate, not a measured token count.
2. **Semantic Search** — Find relevant memories even with different wording
3. **Structured Extraction** — Keywords, topics, decisions, and action items
4. **Three-Layer Convention** — Daily logs → Compressed index → Long-term knowledge (the script implements only the compressed index)

---

## 🔄 What It Does and Where Data Goes

- **Integration:** a single Python script driven by shell commands, so it can be called from any AI CLI that can run shell commands. See [Integration with AI CLIs](#-integration-with-ai-clis).
- **Gemini API calls:** compression uses `generateContent` and embeddings use `embedContent`. Conversation text you compress (truncated to the first 50,000 characters) and search queries are sent to Google. Nothing is processed offline.
- **Local storage:** entries and embeddings are written as JSON files under `MEMORY_INDEX_DIR` (default `~/memory/index`).
- **Search:** brute-force cosine similarity over all stored embedding files. This suits a personal memory store, not a large document collection.
- **Cost and limits:** Gemini API usage is metered. See [Google's current pricing and rate limits](https://ai.google.dev/gemini-api/docs/pricing).
- **Other memory approaches:** this project does not benchmark itself against other memory systems. Compare the tools for your own use case.

### How It Works

```
Conversation → generateContent (structured JSON summary) → embedContent (summary + keywords) → JSON files on disk → cosine-similarity search
```

---

## 🧩 Three-Layer Memory Architecture

A practical memory setup uses three complementary layers. The script implements only Layer 2; Layers 1 and 3 are Markdown files you maintain yourself.

```
┌─────────────────────────────────────────────────────────────┐
│                    Layer 3: LONG-TERM                       │
│                                                             │
│  MEMORY.md — Curated facts, patterns, preferences           │
│  ├── Key decisions and their reasoning                      │
│  ├── Learned patterns ("user prefers X over Y")             │
│  └── Important relationships and context                    │
│                                                             │
│  Updated: Weekly or when significant insights emerge        │
│  Format: Human-readable markdown                            │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ Promote important insights
                          │
┌─────────────────────────────────────────────────────────────┐
│                    Layer 2: COMPRESSED INDEX                │
│                    (★ This System ★)                        │
│                                                             │
│  memory/index/                                              │
│  ├── index.json        — Master index of all memories       │
│  ├── embeddings/       — Vector embeddings for search       │
│  └── 2026-02-07.json   — Daily compressed summaries         │
│                                                             │
│  Updated: End of each work session                          │
│  Format: Structured JSON with semantic embeddings           │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ Compress significant sessions
                          │
┌─────────────────────────────────────────────────────────────┐
│                    Layer 1: DAILY LOGS                      │
│                                                             │
│  memory/                                                    │
│  ├── 2026-02-06.md    — Raw notes from Feb 6                │
│  ├── 2026-02-07.md    — Raw notes from Feb 7                │
│  └── session-start.md — Quick context for new sessions      │
│                                                             │
│  Updated: Continuously during sessions                      │
│  Format: Freeform markdown                                  │
└─────────────────────────────────────────────────────────────┘
```

### How Layers Work Together

```
Session Start:
  1. Load MEMORY.md (Layer 3) — big picture context
  2. Search index (Layer 2) — find relevant past work
  3. Read today's log (Layer 1) — recent raw notes

During Session:
  1. Append to daily log (Layer 1) — capture raw events
  2. AI uses context from all layers

Session End:
  1. Compress session → index (Layer 2)
  2. Update MEMORY.md if significant (Layer 3)
```

### Layer Templates

<details>
<summary><strong>MEMORY.md Template (Layer 3)</strong></summary>

```markdown
# Long-Term Memory

## About the User
- Name: [Name]
- Role: [Job/Role]
- Preferences: [Key preferences]

## Key Decisions
- 2026-02-07: Chose PostgreSQL over MySQL for [reason]
- 2026-01-15: Adopted TypeScript for all new projects

## Patterns & Preferences
- Prefers concise responses over verbose explanations
- Uses Docker for all deployments
- Testing: Jest for unit, Playwright for E2E

## Important Context
- Project X deadline: March 15
- Team members: [names]
- Tech stack: [stack]

## Learned Lessons
- Always run migrations in transactions
- Check disk space before large imports

---
*Last updated: 2026-02-07*
```
</details>

<details>
<summary><strong>Daily Log Template (Layer 1)</strong></summary>

```markdown
# 2026-02-07 — Daily Notes

## Morning
- Reviewed PR #42 for authentication changes
- Found bug in token refresh logic

## Afternoon
- Fixed token refresh, deployed to staging
- Met with team about Q2 roadmap

## Decisions
- Will use Redis for session caching (faster than DB)

## TODO
- [ ] Write tests for token refresh
- [ ] Update documentation
```
</details>

---

## 📦 Quick Start Guide

### Prerequisites
- Python 3.8+
- Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Installation

**Option 1: Quick Install (Recommended)**
```bash
# Clone and setup
git clone https://github.com/jamesarslan/ai-memory-system.git
cd ai-memory-system
./setup.sh
```

**Option 2: Manual Install**
```bash
# Clone
git clone https://github.com/jamesarslan/ai-memory-system.git
cd ai-memory-system

# Install dependency
pip install requests

# Set API key
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc

# Add to path (choose one)
sudo ln -s $(pwd)/scripts/gemini-compress.py /usr/local/bin/memory
# OR
echo 'alias memory="python3 ~/ai-memory-system/scripts/gemini-compress.py"' >> ~/.bashrc
```

### Verify Installation
```bash
memory                    # prints usage
memory compress "Test memory: The setup is working correctly."
memory search "setup"
```

---

## 🤖 Integration with AI CLIs

### Claude Code / Codex / Cursor

Add to your `CLAUDE.md` or project instructions:

```markdown
## Memory Protocol

### Session Start (MANDATORY)
Before starting work, load relevant context:
\`\`\`bash
memory search "<today's main topic or project name>"
\`\`\`
Load top 3 results into your working context.

### Session End
If significant work was done, compress the session:
\`\`\`bash
memory compress "Summary of what was accomplished today..."
\`\`\`

### When to Compress
- ✅ Completed a feature or task
- ✅ Made important decisions
- ✅ Learned something new about the codebase
- ✅ Before context window fills up
- ❌ Casual conversation or failed attempts
```

### OpenClaw / Clawdbot

Add to your `AGENTS.md`:

```markdown
## Memory System

Use the three-layer memory system:

### On Session Start
1. Read `MEMORY.md` for long-term context
2. Run `memory search "<topic>"` for relevant past work
3. Check `memory/YYYY-MM-DD.md` for recent notes

### During Session
- Log significant events to `memory/YYYY-MM-DD.md`
- Use `memory search` when you need past context

### On Session End (when user says "save")
1. Run `memory compress "What was accomplished..."`
2. Update `MEMORY.md` if significant insights emerged
3. Note pending tasks in daily log
```

### Aider

Add to `.aider.conf.yml`:
```yaml
# Load memory context at start
auto-commits: false
map-tokens: 1024

# In your workflow:
# Before: aider --message "$(memory search 'current task' | head -20)"
# After: memory compress "$(git log -1 --pretty=%B)"
```

### Generic Integration

Any AI CLI that can run shell commands:
```bash
# Pre-session: Load context
CONTEXT=$(memory search "project topic" 2>/dev/null | head -50)
echo "$CONTEXT" >> session_context.txt

# Post-session: Save memory
memory compress "$(cat session_transcript.txt)"
```

---

## 📚 CLI Reference

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `compress` | Compress text/file to memory | `memory compress "We decided..."` |
| `search` | Semantic search memories | `memory search "database setup"` |
| `list` | Show recent memories | `memory list` |

### Compress

```bash
# From text
memory compress "We set up Docker with Portainer for container management."

# From file
memory compress /path/to/transcript.txt

# From stdin
cat conversation.txt | memory compress

# With context
echo "Project: MyApp. We implemented OAuth2 using Auth0..." | memory compress
```

### Search

```bash
# Basic search
memory search "docker configuration"

# Specific topic
memory search "authentication setup decisions"

# Prints matching memories as plain text, with similarity scores
```

### Output Format

Each compressed memory is stored as a JSON entry in `index.json` (and in that day's file), for example:
```json
{
  "id": "ctx-20260207-abc123",
  "timestamp": "2026-02-07T14:30:00",
  "summary": "Set up Docker with Portainer for container management on home server.",
  "keywords": ["docker", "portainer", "containers", "home-server", "management"],
  "topics": ["infrastructure", "homelab"],
  "decisions": ["Use Portainer UI instead of CLI for container management"],
  "action_items": ["Configure automatic backups", "Set up monitoring"],
  "entities": {
    "people": ["James"],
    "systems": ["Docker", "Portainer", "Ubuntu"],
    "dates": ["tomorrow"]
  },
  "importance": "medium",
  "tokens_original": 1500,
  "tokens_compressed": 75,
  "compression_ratio": "20:1"
}
```

The `tokens_original`, `tokens_compressed` and `compression_ratio` fields are word-count estimates (words × 1.3), not tokenizer counts. The example values are illustrative, and the example is abridged: a stored entry also includes `source_session` and `model`. `memory compress` prints a short text summary rather than this JSON.

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google AI API key | *Required* |
| `MEMORY_INDEX_DIR` | Index storage path | `~/memory/index` |

### Custom Paths

Edit `gemini-compress.py` or set environment:
```bash
export MEMORY_INDEX_DIR="$HOME/.my-ai/memory"
```

### Index Structure

```
~/memory/index/
├── index.json           # Master index (all entries)
├── embeddings/          # Vector files for search
│   ├── ctx-20260207-abc123.json
│   └── ctx-20260207-def456.json
├── 2026-02-07.json      # Daily summaries
├── 2026-02-06.json
└── topics/              # Optional topic indexes
```

---

## 💡 Best Practices

### What to Compress

✅ **Good candidates:**
- Technical decisions with reasoning
- Configuration that worked
- Bug fixes and their solutions
- Project milestones
- Learned patterns
- Important deadlines

❌ **Skip these:**
- Greetings and small talk
- Failed attempts (unless the lesson matters)
- Information easily Googled
- Duplicate of recent memory

### Compression Timing

| Trigger | Action |
|---------|--------|
| End of work session | Compress accomplishments |
| Major decision made | Compress immediately |
| Before context fills | Compress and continue |
| Switching projects | Compress current, search new |

### Maintenance

```bash
# Weekly: Review and consolidate
grep '"importance": "high"' ~/memory/index/index.json

# Monthly: Archive old embeddings
find ~/memory/index/embeddings -mtime +90 -exec mv {} ~/archive/memory/ \;

# Quarterly: Prune outdated entries
# Review index.json, remove stale entries
```

---

## 🎯 As a Skill

For AI systems that support skills (OpenClaw, Codex with skills), install as a skill:

### Installation

```bash
# Copy to skills directory
cp -r skill/ ~/.openclaw/skills/ai-memory/

# Or for Codex
cp -r skill/ ~/.codex/skills/ai-memory/
```

### Skill Contents

See `skill/SKILL.md` for the complete skill definition that teaches AI assistants how to use this system effectively.

---

## 🔧 Troubleshooting

### "No results found"
```bash
# Check index exists
ls ~/memory/index/

# Verify embeddings
ls ~/memory/index/embeddings/

# Try broader terms
memory search "setup"  # instead of "docker container setup"
```

### API Errors
```bash
# Verify key
echo $GEMINI_API_KEY

# Test API
curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY"
```

### Rate Limits
- Check your quota and rate limits in [Google's current pricing documentation](https://ai.google.dev/gemini-api/docs/pricing)
- If hitting limits, add delay between compressions

---

## 🤝 Contributing

PRs welcome! Areas for improvement:
- [ ] Support for OpenAI/Cohere embeddings
- [ ] Web UI for browsing memories
- [ ] Automatic compression triggers
- [ ] Memory deduplication
- [ ] Topic clustering
- [ ] Export to different formats

---

## 📄 License

MIT. See [LICENSE](LICENSE) for the full text.

---

## 🙏 Credits

Built for AI assistants that need to remember.

Inspired by the need for persistent memory across Claude Code, Codex, Cursor, Aider, and OpenClaw sessions.

---

**Star ⭐ if this helps your AI remember!**
