"""Estimate the cost of model calls from token counts.

Prices change often: always copy current prices from your provider's pricing page.
They are expressed per million tokens.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Price:
    input_per_million: float    # e.g. in rupees or dollars
    output_per_million: float


def estimate_cost(input_tokens: int, output_tokens: int, price: Price) -> float:
    """Cost of one call = input part + output part."""
    return (input_tokens * price.input_per_million + output_tokens * price.output_per_million) / 1_000_000


if __name__ == "__main__":
    example = Price(input_per_million=250.0, output_per_million=1000.0)   # illustrative only
    # An agent session that read 2.4M tokens and wrote 60k tokens:
    print(f"Estimated session cost: {estimate_cost(2_400_000, 60_000, example):.2f}")
