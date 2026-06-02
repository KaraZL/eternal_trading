"""In-memory storage for domain objects."""

from typing import Dict, List

# In-memory stores
clients: Dict[str, dict] = {}
books: Dict[str, dict] = {}
loans: Dict[str, dict] = {}
collateral_list: List[dict] = []


def generate_id(prefix: str, collection: Dict | List) -> str:
    """Generate a simple ID based on prefix and collection size."""
    if isinstance(collection, dict):
        count = len(collection) + 1
    else:
        count = len(collection) + 1
    return f"{prefix}_{count}"
