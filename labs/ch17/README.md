# Lab 17: gateway, routing and cost

| File | Use |
|---|---|
| `gateway.toml` | Configuration for `python -m minicode.gateway`: models, routes, team keys, budgets, cache |
| `ai-usage-policy.md` | A template for your team's AI-usage policy |

    python -m minicode.gateway --config labs/ch17/gateway.toml --port 8787
    # in another terminal, as a member of the events team:
    set LLM_BASE_URL=http://127.0.0.1:8787/v1      (macOS/Linux: export ...)
    set LLM_API_KEY=team-events-change-me
    set LLM_MODEL=auto
    set LLM_FEATURE=registration-window
    python -m minicode --workspace .
    # afterwards:
    python -m minicode.cost_report gateway-log.jsonl --html cost.html

The minicode gateway is a teaching tool. For real teams, compare it with an
open-source gateway such as LiteLLM's proxy server, or your cloud provider's gateway.
