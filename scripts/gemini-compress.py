#!/usr/bin/env python3
"""
Context Compression using Gemini 3 Flash + Gemini Embeddings
Enables infinite memory for AI assistants with semantic search capabilities.

Requirements:
- Python 3.8+
- requests library (pip install requests)
- GEMINI_API_KEY environment variable

Usage:
  python3 gemini-compress.py compress "conversation text"
  python3 gemini-compress.py compress /path/to/file.txt
  python3 gemini-compress.py search "query"
  python3 gemini-compress.py list
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path
import requests

# Configuration - customize these paths as needed
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
COMPRESS_MODEL = "gemini-2.0-flash"  # or "gemini-1.5-flash" for older API
EMBED_MODEL = "text-embedding-004"   # or "embedding-001"

# Default index directory - change to your preferred location
INDEX_DIR = Path(os.environ.get("MEMORY_INDEX_DIR", Path.home() / "memory" / "index"))


def ensure_dirs():
    """Create index directories if they don't exist."""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    (INDEX_DIR / "topics").mkdir(exist_ok=True)
    (INDEX_DIR / "embeddings").mkdir(exist_ok=True)


def generate_id():
    """Generate unique context ID."""
    now = datetime.now()
    hash_part = hashlib.md5(str(now.timestamp()).encode()).hexdigest()[:6]
    return f"ctx-{now.strftime('%Y%m%d')}-{hash_part}"


def call_gemini(prompt: str, model: str = COMPRESS_MODEL, max_tokens: int = 2000) -> dict:
    """Call Gemini generateContent API."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    url = f"{BASE_URL}/models/{model}:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": 0.2,  # Lower temp for factual compression
            "responseMimeType": "application/json"  # Force JSON output
        }
    }
    
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    response.raise_for_status()
    return response.json()


def get_embedding(text: str) -> list:
    """Get embedding vector using Gemini Embedding API."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    url = f"{BASE_URL}/models/{EMBED_MODEL}:embedContent?key={GEMINI_API_KEY}"
    
    payload = {
        "content": {"parts": [{"text": text}]},
        "taskType": "RETRIEVAL_DOCUMENT"  # Optimized for search
    }
    
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    response.raise_for_status()
    result = response.json()
    return result.get("embedding", {}).get("values", [])


def cosine_similarity(a: list, b: list) -> float:
    """Calculate cosine similarity between two vectors."""
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def compress_conversation(conversation: str) -> tuple:
    """Compress a conversation into structured summary with embedding."""
    
    # Truncate very long conversations to avoid token limits
    max_chars = 50000
    if len(conversation) > max_chars:
        conversation = conversation[:max_chars] + "\n...[truncated]"
    
    prompt = f"""Analyze this conversation and extract essential information for memory storage.

CONVERSATION:
{conversation}

Return a JSON object with these fields:
- summary: 2-3 sentence summary of accomplishments
- keywords: array of 5-10 specific keywords (not generic words)
- topics: array of 1-3 high-level categories
- decisions: array of key decisions made (empty array if none)
- action_items: array of pending tasks (empty array if none)
- entities: object with people (names), systems (tools/services), dates (deadlines)
- importance: "low", "medium", or "high"

Be concise and specific. Focus on actionable information."""

    result = call_gemini(prompt)
    
    # Extract response text
    try:
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        # Parse JSON from response (handle markdown code blocks)
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        data = json.loads(text.strip())
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Parse error: {e}", file=sys.stderr)
        print(f"Raw response: {text[:500]}...", file=sys.stderr)
        # Fallback parsing
        import re
        try:
            match = re.search(r'\{[^{}]*"summary"[^{}]*\}', text, re.DOTALL)
            if match:
                data = json.loads(match.group())
            else:
                raise ValueError("No JSON found")
        except:
            summary_match = re.search(r'"summary":\s*"([^"]+)"', text)
            summary = summary_match.group(1) if summary_match else text[:300]
            data = {
                "summary": summary,
                "keywords": [],
                "topics": ["general"],
                "decisions": [],
                "action_items": [],
                "entities": {"people": [], "systems": [], "dates": []},
                "importance": "medium"
            }
    
    # Generate embedding for semantic search
    embed_text = f"{data.get('summary', '')} {' '.join(data.get('keywords', []))}"
    embedding = get_embedding(embed_text)
    
    # Calculate token stats (rough estimate)
    original_tokens = len(conversation.split()) * 1.3
    compressed_tokens = len(data.get("summary", "").split()) * 1.3
    
    entry = {
        "id": generate_id(),
        "timestamp": datetime.now().isoformat(),
        "summary": data.get("summary", ""),
        "keywords": data.get("keywords", []),
        "topics": data.get("topics", []),
        "decisions": data.get("decisions", []),
        "action_items": data.get("action_items", []),
        "entities": data.get("entities", {}),
        "importance": data.get("importance", "medium"),
        "tokens_original": int(original_tokens),
        "tokens_compressed": int(compressed_tokens),
        "compression_ratio": f"{int(original_tokens / max(compressed_tokens, 1))}:1",
        "source_session": "main",
        "model": COMPRESS_MODEL
    }
    
    return entry, embedding


def save_entry(entry: dict, embedding: list) -> str:
    """Save entry to index and embedding to separate file."""
    ensure_dirs()
    
    # Load or create master index
    index_file = INDEX_DIR / "index.json"
    if index_file.exists():
        with open(index_file) as f:
            index = json.load(f)
    else:
        index = {"entries": [], "version": "2.0", "provider": "gemini"}
    
    # Add entry
    index["entries"].append(entry)
    index["last_updated"] = datetime.now().isoformat()
    
    # Save index
    with open(index_file, "w") as f:
        json.dump(index, f, indent=2)
    
    # Save embedding separately (for efficient vector search)
    embed_file = INDEX_DIR / "embeddings" / f"{entry['id']}.json"
    with open(embed_file, "w") as f:
        json.dump({"id": entry["id"], "embedding": embedding}, f)
    
    # Also save to daily file
    daily_file = INDEX_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.json"
    if daily_file.exists():
        with open(daily_file) as f:
            daily = json.load(f)
    else:
        daily = {"entries": []}
    daily["entries"].append(entry)
    with open(daily_file, "w") as f:
        json.dump(daily, f, indent=2)
    
    return entry["id"]


def search_memory(query: str, top_k: int = 5) -> list:
    """Semantic search using Gemini embeddings."""
    ensure_dirs()
    
    # Get query embedding
    query_embedding = get_embedding(query)
    
    # Load all embeddings and calculate similarities
    embed_dir = INDEX_DIR / "embeddings"
    if not embed_dir.exists():
        return []
    
    scores = []
    for embed_file in embed_dir.glob("*.json"):
        with open(embed_file) as f:
            data = json.load(f)
        
        similarity = cosine_similarity(query_embedding, data.get("embedding", []))
        scores.append((data["id"], similarity))
    
    # Sort by similarity
    scores.sort(key=lambda x: x[1], reverse=True)
    top_ids = [s[0] for s in scores[:top_k]]
    
    # Load full entries for top results
    index_file = INDEX_DIR / "index.json"
    if not index_file.exists():
        return []
    
    with open(index_file) as f:
        index = json.load(f)
    
    results = []
    for entry in index.get("entries", []):
        if entry["id"] in top_ids:
            # Add similarity score
            for id_, score in scores:
                if id_ == entry["id"]:
                    entry["similarity"] = round(score, 4)
                    break
            results.append(entry)
    
    # Sort results by similarity
    results.sort(key=lambda x: x.get("similarity", 0), reverse=True)
    return results


def main():
    """CLI interface."""
    if not GEMINI_API_KEY:
        print("Error: Set GEMINI_API_KEY environment variable", file=sys.stderr)
        print("  Get a free key at: https://aistudio.google.com/app/apikey", file=sys.stderr)
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("AI Memory System - Compress and search conversation memories")
        print()
        print("Usage:")
        print("  python3 gemini-compress.py compress <file_or_text>")
        print("  python3 gemini-compress.py search <query>")
        print("  python3 gemini-compress.py list")
        print()
        print("Examples:")
        print('  python3 gemini-compress.py compress "We set up Docker today..."')
        print('  python3 gemini-compress.py search "docker configuration"')
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "compress":
        # Read from file or stdin
        if len(sys.argv) > 2:
            path = sys.argv[2]
            if os.path.exists(path):
                with open(path) as f:
                    conversation = f.read()
            else:
                conversation = " ".join(sys.argv[2:])
        else:
            print("Reading from stdin...", file=sys.stderr)
            conversation = sys.stdin.read()
        
        if not conversation.strip():
            print("Error: No content to compress", file=sys.stderr)
            sys.exit(1)
        
        print("🧠 Compressing with Gemini...", file=sys.stderr)
        entry, embedding = compress_conversation(conversation)
        entry_id = save_entry(entry, embedding)
        
        print(f"\n✅ Saved: {entry_id}")
        print(f"📝 Summary: {entry['summary']}")
        print(f"🏷️  Keywords: {', '.join(entry['keywords'])}")
        print(f"📊 Compression: {entry['compression_ratio']} ({entry['tokens_original']} → {entry['tokens_compressed']} tokens)")
        
    elif action == "search":
        if len(sys.argv) < 3:
            print("Usage: gemini-compress.py search <query>", file=sys.stderr)
            sys.exit(1)
        
        query = " ".join(sys.argv[2:])
        print(f"🔍 Searching for: {query}", file=sys.stderr)
        
        results = search_memory(query)
        
        if not results:
            print("No results found.")
            print(f"Index directory: {INDEX_DIR}")
        else:
            print(f"\n📚 Found {len(results)} relevant memories:\n")
            for r in results:
                print(f"[{r['id']}] (similarity: {r.get('similarity', 'N/A')})")
                print(f"  📝 {r['summary']}")
                print(f"  🏷️  {', '.join(r['keywords'][:5])}")
                print(f"  ⏰ {r['timestamp'][:10]}")
                print()
    
    elif action == "list":
        index_file = INDEX_DIR / "index.json"
        if not index_file.exists():
            print("No memories indexed yet.")
            print(f"Index directory: {INDEX_DIR}")
            sys.exit(0)
        
        with open(index_file) as f:
            index = json.load(f)
        
        entries = index.get("entries", [])
        print(f"📚 {len(entries)} memories indexed")
        print(f"📁 Index: {INDEX_DIR}\n")
        
        for e in entries[-10:]:  # Last 10
            print(f"[{e['id']}] {e['summary'][:80]}...")
            print(f"  🏷️  {', '.join(e.get('keywords', [])[:5])}")
            print()
    
    else:
        print(f"Unknown action: {action}")
        print("Valid actions: compress, search, list")
        sys.exit(1)


if __name__ == "__main__":
    main()
