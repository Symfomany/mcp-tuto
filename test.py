import asyncio
from typing import List
import requests
from bs4 import BeautifulSoup

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

if __name__ == "__main__":
    recipes = asyncio.run(scrape_christmsas_recipes())
    print(recipes)