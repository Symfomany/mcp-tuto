from __future__ import annotations

from typing import List, Optional, Dict, Any
import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP
from pymongo import MongoClient
import random
from pydantic import BaseModel, Field
import logging

from bson import ObjectId
from datetime import datetime

### Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("recipies")



### Helper function to convert MongoDB documents to JSON-serializable format
def _to_jsonable(doc: Dict[str, any]) -> Dict[str, any]:
    out = {}
    for k, v in doc.items():
        if isinstance(v, ObjectId):
            out[k] = str(v)
        elif isinstance(v, datetime):
            out[k] = v.isoformat()
        elif isinstance(v, dict):
            out[k] = _to_jsonable(v)
        elif isinstance(v, list):
            out[k] = [_to_jsonable(x) if isinstance(x, dict) else x for x in v]
        else:
            out[k] = v
    return out


# ---------
# MCP INITIALIZATION
# ---------
mcp = FastMCP("recipies")


# ---------
# MODELS
# ---------
class Recipe(BaseModel):
    name: str
    category: str  # "Entrée", "Plat principal", "Dessert"
    servings: int
    ingredients: Dict[str, str]  # e.g., {"chocolat noir": "200g"}
    instructions: List[str]
    wine_pairing: Optional[str] = None

# ---------
# RESOURCES (lecture seule)
# ---------

@mcp.resource(
    "recipes://ingredients/default",
    description="Default ingredients list.",
)
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

@mcp.resource(
    "recipes://tips/general",
    description="General cooking tips.",
)
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

@mcp.resource(
    "recipes://christmas/all",
    description="List of Christmas recipes.",
)
def christmas_recipes() -> List[Recipe]:
    """Liste de recettes de Noël."""
    return [
        Recipe(
            name="Dinde de Noël",
            category="Plat principal",
            servings=8,
            ingredients={"dinde": "1", "marrons": "500g", "beurre": "100g", "sel": "1 pincée", "poivre": "1 pincée"},
            instructions=[
                "Préchauffer le four à 180°C.",
                "Farcir la dinde avec les marrons.",
                "Badigeonner de beurre, saler et poivrer.",
                "Enfourner pour 3 heures.",
            ],
            wine_pairing="Bourgogne rouge",
        ),
        Recipe(
            name="Bûche de Noël",
            category="Dessert",
            servings=6,
            ingredients={"chocolat noir": "200g", "beurre": "100g", "sucre": "150g", "oeufs": "4", "farine": "50g"},
            instructions=[
                "Faire fondre le chocolat avec le beurre.",
                "Ajouter le sucre, les oeufs et la farine.",
                "Verser sur une plaque et cuire 10 minutes.",
                "Rouler la bûche et la laisser refroidir.",
            ],
            wine_pairing="Champagne",
        ),
        Recipe(
            name="Saumon fumé sur blinis",
            category="Entrée",
            servings=4,
            ingredients={"saumon fumé": "4 tranches", "blinis": "8", "crème fraîche": "100g", "ciboulette": "1 botte"},
            instructions=[
                "Tartiner les blinis de crème fraîche.",
                "Ajouter une tranche de saumon fumé.",
                "Ciseler la ciboulette et en parsemer les blinis.",
            ],
            wine_pairing="Sancerre",
        ),
    ]

# ---------
# TOOLS (actions)
# ---------
@mcp.tool(
    name="list_christmas_recipes",
    description="Returns a list of all Christmas recipes.",
)
async def list_christmas_recipes() -> List[Dict]:
    """Retourne la liste de toutes les recettes de Noël."""
    return [recipe.model_dump() for recipe in christmas_recipes()]

@mcp.tool(
    name="search_by_ingredient",
    description="Search for Christmas recipes containing a specific ingredient.",
)
async def search_by_ingredient(ingredient: str) -> List[Dict]:
    """Recherche les recettes de Noël contenant un ingrédient spécifique."""
    results = []
    for recipe in christmas_recipes():
        if ingredient.lower() in [ing.lower() for ing in recipe.ingredients.keys()]:
            results.append(recipe.model_dump())
    return results

@mcp.tool(
    name="get_random_recipe",
    description="Returns a random Christmas recipe.",
)
async def get_random_recipe() -> Dict:
    """Retourne une recette de Noël au hasard."""
    return random.choice(christmas_recipes()).model_dump()

@mcp.tool(
    name="suggest_christmas_menu",
    description="Suggests a complete Christmas menu (starter, main course, dessert).",
)
async def suggest_christmas_menu() -> Dict[str, Dict]:
    """Suggère un menu de Noël complet (entrée, plat, dessert)."""
    recipes = christmas_recipes()
    entrees = [r for r in recipes if r.category == "Entrée"]
    plats = [r for r in recipes if r.category == "Plat principal"]
    desserts = [r for r in recipes if r.category == "Dessert"]

    return {
        "entree": random.choice(entrees).model_dump() if entrees else None,
        "plat_principal": random.choice(plats).model_dump() if plats else None,
        "dessert": random.choice(desserts).model_dump() if desserts else None,
    }

@mcp.tool(
    name="scale_recipe",
    description="Scales a recipe for a different number of servings.",
)
async def scale_recipe(recipe_name: str, servings: int) -> Dict:
    """Met à l'échelle une recette pour un nombre de personnes différent."""
    for recipe in christmas_recipes():
        if recipe.name.lower() == recipe_name.lower():
            scaled_ingredients = {}
            for ingredient, quantity in recipe.ingredients.items():
                try:
                    # Simple scaling, may not work for all units
                    amount, unit = quantity.split("g")
                    scaled_amount = (int(amount) / recipe.servings) * servings
                    scaled_ingredients[ingredient] = f"{scaled_amount:.0f}g"
                except ValueError:
                    scaled_ingredients[ingredient] = quantity  # Cannot scale
            
            scaled_recipe = recipe.model_copy()
            scaled_recipe.servings = servings
            scaled_recipe.ingredients = scaled_ingredients
            return scaled_recipe.model_dump()
    return {"error": "Recette non trouvée."}

@mcp.tool(
    name="create_shopping_list",
    description="Creates a shopping list for a recipe.",
)
async def create_shopping_list(recipe_name: str) -> Dict:
    """Crée une liste de courses pour une recette."""
    for recipe in christmas_recipes():
        if recipe.name.lower() == recipe_name.lower():
            return {"recipe": recipe.name, "ingredients": recipe.ingredients}
    return {"error": "Recette non trouvée."}

@mcp.tool(
    name="suggest_wine_pairing",
    description="Suggests a wine pairing for a recipe.",
)
async def suggest_wine_pairing(recipe_name: str) -> Dict:
    """Suggère un accord mets-vin pour une recette."""
    for recipe in christmas_recipes():
        if recipe.name.lower() == recipe_name.lower():
            return {"recipe": recipe.name, "wine_pairing": recipe.wine_pairing}
    return {"error": "Recette non trouvée."}

@mcp.tool(
    name="generate_recipe_from_ingredients",
    description="Generates a new Christmas recipe from a list of ingredients.",
)
async def generate_recipe_from_ingredients(ingredients: List[str]) -> Dict:
    """Génère une nouvelle recette de Noël à partir d'une liste d'ingrédients."""
    return {
        "name": "Recette créative de Noël",
        "category": "Plat principal",
        "servings": 4,
        "ingredients": {ingredient: "quantité au goût" for ingredient in ingredients},
        "instructions": [
            "Préchauffer le four à 180°C.",
            "Mélanger tous les ingrédients dans un plat.",
            "Enfourner pour 30 minutes.",
            "Déguster avec amour.",
        ],
        "wine_pairing": "Un vin qui vous fait plaisir !",
    }


@mcp.tool(
    name="list_ingredients",
    description="Returns a list of ingredients based on a simple style.",
)
async def list_ingredients(style: str = "basics") -> List[str]:
    """Retourne une liste d'ingrédients selon un style simple."""
    if style == "basics":
        return default_ingredients()
    if style == "fridge":
        return ["oeufs", "fromage râpé", "lait", "beurre", "restes de légumes", "riz"]
    return ["pain", "tomate", "mozzarella", "basilic", "huile d'olive"]

@mcp.tool(
    name="invent_recipe",
    description="Invents a recipe from ingredients (structured format).",
)
async def invent_recipe(ingredients: list[str], servings: int = 4) -> dict:
    """Invente une recette à partir des ingrédients et du nombre de personnes."""
    logger.info("invent_recipe called with ingredients=%s, servings=%s", ingredients, servings)

    # ta logique
    recipe = {
        "title": "Entrée de fête au foie gras et fruits",
        "ingredients": ingredients,
        "servings": servings,
    }
    logger.info("invent_recipe returning recipe=%s", recipe)
    return recipe


@mcp.tool(
    name="invent_magical_recipe",
    description="Invents a magical recipe from magical ingredients.",
)
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


@mcp.tool(
    name="elicit_user_needs",
    description="Helps the user create a recipe based on their needs.",
)
async def elicit_user_needs(
    ingredients: Optional[List[str]] = None,
    utensils: Optional[List[str]] = None,
    time: Optional[int] = None,
) -> Dict[str, object]:
    """Aides l'utilisateur a créér une recette à partir de ses besoins"""
    return {
        "ingredients": ingredients,
        "utensils": utensils,
        "time": time,
    }



@mcp.tool(
    name="list_magical_ingredients",
    description="Returns a list of magical ingredients by style.",
)
async def list_magical_ingredients(style: str = "basics") -> List[str]:
    """Retourne une liste d'ingrédients magiques selon un style."""
    if style == "basics":
        return ["poudre de licorne", "ailes de fée", "potion d'élixir", "feuilles de mandragore", "cristaux de lune"]
    if style == "dark":
        return ["sang de dragon", "œil de troll", "racine de belladone", "poussière de vampire", "larmes de sirène"]
    return ["étoiles filantes", "nectar d'arc-en-ciel", "plumes de phénix", "ambre magique", "eau de source enchantée"]

# @mcp.tool(
#     name="scrape_christmas_recipes",
#     description="Scrapes Christmas recipe titles from Marmiton.org.",
# )
# async def scrape_christmsas_recipes() -> List[str]:
#     """Scrape les titres des recettes de Noël depuis Marmiton.org."""
#     url = "https://www.marmiton.org/recettes/recherche.aspx?aqt=noël"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     recipes = []
#     for item in soup.find_all('a', href=lambda x: x and '/recettes/recette_' in x):
#         title = item.text.strip()
#         if title:
#             recipes.append(title)
#     return recipes[:10]  # Limiter à 10 pour l'exemple




@mcp.tool(
    name="get_recipe_by_index",
    description="Retrieves a Christmas recipe by its index (1-based).",
)
async def get_recipe_by_index(index: int) -> Dict:
    """Récupère une recette de Noël par son index (1-based)."""
    recipes = christmas_recipes()
    if 1 <= index <= len(recipes):
        return recipes[index - 1].model_dump()
    return {"error": "Index de recette invalide."}




### BDD MongoDB


# @mcp.tool(
#     name="query_comments",
#     description="Queries the 'comments' collection of the 'recipies' MongoDB database.",
# )
# async def query_comments(query: Optional[Dict] = None) -> List[Dict]:
#     """Interroge la collection 'comments' de la base de données MongoDB 'recipies'."""
#     client = MongoClient('mongodb://localhost:27017/')
#     db = client['recipies']
#     collection = db['comments']
#     query = query or {}
#     results = list(collection.find(query))
#     client.close()

#     return [_to_jsonable(doc) for doc in results]


# @mcp.tool(
#     name="query_users",
#     description="Queries the 'users' collection of the 'recipies' MongoDB database.",
# )
# async def query_users(query: Optional[Dict] = None) -> List[Dict]:
#     """Interroge la collection 'users' de la base de données MongoDB 'recipies'."""
#     client = MongoClient('mongodb://localhost:27017/')
#     db = client['recipies']
#     collection = db['users']
#     query = query or {}
#     docs  = list(collection.find(query))
#     client.close()
    
#     return [_to_jsonable(doc) for doc in docs]


# @mcp.tool(
#     name="query_ustensils",
#     description="Queries the 'ustensils' collection of the 'recipies' MongoDB database.",
# )
# async def query_ustensils(query: Optional[Dict] = None) -> List[Dict]:
#     """Interroge la collection 'ustensils' de la base de données MongoDB 'recipies'."""
#     client = MongoClient('mongodb://localhost:27017/')
#     db = client['recipies']
#     collection = db['ustensils']
#     query = query or {}
#     results = list(collection.find(query))
#     client.close()
    
#     return [_to_jsonable(doc) for doc in results]

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
    mcp.run()

if __name__ == "__main__":
    main()
