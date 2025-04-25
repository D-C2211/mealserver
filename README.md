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

## Environment Variables and Security

The mealserver uses environment variables for configuration and security. These are loaded from a `.env` file in the project root directory.

### Setting Up Environment Variables

1. Copy the `.env.example` file to create a new `.env` file:
   ```
   cp .env.example .env
   ```

2. Edit the `.env` file to customize your configuration:
   ```
   # TheMealDB API Configuration
   # Default is "1" for the free tier, change if you have premium access
   MEALDB_API_KEY=1

   # MCP Server Configuration
   MCP_SERVER_HOST=127.0.0.1
   MCP_SERVER_PORT=8080

   # Security Configuration
   # Generate a secure random key for production use
   MCP_SERVER_API_KEY=your_secure_api_key_here

   # Logging Configuration
   # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
   LOG_LEVEL=INFO

   # Rate Limiting Configuration
   # Number of requests allowed per time window
   RATE_LIMIT_MAX_REQUESTS=60
   # Time window in seconds
   RATE_LIMIT_WINDOW_SECONDS=60
   ```

### Security Features

The mealserver includes several security features:

1. **API Key Management**: TheMealDB API key is stored in environment variables rather than hardcoded in the source code.

2. **Logging**: Comprehensive logging with configurable log levels helps track usage and identify potential issues.

3. **Error Handling**: Robust error handling prevents exposing sensitive information in error messages.

4. **Environment Variable Protection**: The `.env` file is excluded from version control via `.gitignore` to prevent accidental exposure of sensitive information.

### Premium API Access

If you have a premium subscription to TheMealDB API, you can set your API key in the `.env` file:

```
MEALDB_API_KEY=your_premium_api_key_here
```

This will automatically use your premium API key for all requests to TheMealDB.

## Usage Examples

Here are some examples of how to interact with the mealserver through an AI assistant like Claude:

### Finding Recipes by Name

```
User: Can you find me a recipe for Arrabiata?

Claude: I'll search for Arrabiata recipes using the mealserver.
[Uses get_meal_by_name tool with parameter "Arrabiata"]

I found Pasta all'Arrabiata! Here's the recipe:

Meal: Pasta all'Arrabiata
Category: Vegetarian
Country: Italian

Ingredients:
- 1 pound Penne Rigate
- 1/4 cup Olive Oil
- 3 cloves Garlic
- 1 tin Chopped Tomatoes
- 1/2 teaspoon Red Chile Flakes
- 1/2 teaspoon Italian Seasoning
- 6 leaves Basil
- Spinkling Parmigiano-Reggiano

Instructions: [Full cooking instructions would appear here]
```

### Getting a Random Recipe for Inspiration

```
User: I'm not sure what to cook tonight. Any suggestions?

Claude: Let me get a random recipe suggestion for you.
[Uses get_random_meal tool]

How about trying Beef and Mustard Pie? Here's the recipe:

Meal: Beef and Mustard Pie
Category: Beef
Country: British

Ingredients:
- 2 tbs Olive Oil
- 1 Onion
- 2 Carrots
- 2 tbs Plain Flour
- 2 tbs Mustard
- 2 Bay Leaves
- 500g Beef
- 500g Puff Pastry
- 300g Mushrooms
- 1 Egg Yolk
- 2 tbs Thyme
- 200g Creme Fraiche
- 0.5 Beef Stock Cube

Instructions: [Full cooking instructions would appear here]
```

### Finding Recipes Based on Ingredients You Have

```
User: I have chicken, potatoes, and rosemary. What can I make?

Claude: Let me find recipes that use those ingredients.
[Uses get_meal_by_multiple_ingredients tool with parameters ["chicken", "potatoes", "rosemary"]]

I found Roast Chicken with Lemon and Rosemary! Here's the recipe:

Meal: Roast Chicken with Lemon and Rosemary
Category: Chicken
Country: British

Ingredients:
- 1 whole Chicken
- 2 pounds Potatoes
- 1 sprig Rosemary
- 1 Lemon
- 2 tbs Olive Oil
- 1 tsp Salt
- 1 tsp Black Pepper

Instructions: [Full cooking instructions would appear here]
```

### Exploring Cuisine from a Specific Region

```
User: I'd like to try making some Thai food. What options do I have?

Claude: Let me find some Thai recipes for you.
[Uses get_meal_by_area tool with parameter "Thai"]

Here are some Thai recipes you might enjoy:

1. Thai Green Curry
2. Pad See Ew
3. Massaman Beef Curry
4. Thai Red Curry Fish Cakes
5. Tom Yum Soup

Would you like the full recipe for any of these?
```

### Creating a Shopping List

```
User: I want to make Beef Stroganoff. Can you create a shopping list for me?

Claude: Let me find the recipe and create a shopping list for you.
[Uses get_meal_by_name tool with parameter "Beef Stroganoff"]
[Then uses save_ingredients_to_file tool with the ingredients]

I've created a shopping list for Beef Stroganoff and saved it to "Beef Stroganoff - ingredients.txt". Here's what you'll need:

- 1 lb Beef
- 2 tbs Olive Oil
- 1 Onion
- 1 tbs Plain Flour
- 1 tbs Tomato Puree
- 1 cup Beef Stock
- 1 tbs Worcestershire Sauce
- 1 tsp Dijon Mustard
- 2 cups Mushrooms
- 1 cup Sour Cream
- Parsley (for garnish)
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

## MCP Prompts

In addition to tools and resources, this MCP server provides several prompts that can be used directly by AI assistants. Prompts are pre-defined natural language patterns that map to specific functionality, making it easier to interact with the server.

### Available Prompts

1. **Show me {cuisine} {category} recipes**
   - Finds recipes that match both a specific cuisine and category
   - Parameters:
     - `cuisine`: The cuisine/area (e.g., Italian, Mexican)
     - `category`: The meal category (e.g., Dessert, Seafood)
   - Returns meals that belong to both the specified cuisine and category
   - Example: "Show me Italian Pasta recipes"
   - Useful for exploring specific types of dishes within a cuisine

2. **What {category} recipes can I make?**
   - Retrieves all recipes from a specific category
   - Parameter: `category`: The meal category (e.g., Seafood, Vegetarian)
   - Returns all meals belonging to the specified category
   - Example: "What Dessert recipes can I make?"
   - Useful for exploring meal options within a dietary preference or meal type

3. **Find {category} recipes that start with {letter}**
   - Finds recipes from a specific category that start with a particular letter
   - Parameters:
     - `category`: The meal category (e.g., Breakfast, Dessert)
     - `letter`: The starting letter (e.g., A, B)
   - Returns meals that belong to the specified category and start with the given letter
   - Example: "Find Vegetarian recipes that start with B"
   - Perfect for narrowing down recipe options or playing food-related games

4. **Suggest a random recipe**
   - Retrieves a random meal from the database
   - No parameters required
   - Returns complete details for a randomly selected meal
   - Example: "Suggest a random recipe"
   - Great for meal inspiration or discovering new recipes to try

These prompts provide a more natural way to interact with the meal database, allowing for intuitive queries that combine multiple search criteria.