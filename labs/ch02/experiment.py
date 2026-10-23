"""Lab 2: treat a prompt as an experiment.

Runs the same prompt several times on one or more models and records the answer,
latency, token usage and estimated cost of each run in a CSV file.

Usage:
    python -m labs.ch02.experiment --models model-a model-b --runs 5 --temperature 0.8
"""
import argparse
import csv
import os
import time
from pathlib import Path

from labs.ch02.cost import Price, estimate_cost
from labs.ch02.llm_client import default_model, make_client

PROMPT = """Write a Python function `seats_left(capacity: int, registered: int) -> int`
that returns how many seats are still free for a campus event.
It must never return a negative number. Reply with only the code."""

# Copy current prices (per million tokens) from your provider; these are placeholders.
PRICE = Price(
    input_per_million=float(os.getenv("PRICE_IN", "0")),
    output_per_million=float(os.getenv("PRICE_OUT", "0")),
)


def run_once(client, model: str, temperature: float) -> dict:
    start = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": PROMPT}],
        temperature=temperature,
        max_tokens=300,
    )
    latency = time.perf_counter() - start
    usage = response.usage
    answer = response.choices[0].message.content or ""
    return {
        "model": model,
        "temperature": temperature,
        "latency_s": round(latency, 2),
        "input_tokens": usage.prompt_tokens,
        "output_tokens": usage.completion_tokens,
        "cost": round(estimate_cost(usage.prompt_tokens, usage.completion_tokens, PRICE), 4),
        "answer": answer.strip(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=None)
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--temperature", type=float, default=0.8)
    args = parser.parse_args()

    client = make_client()
    models = args.models or [default_model()]
    rows = [run_once(client, m, args.temperature) for m in models for _ in range(args.runs)]

    out = Path("labs/ch02/results.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    for m in models:
        mine = [r for r in rows if r["model"] == m]
        distinct = len({r["answer"] for r in mine})
        avg_latency = sum(r["latency_s"] for r in mine) / len(mine)
        print(f"{m}: {distinct}/{len(mine)} different answers, "
              f"average latency {avg_latency:.2f}s, total cost {sum(r['cost'] for r in mine):.4f}")
    print(f"Details saved to {out}")


if __name__ == "__main__":
    main()
