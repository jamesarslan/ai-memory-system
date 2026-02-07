# Architecture Reference

Deep dive into the three-layer memory architecture.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           AI ASSISTANT                                   │
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                      │
│  │   Read      │  │   Search    │  │   Write     │                      │
│  │  Context    │  │   Memory    │  │   Memory    │                      │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                      │
└─────────┼────────────────┼────────────────┼─────────────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        MEMORY LAYERS                                     │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ LAYER 3: LONG-TERM KNOWLEDGE                                       │ │
│  │                                                                     │ │
│  │ MEMORY.md                   USER.md           AGENTS.md            │ │
│  │ ├── Key decisions           ├── Name          ├── Instructions     │ │
│  │ ├── Learned patterns        ├── Preferences   ├── Memory protocol  │ │
│  │ └── Important context       └── History       └── Behaviors        │ │
│  │                                                                     │ │
│  │ Format: Human-readable Markdown                                    │ │
│  │ Update: Weekly / on significant insights                           │ │
│  │ Size: 2-10 KB                                                      │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                              ▲                                           │
│                              │ Promote important insights                │
│                              │                                           │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ LAYER 2: COMPRESSED INDEX (This System)                           │ │
│  │                                                                     │ │
│  │ memory/index/                                                       │ │
│  │ ├── index.json          Master index of all memories               │ │
│  │ ├── embeddings/         Vector embeddings for semantic search      │ │
│  │ │   ├── ctx-20260207-abc.json                                      │ │
│  │ │   └── ctx-20260206-def.json                                      │ │
│  │ └── 2026-02-07.json     Daily compressed summaries                 │ │
│  │                                                                     │ │
│  │ Format: Structured JSON + Vector embeddings                        │ │
│  │ Update: End of each significant session                            │ │
│  │ Size: 50-500 KB (grows over time)                                  │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                              ▲                                           │
│                              │ Compress significant sessions             │
│                              │                                           │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ LAYER 1: DAILY LOGS                                                │ │
│  │                                                                     │ │
│  │ memory/                                                             │ │
│  │ ├── 2026-02-07.md       Today's raw notes                          │ │
│  │ ├── 2026-02-06.md       Yesterday's notes                          │ │
│  │ ├── session-start.md    Quick context for new sessions             │ │
│  │ └── heartbeat-state.json Periodic check tracking                   │ │
│  │                                                                     │ │
│  │ Format: Freeform Markdown                                          │ │
│  │ Update: Continuously during sessions                               │ │
│  │ Size: 1-5 KB per day                                               │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### Read Flow (Session Start)

```
Session Start
     │
     ├──▶ Read MEMORY.md (Layer 3)
     │    └── Load key facts, preferences, patterns (~2KB)
     │
     ├──▶ memory search "<topic>" (Layer 2)
     │    └── Semantic search, return top 3-5 matches (~1KB)
     │
     └──▶ Read memory/YYYY-MM-DD.md (Layer 1)
          └── Today's raw notes if any (~500B)

Total context: ~3-4KB (vs 50KB+ without compression)
```

### Write Flow (Session End)

```
Session End
     │
     ├──▶ memory compress "summary" (Layer 2)
     │    ├── Send to Gemini Flash → structured JSON
     │    ├── Generate embedding → vector file
     │    └── Append to index.json
     │
     ├──▶ Update memory/YYYY-MM-DD.md (Layer 1)
     │    └── Append raw events, TODOs
     │
     └──▶ (Optional) Update MEMORY.md (Layer 3)
          └── If significant insight, add to long-term

Session transcripts: 10-50KB
Compressed memory: 100-500 bytes
Compression ratio: 20:1 to 100:1
```

### Search Flow

```
Query: "database configuration"
     │
     ├──▶ Embed query via Gemini
     │
     ├──▶ Load all embeddings from memory/index/embeddings/
     │
     ├──▶ Calculate cosine similarity for each
     │
     ├──▶ Sort by similarity, take top K
     │
     └──▶ Return matching entries from index.json

Latency: ~500ms (embedding + search)
```

---

## Schema Reference

### Index Entry (Layer 2)

```json
{
  "id": "ctx-20260207-abc123",
  "timestamp": "2026-02-07T14:30:00.000Z",
  "summary": "Set up OAuth2 authentication using Auth0...",
  "keywords": ["oauth2", "auth0", "authentication", "jwt"],
  "topics": ["security", "infrastructure"],
  "decisions": ["Use Auth0 instead of custom JWT handling"],
  "action_items": ["Add refresh token rotation", "Write tests"],
  "entities": {
    "people": ["James", "Sarah"],
    "systems": ["Auth0", "Node.js", "Express"],
    "dates": ["March 15 deadline"]
  },
  "importance": "high",
  "tokens_original": 15000,
  "tokens_compressed": 150,
  "compression_ratio": "100:1",
  "source_session": "main",
  "model": "gemini-2.0-flash"
}
```

### Embedding Entry

```json
{
  "id": "ctx-20260207-abc123",
  "embedding": [0.023, -0.045, 0.012, ...]  // 768 dimensions
}
```

### Master Index

```json
{
  "version": "2.0",
  "provider": "gemini",
  "last_updated": "2026-02-07T14:30:00.000Z",
  "entries": [
    { /* entry 1 */ },
    { /* entry 2 */ }
  ]
}
```

---

## Layer Characteristics

| Layer | Format | Update Frequency | Retention | Search Method |
|-------|--------|------------------|-----------|---------------|
| 3 (Long-term) | Markdown | Weekly | Permanent | Text search |
| 2 (Index) | JSON + Vectors | Per session | 6-12 months | Semantic |
| 1 (Daily) | Markdown | Continuous | 30-90 days | Date-based |

---

## Integration Patterns

### Pattern 1: Full Stack (Recommended)

Use all three layers:

```markdown
## Session Start Protocol
1. Load MEMORY.md → big picture
2. memory search → relevant past work
3. Read today's daily log → recent context

## Session End Protocol
1. Update daily log → raw events
2. memory compress → structured memory
3. Update MEMORY.md → if significant
```

### Pattern 2: Index Only

Just use Layer 2:

```markdown
## Session Start
memory search "<topic>"

## Session End
memory compress "<summary>"
```

### Pattern 3: With Knowledge Graph

Add entity tracking (advanced):

```
areas/
├── people/
│   ├── james/
│   │   ├── summary.md
│   │   └── items.json
│   └── sarah/
├── projects/
│   └── auth-system/
└── systems/
    └── auth0/
```

---

## Scaling Considerations

### For Individual Use (Default)
- Single index.json file
- All embeddings in memory
- Sub-second search

### For Teams (Extended)
- Separate indexes per user
- Shared knowledge index
- Access controls on entries

### For Large History (1000+ entries)
- Partition by date/topic
- Use proper vector DB (pgvector, Pinecone)
- Archive old embeddings

---

## Backup & Migration

### Backup

```bash
# Backup entire memory system
tar -czf memory-backup-$(date +%Y%m%d).tar.gz \
    ~/memory/ \
    ~/MEMORY.md \
    ~/AGENTS.md
```

### Restore

```bash
tar -xzf memory-backup-20260207.tar.gz -C ~/
```

### Export to Other Formats

```bash
# To CSV
cat ~/memory/index/index.json | jq -r \
  '.entries[] | [.timestamp, .summary, (.keywords | join(","))] | @csv'

# To plain text
cat ~/memory/index/index.json | jq -r \
  '.entries[] | "[\(.timestamp)] \(.summary)\n"'
```

---

*Last updated: 2026-02-07*
