# ⚡ Quickstart

Get up and running in 60 seconds.

---

## 1. Get API Key (Free)

👉 [Google AI Studio](https://aistudio.google.com/app/apikey) — Click "Create API Key"

---

## 2. Install

```bash
git clone https://github.com/jamesarslan/ai-memory-system.git
cd ai-memory-system
export GEMINI_API_KEY="paste-your-key-here"
sudo ln -s $(pwd)/scripts/gemini-compress.py /usr/local/bin/memory
```

---

## 3. Use

```bash
# Save a memory
memory compress "We chose PostgreSQL over MySQL because of better JSON support."

# Find past memories
memory search "database decision"

# List recent memories  
memory list
```

---

## 4. Integrate with Your AI CLI

Add to your `CLAUDE.md` / `AGENTS.md`:

```markdown
## Memory Protocol

Session Start:
  memory search "<current topic>"

Session End (if significant work done):
  memory compress "<what was accomplished>"
```

---

## Done! 🎉

Your AI assistant now remembers across sessions.

**Full docs:** [README.md](README.md)
