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
