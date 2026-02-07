# AI Memory System 🧠

**Infinite context for AI assistants using semantic compression and retrieval.**

Turn any AI CLI (Claude Code, Codex, Cursor, Aider, OpenClaw) into something that actually *remembers* — across sessions, topics, and time.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Gemini API](https://img.shields.io/badge/API-Gemini-4285F4.svg)](https://ai.google.dev/)

---

## 🚀 30-Second Jumpstart

```bash
# 1. Clone
git clone https://github.com/jamesarslan/ai-memory-system.git
cd ai-memory-system

# 2. Set API key (free from Google AI Studio)
export GEMINI_API_KEY="your-key-here"

# 3. Add to path
sudo ln -s $(pwd)/scripts/gemini-compress.py /usr/local/bin/memory

# 4. Use it
memory compress "We decided to use PostgreSQL instead of MySQL for the project."
memory search "database choice"
```

**That's it.** Your AI assistant now has persistent memory.

---

## 📖 Table of Contents

- [The Problem](#the-problem)
- [The Solution](#the-solution)
- [Comparison with Other Systems](#-comparison-with-other-memory-systems)
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
1. **Compression** — Summarize conversations into searchable memories (20:1 to 100:1 ratio)
2. **Semantic Search** — Find relevant memories even with different wording
3. **Structured Extraction** — Keywords, topics, decisions, and action items
4. **Three-Layer Architecture** — Daily logs → Compressed index → Long-term knowledge

---

## 🔄 Comparison with Other Memory Systems

| System | Approach | Pros | Cons | Best For |
|--------|----------|------|------|----------|
| **This System** | Compression + Embeddings | Simple, low cost, works offline, any AI CLI | Manual triggers | CLI users, cost-conscious |
| **MemGPT/Letta** | Hierarchical memory, self-editing | Autonomous, sophisticated | Complex setup, high token use | Research, complex agents |
| **RAG (Retrieval)** | Vector DB + chunking | Scales to large docs | No compression, retrieval noise | Document search |
| **LangChain Memory** | Conversation buffer/summary | Easy integration | Python-only, framework lock-in | LangChain apps |
| **Zep** | Session memory + facts | Hosted option, auto-extract | Requires server | Production apps |
| **Mem0** | Personal memory layer | User-centric, learns patterns | Early stage, hosted | Personal assistants |

### Why Choose This System?

| If You Need... | Use This Because... |
|----------------|---------------------|
| **Any AI CLI** | Works with Claude Code, Codex, Aider, Cursor, OpenClaw, Pi |
| **Low cost** | Gemini API is free (2M tokens/day) |
| **Simplicity** | One Python file, no servers, no frameworks |
| **Portability** | Plain JSON files, easy to backup/migrate |
| **Privacy** | Runs locally, your data stays yours |
| **Customization** | Fork and modify freely |

### Key Differentiators

```
Traditional RAG:
  Document → Chunks → Embeddings → Retrieve chunks
  Problem: Returns raw chunks, wastes context on irrelevant parts

This System:
  Conversation → Compress → Structured JSON → Embeddings → Retrieve summaries
  Benefit: 20-100x smaller, preserves decisions/actions, semantic search
```

---

## 🧩 Three-Layer Memory Architecture

The most effective memory system uses three complementary layers:

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
- Free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

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
memory --help
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

# Returns JSON-formatted results with similarity scores
```

### Output Format

Compression returns structured JSON:
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
memory list | grep "importance.*high"

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
- Gemini free tier: 2M tokens/day, 32k tokens/minute
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

MIT — Use freely, modify as needed.

---

## 🙏 Credits

Built for AI assistants that need to remember.

Inspired by the need for persistent memory across Claude Code, Codex, Cursor, Aider, and OpenClaw sessions.

---

**Star ⭐ if this helps your AI remember!**
