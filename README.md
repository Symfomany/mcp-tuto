# Recettes MCP Server

Ce projet est un serveur MCP (Model Context Protocol) qui fournit des outils et ressources pour la gestion de recettes culinaires, incluant des fonctionnalités de scraping web et de génération de recettes magiques.

## Technologies et Stack Utilisées

### Langage de Programmation
- **Python 3.12+** : Langage principal utilisé pour développer le serveur.

### Frameworks et Bibliothèques
- **FastMCP** : Framework de la bibliothèque `mcp` pour créer des serveurs MCP rapidement. Utilisé pour définir les ressources, outils et prompts du serveur.
- **Requests** : Bibliothèque pour effectuer des requêtes HTTP, utilisée pour le scraping web.
- **BeautifulSoup4** : Bibliothèque pour analyser et extraire des données HTML, utilisée conjointement avec requests pour scraper des sites comme Marmiton.org.
- **Python-Marmiton** : Bibliothèque spécifique pour interagir avec le site Marmiton.org.
- **PyMongo** : Bibliothèque pour interagir avec MongoDB, utilisée pour interroger des bases de données.

### Outils de Développement
- **uv** : Outil de gestion de paquets et d'exécution Python moderne, utilisé pour exécuter le serveur via `uv run python main.py`.
- **MCP-CLI** : Outil en ligne de commande pour gérer les serveurs MCP.

### Configuration
- **pyproject.toml** : Fichier de configuration pour les métadonnées du projet, les dépendances et les exigences Python.
- **server_config.json** : Configuration spécifique pour le serveur MCP, définissant la commande et les arguments pour lancer le serveur.

### Fonctionnalités Principales
- **Ressources** : Fournit des listes d'ingrédients par défaut et des astuces de cuisine.
- **Outils** : Permet de lister des ingrédients, inventer des recettes, scraper des recettes de Noël, gérer des ingrédients magiques, et interroger une base de données MongoDB 'recipies' (collections : comments, users, ustensils).
- **Prompts** : Offre des prompts pour générer des recettes magiques et des astuces culinaires magiques.

## Installation et Exécution

1. Assurez-vous d'avoir Python 3.12+ installé.
2. Installez les dépendances avec `uv` :
   ```
   uv sync
   ```
3. Lancez le serveur :
   ```
   uv run python main.py
   ```

## Configuration MCP

Le serveur est configuré via `server_config.json` pour être utilisé avec des clients MCP comme LM Studio.

## Utilisation avec des Prompts

Ce serveur MCP est conçu pour être utilisé avec un client compatible, comme un modèle de langage (LLM). Vous pouvez interagir avec le serveur en utilisant des prompts en langage naturel. Voici quelques exemples de ce que vous pouvez demander :

### Explorer les Recettes de Noël

Vous pouvez rechercher, lister et obtenir des détails sur les recettes de Noël.

-   **"Liste-moi toutes les recettes de Noël."**
    -   Cette commande appelle l'outil `list_christmas_recipes` et retourne une liste complète des recettes de Noël disponibles.

-   **"Je cherche une recette avec des marrons."**
    -   L'outil `search_by_ingredient` est utilisé avec le paramètre `ingredient="marrons"` pour trouver toutes les recettes contenant cet ingrédient.

-   **"Donne-moi une recette de Noël au hasard."**
    -   L'outil `get_random_recipe` est appelé pour retourner une seule recette de Noël de manière aléatoire.

-   **"Propose-moi un menu complet pour le réveillon."**
    -   L'outil `suggest_christmas_menu` génère un menu complet avec une entrée, un plat principal et un dessert.

-   **"J'aimerais faire la recette de la 'Dinde de Noël', mais pour 12 personnes."**
    -   L'outil `scale_recipe` est utilisé avec `recipe_name="Dinde de Noël"` and `servings=12` pour ajuster les quantités d'ingrédients.

### Créer et Inventer des Recettes

Le serveur peut vous aider à créer de nouvelles recettes à partir des ingrédients que vous avez.

-   **"Invente-moi une recette avec du poulet, des champignons et de la crème."**
    -   L'outil `invent_recipe` est appelé avec `ingredients=["poulet", "champignons", "crème"]` pour créer une nouvelle recette.

-   **"Génère une recette à partir des ingrédients suivants : saumon, aneth, citron."**
    -   L'outil `generate_recipe_from_ingredients` prendra la liste des ingrédients pour créer une nouvelle recette de Noël.

### Cuisine Magique

Pour une touche de fantaisie, vous pouvez explorer la cuisine magique.

-   **"Je veux créer une recette magique avec de la poudre de licorne et des larmes de sirène."**
    -   L'outil `invent_magical_recipe` est appelé avec `magical_ingredients=["poudre de licorne", "larmes de sirène"]`.

-   **"Comment puis-je utiliser du sang de dragon en cuisine sans me faire maudire ?"**
    -   Le prompt `astuces-magiques` est utilisé pour générer une réponse qui donne des conseils sur l'utilisation d'ingrédients magiques.

-   **"Crée une recette magique fantastique et amusante avec des ailes de fée et des cristaux de lune."**
    -   Le prompt `recette-magique` est utilisé avec les ingrédients `["ailes de fée", "cristaux de lune"]` pour générer une recette magique détaillée.

### Outils Utilitaires

Le serveur fournit également des outils pratiques.

-   **"Crée une liste de courses pour la recette 'Bûche de Noël'."**
    -   L'outil `create_shopping_list` est appelé avec `recipe_name="Bûche de Noël"` pour générer la liste des ingrédients nécessaires.

-   **"Quel vin irait bien avec la 'Dinde de Noël' ?"**
    -   L'outil `suggest_wine_pairing` est appelé avec `recipe_name="Dinde de Noël"` pour suggérer un accord mets-vin.

-   **"Quelles sont les dernières recettes de Noël sur Marmiton ?"**
    -   L'outil `scrape_christmas_recipes` est appelé pour scraper les titres des dernières recettes de Noël sur Marmiton.org.
