# Labs for *The Modern Software Developer*

Each folder holds the code for one chapter's hands-on lab.

| Folder | Chapter | What you do |
|---|---|---|
| `ch02/` | 2 — LLMs Through a Software Engineer's Eyes | Call models through an API, count tokens, measure variance, latency and cost, and let a model call the CampusHub API |

## Setup (once)

```bash
pip install -r labs/requirements-labs.txt
```

All labs talk to models through the **OpenAI-compatible API**, which most providers and
local runtimes support. Set three environment variables:

| Variable | Example (cloud) | Example (free, local with Ollama) |
|---|---|---|
| `LLM_BASE_URL` | `https://api.openai.com/v1` | `http://localhost:11434/v1` |
| `LLM_API_KEY` | your secret key | `ollama` (any text) |
| `LLM_MODEL` | a model name from your provider | `qwen2.5-coder:7b` |

Never commit API keys. Put them in a `.env` file (already ignored by Git) or set them in
your terminal session.
