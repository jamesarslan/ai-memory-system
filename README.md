# AI Memory System 🧠

**Infinite context for AI assistants using semantic compression and retrieval.**

Turn your AI assistant into something that actually *remembers* — across sessions, topics, and time.

## The Problem

AI assistants forget everything when a conversation ends. You explain the same things over and over. Context windows fill up and old information gets lost.

## The Solution

This system provides:
1. **Compression** — Summarize conversations into searchable memories using Gemini 3 Flash
2. **Semantic Search** — Find relevant memories even with different wording using embeddings
3. **Structured Storage** — Keywords, topics, decisions, and action items extracted automatically
4. **Three-Layer Architecture** — Daily logs → Compressed index → Long-term knowledge

## Quick Start

### 1. Get API Key

Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Install

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-memory-system.git
cd ai-memory-system

# Set your API key
export GEMINI_API_KEY="your-api-key-here"

# Or add to ~/.bashrc or .env file
echo 'export GEMINI_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Use It

```bash
# Compress a conversation
python3 scripts/gemini-compress.py compress "We discussed setting up Docker on the home server. Decided to use Portainer for management. James will install it tomorrow."

# Search your memories
python3 scripts/gemini-compress.py search "docker setup"

# List recent memories
python3 scripts/gemini-compress.py list
```

## Features

### Intelligent Compression

The system uses Gemini 3 Flash to extract:
- **Summary** — 2-3 sentence overview
- **Keywords** — Specific, searchable terms
- **Topics** — High-level categories
- **Decisions** — Key choices made
- **Action Items** — Pending tasks
- **Entities** — People, systems, dates mentioned

Example output:
```json
{
  "id": "ctx-20260207-abc123",
  "summary": "Set up Docker with Portainer on home server. Configured network bridge for container communication.",
  "keywords": ["docker", "portainer", "home-server", "networking", "containers"],
  "topics": ["infrastructure", "homelab"],
  "decisions": ["Use Portainer instead of CLI management"],
  "action_items": ["Configure automatic backups"],
  "importance": "medium"
}
```

### Semantic Search

Unlike keyword search, semantic search understands meaning:
- Query "container orchestration" → finds "Docker setup"
- Query "message queue" → finds "RabbitMQ configuration"
- Query "API testing" → finds "Postman collection setup"

### Compression Ratios

Typical results: **20:1 to 100:1** compression
- 15,000 token conversation → 150-750 token summary
- Preserves essential information while drastically reducing context size

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Your Conversation                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Gemini 3 Flash (Compression)                    │
│  • Extract summary, keywords, decisions                      │
│  • Identify entities and action items                        │
│  • Determine importance level                                │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Gemini Embeddings (Indexing)                    │
│  • Convert summary to vector                                 │
│  • Enable semantic similarity search                         │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Storage Layer                             │
│  memory/index/                                               │
│  ├── index.json          # Master index                      │
│  ├── embeddings/         # Vector embeddings                 │
│  ├── 2026-02-07.json     # Daily summaries                   │
│  └── topics/             # Topic-specific indexes            │
└─────────────────────────────────────────────────────────────┘
```

## Three-Layer Memory System

For best results, combine this with a broader memory architecture:

### Layer 1: Daily Logs
Raw notes of what happened each day.
```
memory/
├── 2026-02-06.md
├── 2026-02-07.md
└── ...
```

### Layer 2: Compressed Index (This System)
Searchable, structured summaries.
```
memory/index/
├── index.json
├── embeddings/
└── 2026-02-07.json
```

### Layer 3: Long-Term Knowledge
Curated, persistent information (manually maintained).
```
MEMORY.md          # Key facts, preferences, patterns
AGENTS.md          # Instructions and behaviors
```

## Integration with AI Assistants

### With Claude/Clawdbot

Add to your `AGENTS.md`:
```markdown
## Session Start
Before any task, search memory index for relevant context.
Load up to 3 most relevant summaries.

## Session End  
If significant work was done, compress the session:
\`\`\`bash
python3 ~/ai-memory-system/scripts/gemini-compress.py compress "$(cat session.txt)"
\`\`\`
```

### With Other Systems

The CLI works with any system that can run shell commands:
```bash
# Compress
echo "conversation text" | python3 gemini-compress.py compress

# Search (returns JSON)
python3 gemini-compress.py search "query" 2>/dev/null
```

## CLI Reference

### Compress
```bash
# From text
python3 gemini-compress.py compress "Your conversation text here"

# From file
python3 gemini-compress.py compress /path/to/transcript.txt

# From stdin
cat conversation.txt | python3 gemini-compress.py compress
```

### Search
```bash
# Basic search
python3 gemini-compress.py search "docker deployment"

# Returns top 5 most similar memories with similarity scores
```

### List
```bash
# Show recent memories
python3 gemini-compress.py list
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google AI API key | Yes |
| `MEMORY_INDEX_DIR` | Custom index path | No (default: `~/memory/index`) |

### Customize Index Path

Edit `gemini-compress.py`:
```python
INDEX_DIR = Path.home() / "your" / "custom" / "path"
```

## Best Practices

### When to Compress

- End of each significant work session
- After completing a major task
- When switching topics
- Before context window fills up

### What Makes Good Memories

✅ **Good:**
- Specific decisions and their reasoning
- Technical configurations that worked
- Names, dates, deadlines
- Action items and outcomes

❌ **Avoid:**
- Greetings and pleasantries
- Failed attempts (unless the lesson matters)
- Generic information easily found elsewhere

### Maintenance

```bash
# Monthly: Archive old embeddings
mv memory/index/embeddings/*.json ~/archive/memory/

# Quarterly: Review and prune index
# Remove outdated or irrelevant entries
```

## Troubleshooting

### "No results found"
- Check if index exists: `ls ~/memory/index/`
- Verify embeddings: `ls ~/memory/index/embeddings/`
- Try broader search terms

### API Errors
- Verify API key: `echo $GEMINI_API_KEY`
- Check rate limits (Gemini has generous free tier)
- Ensure network connectivity

### JSON Parse Errors
- Model occasionally returns malformed JSON
- Script includes fallback parsing
- Check logs for raw response

## License

MIT — Use freely, modify as needed.

## Contributing

PRs welcome! Areas for improvement:
- [ ] Support for additional embedding providers (OpenAI, Cohere)
- [ ] Web UI for browsing memories
- [ ] Automatic compression triggers
- [ ] Memory deduplication
- [ ] Topic clustering

---

Built for AI assistants that need to remember. 🧠
