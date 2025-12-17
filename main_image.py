# recipe_images_composite.py
import asyncio
from typing import Optional
from fastmcp import FastMCP, Client, Context

# Importer le serveur d'images existant
from image import mcp as pexels_mcp

# Serveur composite pour les images de recettes
main_mcp = FastMCP("recipe-images")

async def setup():
    # Importer statiquement le serveur Pexels
    await main_mcp.import_server(pexels_mcp, prefix="img")

@main_mcp.tool()
async def get_recipe_image(
    ctx: Context,
    recipe_name: str,
    per_page: int = 1,
) -> str:
    """
    Retourne une image Pexels pour un nom de recette donné.
    """
    # Appeler le tool de recherche d'images du serveur Pexels
    async with Client(pexels_mcp) as img_client:
        result = await img_client.call_tool(
            "search_images",
            arguments={"query": recipe_name, "per_page": per_page},
        )

    if not result.data or not result.data.get("images"):
        return f"Aucune image trouvée pour '{recipe_name}'."

    # Extraire les informations de la première image
    img = result.data["images"][0]
    url = img.get("url", "N/A")
    photographer = img.get("photographer", "Inconnu")

    return f"Image pour '{recipe_name}': {url} (Photographe: {photographer})"

if __name__ == "__main__":
    asyncio.run(setup())
    main_mcp.run()
