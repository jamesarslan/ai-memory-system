# Memory Systems Comparison

Detailed comparison of AI memory solutions.

---

## Quick Decision Matrix

| Need | Best Choice |
|------|-------------|
| CLI-based workflow (Claude Code, Codex, Aider) | **This System** |
| Complex autonomous agents | MemGPT/Letta |
| Document search over large corpus | RAG |
| LangChain application | LangChain Memory |
| Production SaaS with hosting | Zep or Mem0 |
| Personal assistant | Mem0 |

---

## Detailed Comparison

### This System (AI Memory System)

**Approach:** LLM compression + vector embeddings for search

**Architecture:**
```
Conversation → Gemini Flash (compress) → Structured JSON
                                              ↓
                                    Gemini Embeddings (index)
                                              ↓
                                    Semantic Search (retrieve)
```

**Pros:**
- Works with ANY AI CLI (not framework-specific)
- Free API tier (Gemini: 2M tokens/day)
- Simple: one Python file, no servers
- Portable: plain JSON files
- Privacy: runs locally
- Excellent compression (20:1 to 100:1)

**Cons:**
- Manual trigger (not autonomous)
- Single-user focused
- No built-in deduplication

**Best for:** Individual developers using CLI-based AI assistants

---

### MemGPT / Letta

**Approach:** Hierarchical memory with self-editing capabilities

**Architecture:**
```
Agent ← → Core Memory (editable by agent)
      ← → Archival Memory (vector store)
      ← → Recall Memory (conversation buffer)
```

**Pros:**
- Autonomous memory management
- Agent can edit its own memory
- Sophisticated retrieval
- Research-backed approach

**Cons:**
- Complex setup and configuration
- High token consumption (memory management overhead)
- Requires understanding of memory architecture
- Can be unpredictable

**Best for:** Research, complex autonomous agents, power users

**Links:** 
- https://github.com/cpacker/MemGPT
- https://www.letta.com/

---

### RAG (Retrieval-Augmented Generation)

**Approach:** Chunk documents → embed → retrieve relevant chunks

**Architecture:**
```
Documents → Chunking → Embeddings → Vector DB
                                        ↓
Query → Embed → Similarity Search → Retrieved Chunks → LLM
```

**Pros:**
- Scales to large document collections
- Well-understood, many implementations
- Good for factual lookup

**Cons:**
- No compression (retrieves raw chunks)
- Chunk boundaries lose context
- Retrieval noise (irrelevant chunks)
- Doesn't preserve decisions/actions

**Best for:** Document Q&A, knowledge bases, enterprise search

**Implementations:** LangChain, LlamaIndex, Haystack

---

### LangChain Memory

**Approach:** Conversation buffer with optional summarization

**Types:**
- `ConversationBufferMemory` — Store everything
- `ConversationSummaryMemory` — Summarize old messages
- `ConversationBufferWindowMemory` — Keep last N messages
- `VectorStoreRetrieverMemory` — Vector-based retrieval

**Pros:**
- Easy integration with LangChain
- Multiple memory types
- Active development

**Cons:**
- Python/LangChain only
- Framework lock-in
- Not CLI-friendly
- Summary memory can lose details

**Best for:** LangChain-based applications

**Links:** https://python.langchain.com/docs/modules/memory/

---

### Zep

**Approach:** Session-based memory with fact extraction

**Architecture:**
```
Messages → Zep Server → Session Memory
                     → Extracted Facts
                     → Vector Search
```

**Pros:**
- Hosted option (managed)
- Automatic fact extraction
- Multiple sessions support
- Production-ready

**Cons:**
- Requires server (self-hosted or cloud)
- Additional infrastructure
- Cost for hosted option

**Best for:** Production SaaS applications needing memory

**Links:** https://github.com/getzep/zep

---

### Mem0

**Approach:** Personal memory layer with learning

**Architecture:**
```
Conversations → Mem0 → User Memory Graph
                    → Learned Preferences
                    → Contextual Retrieval
```

**Pros:**
- User-centric (learns about person)
- Pattern recognition
- Nice API
- Hosted option

**Cons:**
- Early stage
- Primarily hosted
- Less control over storage

**Best for:** Personal assistants that learn user preferences

**Links:** https://github.com/mem0ai/mem0

---

## Feature Comparison Table

| Feature | This System | MemGPT | RAG | LangChain | Zep | Mem0 |
|---------|-------------|--------|-----|-----------|-----|------|
| Compression | ✅ 20-100x | ❌ | ❌ | ⚠️ Summary | ⚠️ | ⚠️ |
| Semantic Search | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Structured Extraction | ✅ | ⚠️ | ❌ | ❌ | ✅ | ✅ |
| Autonomous | ❌ | ✅ | ❌ | ⚠️ | ⚠️ | ✅ |
| CLI-friendly | ✅ | ⚠️ | ❌ | ❌ | ❌ | ❌ |
| Self-hosted | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| Free tier | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Multi-user | ❌ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ |
| Setup complexity | Low | High | Medium | Medium | Medium | Low |

---

## When to Use What

### Use This System When:
- ✅ You use Claude Code, Codex, Aider, Cursor, or similar CLIs
- ✅ You want simple, portable memory
- ✅ Cost is a concern (free Gemini API)
- ✅ You prefer files over databases
- ✅ You want full control and privacy

### Use MemGPT When:
- ✅ Building complex autonomous agents
- ✅ Agent should manage its own memory
- ✅ Research or experimental projects
- ✅ You understand the complexity tradeoffs

### Use RAG When:
- ✅ Searching large document collections
- ✅ FAQ or knowledge base applications
- ✅ Factual lookup is primary use case
- ✅ Already have vector DB infrastructure

### Use LangChain Memory When:
- ✅ Building with LangChain framework
- ✅ Python application
- ✅ Need quick integration
- ✅ Standard conversation memory is enough

### Use Zep When:
- ✅ Production SaaS application
- ✅ Multiple users/sessions
- ✅ Need managed hosting option
- ✅ Automatic fact extraction is valuable

### Use Mem0 When:
- ✅ Personal assistant use case
- ✅ Learning user preferences matters
- ✅ Want hosted solution
- ✅ Building consumer-facing product

---

## Cost Comparison

| System | API Cost | Infrastructure |
|--------|----------|----------------|
| This System | Free (Gemini) | None |
| MemGPT | Model API | Moderate |
| RAG | Embedding API | Vector DB |
| LangChain | Model API | Varies |
| Zep | Free/Paid tiers | Server |
| Mem0 | Paid tiers | Hosted |

---

## Migration Paths

### From RAG to This System
```bash
# Export your documents, compress each one
for doc in documents/*.txt; do
    memory compress "$doc"
done
```

### From This System to MemGPT
```python
# Export index.json, import as archival memory
import json
with open('~/memory/index/index.json') as f:
    index = json.load(f)
for entry in index['entries']:
    memgpt_agent.archival_memory.insert(entry['summary'])
```

### From LangChain to This System
```python
# Export conversation history, compress
from langchain.memory import ConversationBufferMemory
history = memory.load_memory_variables({})
# Save to file, then: memory compress history.txt
```

---

*Last updated: 2026-02-07*
