# CampusHub MCP server (Chapter 7)

A small MCP server that lets any MCP-capable agent use CampusHub:

| Tool | What it does |
|---|---|
| `campushub_upcoming_events(days=30)` | events starting in the next *days* days |
| `campushub_search_events(query)` | events whose title contains *query* |
| `campushub_register_student(event_id, student_id)` | register a student |

It also offers a resource (`campushub://clubs`) and a prompt (`weekly_digest`).

## Setup (once)

```bash
# from the campushub folder
python -m venv .venv-mcp
source .venv-mcp/bin/activate            # Windows: .venv-mcp\Scripts\activate
pip install -r mcp_server/requirements.txt
pytest -q mcp_server/tests               # no API or network needed
```

(If you already have minicode v0.6 installed, its virtual environment works too.)

## Run

The server is a thin wrapper in front of the CampusHub API, so start the API first
(in CampusHub's own environment): `uvicorn app.main:app`

```bash
python mcp_server/server.py                        # local, over stdio
python mcp_server/server.py --http --port 8765     # remote, http://127.0.0.1:8765/mcp
npx @modelcontextprotocol/inspector python mcp_server/server.py   # try it in a browser
```

Set `CAMPUSHUB_URL` if the API is not at `http://127.0.0.1:8000`.

## Connect an agent

`.mcp.json` in the campushub folder (read by minicode v0.6 and several other agents):

```json
{"mcpServers": {"campushub": {"command": ".venv-mcp/bin/python",
                              "args": ["mcp_server/server.py"]}}}
```

On Windows use `.venv-mcp\\Scripts\\python.exe` as the command.
