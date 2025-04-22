# Meal Server

A Python-based MCP server for accessing [TheMealDB API](https://www.themealdb.com/).

## About TheMealDB

[TheMealDB](https://www.themealdb.com/) is an open, crowd-sourced database of recipes from around the world. The database includes:

- Detailed meal recipes with ingredients and instructions
- Categorization by meal type, region, and ingredients
- Images and videos for many recipes
- Free API access for basic features

This MCP server provides a convenient interface to TheMealDB's API through Claude, Clide, or similar AI clients, allowing you to search for and retrieve meal information using natural language.

## Features

### Tools
- Get meals by letter, name, ingredient, category, or area
- Get random meals
- Save ingredients to a file for shopping lists

### Resources
- Access meal categories (dessert, seafood, vegetarian, etc.)
- Access cuisine areas/regions (Italian, Mexican, Indian, etc.)
- Access common ingredients database (575+ ingredients)

## Usage

To run the server:

```
python mealserver.py
```

## MCP Client Integration

To use this server with Claude, Clide, or similar MCP-compatible clients, you need to add it to your client's MCP settings configuration. For example, with Cline (a VS Code extension for Claude), you would add it to your `cline_mcp_settings.json` file. This file is typically located at:

- Windows: `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
- macOS: `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
- Linux: `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

Add the following configuration to the `mcpServers` object in your settings file:

```json
"mealserver": {
  "command": "uv",
  "args": [
    "--directory",
    "C:\\mcp\\mealserver",
    "run",
    "mealserver.py"
  ]
}
```

Make sure to adjust the directory path to match your installation location.

After adding this configuration, restart your MCP client or reload the window. You should then be able to use the mealserver tools in your conversations with your AI assistant.

## MCP Tools

This MCP server provides several tools that allow AI assistants to interact with TheMealDB API. Each tool serves a specific purpose for retrieving or manipulating meal data.

### Available Tools

1. **get_meal_by_letter**
   - Retrieves meals that start with a specific letter
   - Parameter: `letter` (a single letter, e.g., "A", "B")
   - Returns formatted meal information including ingredients, instructions, and links
   - Useful for exploring meals alphabetically

2. **get_meal_by_name**
   - Searches for meals by name or partial name
   - Parameter: `name` (e.g., "Arrabiata", "Spicy")
   - Returns detailed information about matching meals
   - Perfect for finding specific recipes or meals containing certain words

3. **get_random_meal**
   - Retrieves a random meal from the database
   - No parameters required
   - Returns complete meal details
   - Great for meal inspiration or discovering new recipes

4. **get_meal_by_ingredient**
   - Finds meals that use a specific ingredient
   - Parameter: `ingredient` (e.g., "chicken_breast", "tomatoes")
   - Returns meals containing the specified ingredient
   - Ideal for planning meals based on available ingredients

5. **get_meal_by_category**
   - Retrieves meals from a specific category
   - Parameter: `category` (e.g., "Seafood", "Vegetarian")
   - Returns meals belonging to the specified category
   - Useful for finding meals within dietary preferences or meal types

6. **get_meal_by_area**
   - Finds meals from a specific cuisine or region
   - Parameter: `area` (e.g., "Italian", "Mexican")
   - Returns meals from the specified cuisine
   - Perfect for exploring international cuisines

7. **save_ingredients_to_file**
   - Saves a meal's ingredients to a file (can be used as a shopping list)
   - Parameters:
     - `meal_name`: Name of the meal
     - `ingredients_with_measures`: List of ingredients with their measurements
     - `file_path`: Path where to save the ingredients file
   - Creates a formatted text file with all ingredients needed for a recipe
   - Useful for meal planning and grocery shopping

These tools can be used individually or in combination to find recipes, explore cuisines, and plan meals based on various criteria.

## MCP Resources

In addition to tools, this MCP server provides several resources that can be accessed directly by AI assistants. Resources are data sources that provide context and information without requiring specific parameters.

### Available Resources

1. **Meal Categories** (URI: `http://localhost/meal_categories`)
   - Provides a comprehensive list of all 14 meal categories available in TheMealDB
   - Categories include: Beef, Chicken, Dessert, Lamb, Miscellaneous, Pasta, Pork, Seafood, Side, Starter, Vegan, Vegetarian, Breakfast, and Goat
   - Each category includes a name, description, and thumbnail image URL

2. **Cuisine Areas** (URI: `http://localhost/cuisine_areas`)
   - Provides a list of all 29 cuisine regions/countries available in TheMealDB
   - Regions include: American, British, Canadian, Chinese, Croatian, Dutch, Egyptian, Filipino, French, Greek, Indian, Irish, Italian, Jamaican, Japanese, Kenyan, Malaysian, Mexican, Moroccan, Polish, Portuguese, Russian, Spanish, Thai, Tunisian, Turkish, Ukrainian, Uruguayan, and Vietnamese

3. **Common Ingredients** (URI: `http://localhost/common_ingredients`)
   - Provides access to a database of 575+ common cooking ingredients
   - Each ingredient includes a name and many include detailed descriptions
   - Ingredients span various categories including meats, vegetables, fruits, grains, dairy, herbs, spices, and more

These resources can be used to explore the available meal options, understand different cuisine types, and discover ingredients for recipe planning.