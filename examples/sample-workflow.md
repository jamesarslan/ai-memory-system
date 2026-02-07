# Sample Workflows

Practical examples for different use cases.

---

## 1. Daily Developer Workflow

### Morning: Session Start

```bash
# Load context for today's work
$ memory search "current sprint authentication"
📚 Found 3 relevant memories:

[ctx-20260206-abc] (similarity: 0.89)
  📝 Implemented OAuth2 login flow with Auth0...
  🏷️  oauth2, auth0, login, callback

[ctx-20260205-def] (similarity: 0.72)
  📝 Set up user database schema with roles...
  🏷️  database, schema, users, roles

# Check long-term memory
$ head -50 MEMORY.md
# Long-Term Memory
## Current Sprint: Authentication
- Using Auth0 for OAuth2
- PostgreSQL for user data
- Deadline: Feb 15
...
```

### During Work

```bash
# When you need past context
$ memory search "refresh token implementation"
📚 Found 1 relevant memory:
[ctx-20260204-xyz] Added refresh token handling...

# If topic shifts
$ memory search "deployment pipeline"
```

### Evening: Session End

```bash
# Compress today's work
$ memory compress "Completed refresh token rotation. Added /api/auth/refresh endpoint. Tests: 12 passed. Fixed race condition in token validation. TODO: Add rate limiting, update docs."

✅ Saved: ctx-20260207-ghi
📝 Summary: Completed refresh token rotation with new endpoint and tests...
🏷️  Keywords: refresh-token, auth, endpoint, tests, rate-limiting
📊 Compression: 35:1 (3500 → 100 tokens)

# Update daily log
$ echo "## 2026-02-07
- Completed refresh token rotation
- Fixed race condition in token validation
- TODO: rate limiting, docs" >> memory/2026-02-07.md
```

---

## 2. Project Handoff

### Export Project Memory

```bash
# Find all memories for a project
$ memory search "project alpha"
📚 Found 15 relevant memories...

# Export as documentation
$ cat ~/memory/index/index.json | jq '
  .entries 
  | map(select(.keywords | contains(["project-alpha"])))
  | .[] 
  | "## \(.timestamp[:10])\n\(.summary)\n\nDecisions: \(.decisions | join(", "))\n"
' > project-alpha-history.md
```

### Import Team Knowledge

```bash
# Compress team documentation
$ memory compress "$(cat team-guidelines.md)"
$ memory compress "$(cat architecture-decisions.md)"
$ memory compress "$(cat onboarding-notes.md)"
```

---

## 3. Code Review Context

### Before Review

```bash
# Load context about the feature
$ memory search "feature user-preferences"
📚 Found 2 relevant memories:

[ctx-20260201-abc] Designed user preferences schema...
  Decisions: Store in PostgreSQL, cache in Redis

[ctx-20260203-def] Implemented preferences API...
  Decisions: Use PATCH for updates, validate against schema
```

### After Review

```bash
# Save review feedback
$ memory compress "Code review for user-preferences PR #42. Feedback: add input validation, use transactions for batch updates, add pagination. James will address by Feb 10."
```

---

## 4. Debugging Session

### Search for Similar Issues

```bash
$ memory search "connection timeout database"
📚 Found 1 relevant memory:

[ctx-20260115-xyz] Fixed database connection timeouts...
  Summary: Issue was connection pool exhaustion. Fixed by increasing pool size and adding connection recycling.
  Keywords: database, timeout, connection-pool, postgres
```

### Save the Fix

```bash
$ memory compress "Fixed API timeout issue. Root cause: N+1 query in user list endpoint. Solution: Added eager loading with includes. Performance: 3s → 200ms. Added monitoring alert for slow queries."
```

---

## 5. Meeting Notes

### Compress Meeting Transcript

```bash
$ memory compress "Sprint planning meeting Feb 7. Attendees: James, Sarah, Mike. 
Decided: Prioritize auth features over dashboard. 
Assigned: James-OAuth, Sarah-Tests, Mike-Docs. 
Deadline: Feb 15.
Risks: Auth0 rate limits may need enterprise plan.
Next meeting: Feb 10 standup."

✅ Saved: ctx-20260207-mtg
📝 Summary: Sprint planning prioritized auth over dashboard...
🏷️  Keywords: sprint, planning, auth, oauth, deadline
📊 Compression: 20:1
```

---

## 6. Learning & Research

### Save Research Findings

```bash
$ memory compress "Research: Vector databases comparison.
Evaluated: Pinecone, Weaviate, pgvector, Milvus.
Decision: Use pgvector for simplicity (already have PostgreSQL).
Tradeoffs: Pinecone faster but adds complexity and cost.
Resources: https://github.com/pgvector/pgvector"
```

### Search Past Research

```bash
$ memory search "database comparison evaluation"
```

---

## 7. Automation Examples

### Git Hook: Post-Commit Compression

```bash
#!/bin/bash
# .git/hooks/post-commit

COMMIT_MSG=$(git log -1 --pretty=%B)
CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD | tr '\n' ', ')

memory compress "Commit: $COMMIT_MSG. Files: $CHANGED_FILES"
```

### Daily Summary Cron

```bash
# crontab -e
# 0 18 * * * ~/scripts/daily-memory-summary.sh

#!/bin/bash
# daily-memory-summary.sh

TODAY=$(date +%Y-%m-%d)
if [ -f "memory/$TODAY.md" ]; then
    memory compress "$(cat memory/$TODAY.md)"
fi
```

### Session Transcript Auto-Compress

```bash
#!/bin/bash
# auto-compress.sh - Run at end of AI session

if [ -f "/tmp/session-transcript.txt" ]; then
    memory compress "$(cat /tmp/session-transcript.txt)"
    rm /tmp/session-transcript.txt
fi
```

---

## 8. Multi-Project Setup

### Organize by Project

```bash
# Set different index per project
export MEMORY_INDEX_DIR=~/projects/alpha/memory/index
memory compress "Alpha project work..."

export MEMORY_INDEX_DIR=~/projects/beta/memory/index
memory compress "Beta project work..."
```

### Search Across Projects

```bash
# Create search alias
search_all() {
    for proj in ~/projects/*/memory/index; do
        echo "=== $(dirname $proj) ==="
        MEMORY_INDEX_DIR=$proj memory search "$1"
    done
}

search_all "database migration"
```

---

## 9. Team Memory

### Shared Knowledge Base

```bash
# Team members compress to shared location
export MEMORY_INDEX_DIR=/shared/team-memory/index

# Everyone can search team knowledge
memory search "onboarding new developer"
memory search "deployment checklist"
memory search "incident response"
```

### Personal + Team Search

```bash
# Search personal first, then team
search_both() {
    echo "=== Personal ==="
    MEMORY_INDEX_DIR=~/memory/index memory search "$1"
    echo "=== Team ==="
    MEMORY_INDEX_DIR=/shared/team-memory/index memory search "$1"
}
```

---

## 10. Maintenance Workflows

### Weekly Review

```bash
# List high-importance memories
$ cat ~/memory/index/index.json | jq '
  .entries 
  | map(select(.importance == "high"))
  | .[-5:]
  | .[] 
  | "\(.timestamp[:10]): \(.summary[:60])..."
'

# Check for pending action items
$ cat ~/memory/index/index.json | jq '
  [.entries[].action_items] | flatten | unique | .[]
'
```

### Monthly Archive

```bash
# Archive old embeddings (keep index for reference)
ARCHIVE_DATE=$(date -d "90 days ago" +%Y-%m-)
mkdir -p ~/memory/archive/$ARCHIVE_DATE
mv ~/memory/index/embeddings/ctx-$ARCHIVE_DATE* ~/memory/archive/$ARCHIVE_DATE/
```

### Quarterly Prune

```bash
# Review and remove outdated entries
# Export current index for review
cat ~/memory/index/index.json | jq '.entries | map({id, date: .timestamp[:10], summary: .summary[:50]})' > review.json

# After manual review, remove stale entries
# (Manual process - edit index.json, remove entries and their embedding files)
```

---

*Last updated: 2026-02-07*
