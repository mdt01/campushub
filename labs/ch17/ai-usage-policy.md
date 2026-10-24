# CampusHub team: AI usage policy (template for Lab 17)

Owner: ______________   Last reviewed: ______________   Review every: 3 months

## 1. Approved tools and models
- Coding agents: ______________ (versions/settings managed centrally)
- Models: only through the team gateway (`LLM_BASE_URL=...`). No personal API keys
  for project work.
- MCP servers: only those listed in `.mcp.json` / the team portal. New ones need a
  security review (Chapter 14, "lethal trifecta" question).

## 2. Data
- Never paste into any AI tool: production data, personal data of students,
  secrets, keys, tokens, or anything marked confidential.
- Allowed: this repository's code, public documentation, synthetic test data.
- Our provider settings: data is / is not used for training: __________;
  data stored in region: __________.

## 3. Using agents
- Agents run with `.agents/permissions.json`; nobody switches to `--mode auto`
  outside a sandbox.
- Background agents and loops open draft PRs only; they never merge.
- Budgets per team are set in the gateway; raising one needs the owner's approval.

## 4. Responsibility and review
- You are responsible for every line you merge, whoever or whatever wrote it.
- Every PR states how AI was used (PR template) and includes verification evidence.
- At least one human approval on every PR; two for security-sensitive code.

## 5. Learning and sharing
- Share useful prompts, skills and agent-file lines in `#ai-guild` / the team wiki.
- Report agent mistakes as issues labelled `agent-feedback` so we can fix the
  agent files, tests or loops that allowed them.

## 6. Exceptions and incidents
- Exceptions: ask the owner in writing; record them here.
- A leaked secret or data incident: rotate first, then report to ______ within 1 hour.
