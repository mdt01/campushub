"""Measure what a server's tool definitions cost:  python mcp_server/measure_tools.py

Prints the number of tools and the approximate tokens their definitions add to EVERY
request an agent sends (about four characters per token).
"""
import json
import sys
from pathlib import Path

import anyio
from mcp import Client

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mcp_server import naive_server, server  # noqa: E402


async def cost(mcp) -> tuple[int, int]:
    async with Client(mcp) as client:
        tools = (await client.list_tools()).tools
    definitions = [{"name": t.name, "description": t.description,
                    "parameters": t.input_schema} for t in tools]
    return len(tools), len(json.dumps(definitions)) // 4


async def main() -> None:
    for label, module in [("naive server", naive_server), ("designed server", server)]:
        count, tokens = await cost(module.mcp)
        print(f"{label:<16} {count:>3} tools  ~{tokens:>5,} tokens per request")


if __name__ == "__main__":
    anyio.run(main)
