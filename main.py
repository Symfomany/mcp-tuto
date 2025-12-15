from __future__ import annotations

from typing import List, Optional, Dict
import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP
import asyncio


mcp = FastMCP("recipies")

# ---------
# RESOURCES (lecture seule)
# ---------
@mcp.resource("recipes://ingredients/default")
def default_ingredients() -> List[str]:
    """Liste d'ingrédients par défaut."""
    return [
        "pâtes",
        "tomates concassées",
        "ail",
        "oignon",
        "huile d'olive",
        "sel",
        "poivre",
    ]

@mcp.resource("recipes://tips/general")
def general_tips() -> Dict[str, List[str]]:
    """Astuces de cuisine génériques (non issues de scraping)."""
    return {
        "cuisson": [
            "Saisir à feu vif puis réduire pour finir la cuisson.",
            "Saler l'eau des pâtes après ébullition.",
        ],
        "goût": [
            "Acidité: ajouter un peu de sucre ou carotte dans la sauce tomate.",
            "Umami: ajouter champignons, parmesan, sauce soja (petite quantité).",
        ],
    }

# ---------
# TOOLS (actions)
# ---------
@mcp.tool()
async def list_ingredients(style: str = "basics") -> List[str]:
    """Retourne une liste d'ingrédients selon un style simple."""
    if style == "basics":
        return default_ingredients()
    if style == "fridge":
        return ["œufs", "fromage râpé", "lait", "beurre", "restes de légumes", "riz"]
    return ["pain", "tomate", "mozzarella", "basilic", "huile d'olive"]

@mcp.tool()
async def invent_recipe(
    ingredients: List[str],
    servings: int = 2,
    constraints: Optional[List[str]] = None,
) -> Dict[str, object]:
    """Invente une recette à partir d'ingrédients (format structuré)."""
    constraints = constraints or []
    title = "Recette improvisée"

    steps = [
        "Préparer et découper les ingrédients.",
        "Cuire/assembler selon les ingrédients disponibles.",
        "Assaisonner, goûter, ajuster.",
        "Servir.",
    ]

    if "vegetarien" in [c.lower() for c in constraints]:
        # Exemple de légère adaptation
        steps.insert(1, "Éviter les ingrédients carnés; privilégier légumes/fromages/légumineuses.")

@mcp.tool()
async def invent_magical_recipe(
    magical_ingredients: List[str],
    servings: int = 2,
    magic_type: str = "enchantement"
) -> Dict[str, object]:
    """Invente une recette magique à partir d'ingrédients magiques."""
    title = f"Recette Magique de {magic_type}"

    steps = [
        "Mélanger les ingrédients magiques sous la lune.",
        "Chanter une incantation appropriée.",
        "Laisser infuser avec de la magie pure.",
        "Servir avec un sort de présentation.",
    ]

    return {
        "title": title,
        "servings": servings,
        "ingredients": magical_ingredients,
        "steps": steps,
        "magic_type": magic_type,
        "tips_uri": "recipes://tips/general",
    }

@mcp.tool()
async def list_magical_ingredients(style: str = "basics") -> List[str]:
    """Retourne une liste d'ingrédients magiques selon un style."""
    if style == "basics":
        return ["poudre de licorne", "ailes de fée", "potion d'élixir", "feuilles de mandragore", "cristaux de lune"]
    if style == "dark":
        return ["sang de dragon", "œil de troll", "racine de belladone", "poussière de vampire", "larmes de sirène"]
    return ["étoiles filantes", "nectar d'arc-en-ciel", "plumes de phénix", "ambre magique", "eau de source enchantée"]

@mcp.tool()
async def scrape_christmsas_recipes() -> List[str]:
    """Scrape les titres des recettes de Noël depuis Marmiton.org."""
    url = "https://www.marmiton.org/recettes/recherche.aspx?aqt=noël"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    recipes = []
    for item in soup.find_all('a', href=lambda x: x and '/recettes/recette_' in x):
        title = item.text.strip()
        if title:
            recipes.append(title)
    return recipes[:10]  # Limiter à 10 pour l'exemple



# ---------
# PROMPTS
# ---------
@mcp.prompt("recette-magique")
def magical_recipe_prompt(ingredients: List[str]) -> str:
    """Prompt pour générer une recette magique."""
    return f"Crée une recette magique fantastique et amusante avec ces ingrédients : {', '.join(ingredients)}. Inclue des étapes magiques et des effets spéciaux."

@mcp.prompt("astuces-magiques")
def magical_tips_prompt() -> str:
    """Prompt pour obtenir des astuces de cuisine magique."""
    return "Donne-moi des astuces pour cuisiner avec des ingrédients magiques, comme comment éviter les malédictions ou amplifier les sorts culinaires."

# ---------
# RUN
# ---------
def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
