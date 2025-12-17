# pexels_mcp.py
import os
import httpx
from typing import List

from fastmcp import FastMCP, Context  # FastMCP server
from pydantic import BaseModel

# --- Config Pexels (à passer en env en prod) ---
PEXELS_API_KEY = os.getenv(
    "PEXELS_API_KEY",
    "QAd65CuvkjxUUBTvZnpsZu7VijaQSpY76yQkENd0GsORYWlbJqZse6ug",
)
if not PEXELS_API_KEY:
    raise RuntimeError("PEXELS_API_KEY non défini")

PEXELS_BASE_URL = "https://api.pexels.com/v1"

# --- Modèles de données (Pydantic) ---

class ImageResult(BaseModel):
    id: int
    url: str
    photographer: str
    alt: str

class SearchResponse(BaseModel):
    query: str
    total_results: int
    images: List[ImageResult]

# --- Serveur FastMCP ---

mcp = FastMCP('Pexels Image Search Service')

@mcp.tool()
async def search_images(
    ctx: Context,
    query: str,
    per_page: int = 5,
) -> SearchResponse:
    """
    Search images on Pexels by query.

    Args:
        query: Search keywords, e.g. "sunset beach".
        per_page: Number of images (1-20).
    """
    if not query:
        raise ValueError("query must not be empty")

    if per_page < 1 or per_page > 20:
        raise ValueError("per_page must be between 1 and 20")

    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page}

    async with httpx.AsyncClient(
        base_url=PEXELS_BASE_URL,
        headers=headers,
        timeout=10,
    ) as client:
        r = await client.get("/search", params=params)

    if r.status_code != 200:
        raise RuntimeError(f"Pexels error: {r.status_code} {r.text}")

    data = r.json()
    photos = data.get("photos", [])

    images = [
        ImageResult(
            id=p["id"],
            url=p["src"]["large"],
            photographer=p.get("photographer", ""),
            alt=p.get("alt", ""),
        )
        for p in photos
    ]

    return SearchResponse(
        query=query,
        total_results=data.get("total_results", len(images)),
        images=images,
    )

if __name__ == "__main__":
    # Démarre en mode MCP stdio (pour Claude Desktop, VS Code, MCPAgent…)
    mcp.run()
