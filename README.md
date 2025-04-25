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

### Prompts
- Access meals with the help of some prompts (pre-defined templates to assist more natural language requests)

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

5. **get_meal_by_multiple_ingredients**
   - Finds meals that contain multiple specified ingredients
   - Parameter: `ingredients` (a list of ingredients, e.g., ["beef", "potatoes"])
   - Returns meals that contain ALL of the specified ingredients
   - Perfect for finding recipes based on ingredients you have on hand
   - Useful for reducing food waste and creative cooking

6. **get_meal_by_category**
   - Retrieves meals from a specific category
   - Parameter: `category` (e.g., "Seafood", "Vegetarian")
   - Returns meals belonging to the specified category
   - Useful for finding meals within dietary preferences or meal types

7. **get_meal_by_area**
   - Finds meals from a specific cuisine or region
   - Parameter: `area` (e.g., "Italian", "Mexican")
   - Returns meals from the specified cuisine
   - Perfect for exploring international cuisines

8. **save_ingredients_to_file**
   - Saves a meal's ingredients to a file (can be used as a shopping list)
   - Parameters:
     - `meal_name`: Name of the meal
     - `ingredients_with_measures`: List of ingredients with their measurements
     - `file_path`: Path where to save the ingredients file
   - Creates a formatted text file with all ingredients needed for a recipe
   - Useful for meal planning and grocery shopping



These tools can be used individually or in combination to find recipes, explore cuisines, and plan meals based on various criteria.