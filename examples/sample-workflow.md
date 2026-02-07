# Sample Workflow

## Example 1: End of Work Session

After a productive coding session:

```bash
# Compress the session
memory compress "Today we set up the authentication system using OAuth2. 
Decided to use Auth0 instead of building custom JWT handling. 
Created routes for /login, /callback, and /logout.
TODO: Add refresh token rotation.
James will review the PR tomorrow."
```

Output:
```
✅ Saved: ctx-20260207-a3f2c1
📝 Summary: Set up OAuth2 authentication using Auth0. Created login flow with callback and logout routes. Refresh token rotation pending.
🏷️  Keywords: oauth2, auth0, authentication, jwt, login, routes
📊 Compression: 15:1 (195 → 13 tokens)
```

## Example 2: Finding Past Work

```bash
# Search for authentication-related work
memory search "how did we set up login"
```

Output:
```
📚 Found 2 relevant memories:

[ctx-20260207-a3f2c1] (similarity: 0.8934)
  📝 Set up OAuth2 authentication using Auth0...
  🏷️  oauth2, auth0, authentication, jwt, login
  ⏰ 2026-02-07

[ctx-20260115-b2c4d5] (similarity: 0.7123)
  📝 Configured session management with Redis...
  🏷️  session, redis, cookies, security
  ⏰ 2026-01-15
```

## Example 3: Integrating with AI Assistant

In your AI assistant's system prompt or AGENTS.md:

```markdown
## Memory Protocol

### On Session Start
1. Run: `memory search "<today's main topic>"`
2. Load top 3 results into context
3. Reference past decisions when relevant

### On Session End
If significant work was done:
1. Summarize key accomplishments
2. Run: `memory compress "<summary>"`
3. Note any pending action items

### Keywords to Remember
When compressing, include:
- Project names
- Technology choices
- People involved
- Deadlines mentioned
```

## Example 4: Batch Compression

Compress multiple conversation logs:

```bash
# Compress all transcript files
for file in transcripts/*.txt; do
    echo "Processing: $file"
    memory compress "$file"
done
```

## Example 5: Export for Review

```bash
# List all memories as JSON
cat ~/memory/index/index.json | jq '.entries[-10:]'

# Find high-importance items
cat ~/memory/index/index.json | jq '.entries | map(select(.importance == "high"))'

# Get all action items
cat ~/memory/index/index.json | jq '.entries | map(.action_items) | flatten | unique'
```
