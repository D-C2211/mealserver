from typing import Any
import os
import httpx
import logging
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("mealserver")

# Get configuration from environment variables
host = os.getenv("MCP_SERVER_HOST", "127.0.0.1")
port = int(os.getenv("MCP_SERVER_PORT", "8080"))

# Initialize FastMCP server
mcp = FastMCP("mealserver", host=host, port=port)

# Constants for mealdb connection
MEALDB_API_KEY = os.getenv("MEALDB_API_KEY", "1")  # Default to free tier if not provided
MEALDB_API_BASE = f"https://www.themealdb.com/api/json/v1/{MEALDB_API_KEY}"
USER_AGENT = "mealserver-app/1.0"

logger.info(f"Starting mealserver on {host}:{port}")
logger.info(f"Using TheMealDB API: {MEALDB_API_BASE}")

# function to make a request to the meal api
async def make_meal_request(url: str) -> dict[str, Any] | None:
    """Make a request to the MealDB API with proper error handling."""
    logger.debug(f"Making request to: {url}")
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    logger.debug(f"Request headers: {headers}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            logger.debug(f"Response status: {response.status_code}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.reason_phrase}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None

# function to format a meal response  
def format_meal(meal: dict) -> str:
    """Format a meal into a readable string."""
    props = meal
    
    # Extract ingredients and measurements
    ingredients_section = "Ingredients:\n"
    for i in range(1, 21):  # TheMealDB API provides up to 20 ingredients
        ingredient = props.get(f'strIngredient{i}')
        measure = props.get(f'strMeasure{i}')
        
        if ingredient and ingredient.strip() and measure and measure.strip():
            ingredients_section += f"- {measure.strip()} {ingredient.strip()}\n"
        elif ingredient and ingredient.strip():
            ingredients_section += f"- {ingredient.strip()}\n"
    
    return f"""
Meal: {props.get('strMeal', 'Unknown')}
Category: {props.get('strCategory', 'Unknown')}
Country: {props.get('strArea', 'Unknown')}
{ingredients_section}
Instructions: {props.get('strInstructions', 'No instruction available')}
Thumbnail: {props.get('strMealThumb', 'No thumbnail provided')}
Tags: {props.get('strTags', 'No tags provided')}
Youtube: {props.get('strYoutube', 'No YouTube link provided')}
"""

# tool for getting meals by their first letter in their name
@mcp.tool()
async def get_meal_by_letter(letter: str) -> str:
    """Get meal by letter.

    Args:
        letter: Single-letter (e.g. A, B)
    """
    url = f"{MEALDB_API_BASE}/search.php?f={letter}"
    data = await make_meal_request(url)

    if not data or "meals" not in data:
        return "Unable to fetch meals or no meal found for this letter."

    if not data["meals"]:
        return "No meal found for this letter."

    meals = [format_meal(meal) for meal in data["meals"]]
    return "\n---\n".join(meals)

# tool for getting meals by a specified word in their name
@mcp.tool()
async def get_meal_by_name(name: str) -> str:
    """Get meal by name.

    Args:
        name: name (e.g. Arrabiata, Spicy)
    """
    url = f"{MEALDB_API_BASE}/search.php?s={name}"
    data = await make_meal_request(url)

    if not data or "meals" not in data:
        return "Unable to fetch meals or no meal found for this name."

    if not data["meals"]:
        return "No meal found for this name."

    meals = [format_meal(meal) for meal in data["meals"]]
    return "\n---\n".join(meals)

# tool for getting a single random meal
@mcp.tool()
async def get_random_meal() -> str:
    """Get random meal.
    """
    url = f"{MEALDB_API_BASE}/random.php"
    data = await make_meal_request(url)

    if not data or "meals" not in data:
        return "Unable to fetch any meal."

    if not data["meals"]:
        return "No meal found."

    meals = [format_meal(meal) for meal in data["meals"]]
    return "\n---\n".join(meals)

# tool of getting meals by a specified category
@mcp.tool()
async def get_meal_by_category(category: str) -> str:
    """Get meal by category.

    Args:
        category: category (e.g. Seafood)
    """
    url = f"{MEALDB_API_BASE}/search.php?s={category}"
    data = await make_meal_request(url)

    if not data or "meals" not in data:
        return "Unable to fetch meals or no meal found for this category."

    if not data["meals"]:
        return "No meal found for this category."

    meals = [format_meal(meal) for meal in data["meals"]]
    return "\n---\n".join(meals)

# tool of getting meals by a specified country or area
@mcp.tool()
async def get_meal_by_area(area: str) -> str:
    """Get meal by area.

    Args:
        area: area (e.g. Canadian)
    """
    url = f"{MEALDB_API_BASE}/search.php?s={area}"
    data = await make_meal_request(url)

    if not data or "meals" not in data:
        return "Unable to fetch meals or no meal found for this area."

    if not data["meals"]:
        return "No meal found for this area."

    meals = [format_meal(meal) for meal in data["meals"]]
    return "\n---\n".join(meals)

# tool of getting meals by one ingredient
@mcp.tool()
async def get_meal_by_ingredient(ingredient: str) -> str:
    """Get meal by ingredient.

    Args:
        ingredient: ingredient (e.g. chicken_breast)
    """
    url = f"{MEALDB_API_BASE}/filter.php?i={ingredient}"
    data = await make_meal_request(url)

    if not data or "meals" not in data:
        return "Unable to fetch meals or no meal found for this ingredient."

    if not data["meals"]:
        return "No meal found for this ingredient."

    meals = [format_meal(meal) for meal in data["meals"]]
    return "\n---\n".join(meals)

# tool for finding meals that contain multiple ingredients
@mcp.tool()
async def get_meal_by_multiple_ingredients(ingredients: list) -> str:
    """Get meals containing multiple ingredients.

    Args:
        ingredients: List of ingredients (e.g. ["beef", "potatoes"])
    """
    if not ingredients or len(ingredients) == 0:
        return "Please provide at least one ingredient."
    
    # Start with the first ingredient to get initial results
    first_ingredient = ingredients[0]
    url = f"{MEALDB_API_BASE}/filter.php?i={first_ingredient}"
    data = await make_meal_request(url)
    
    if not data or "meals" not in data or not data["meals"]:
        return f"No meals found containing {first_ingredient}."
    
    # If only one ingredient was provided, return those meals
    if len(ingredients) == 1:
        meals = []
        for meal_summary in data["meals"]:
            # Get full meal details
            meal_id = meal_summary.get("idMeal")
            if meal_id:
                meal_url = f"{MEALDB_API_BASE}/lookup.php?i={meal_id}"
                meal_data = await make_meal_request(meal_url)
                if meal_data and "meals" in meal_data and meal_data["meals"]:
                    meals.append(format_meal(meal_data["meals"][0]))
        
        if not meals:
            return f"Could not fetch detailed information for meals with {first_ingredient}."
        
        return "\n---\n".join(meals)
    
    # For multiple ingredients, we need to filter further
    matching_meals = []
    remaining_ingredients = ingredients[1:]
    
    # For each meal that contains the first ingredient
    for meal_summary in data["meals"]:
        meal_id = meal_summary.get("idMeal")
        if not meal_id:
            continue
        
        # Get full meal details
        meal_url = f"{MEALDB_API_BASE}/lookup.php?i={meal_id}"
        meal_data = await make_meal_request(meal_url)
        
        if not meal_data or "meals" not in meal_data or not meal_data["meals"]:
            continue
        
        meal = meal_data["meals"][0]
        
        # Check if meal contains all remaining ingredients
        contains_all = True
        for ingredient in remaining_ingredients:
            ingredient_found = False
            # Check all 20 possible ingredient slots
            for i in range(1, 21):
                meal_ingredient = meal.get(f'strIngredient{i}', '')
                if meal_ingredient and ingredient.lower() in meal_ingredient.lower():
                    ingredient_found = True
                    break
            
            if not ingredient_found:
                contains_all = False
                break
        
        # If meal contains all ingredients, add it to results
        if contains_all:
            matching_meals.append(format_meal(meal))
    
    if not matching_meals:
        ingredients_str = ", ".join(ingredients)
        return f"No meals found containing all these ingredients: {ingredients_str}"
    
    return "\n---\n".join(matching_meals)

# tool of saving all ingredients of a meal to a shoppling list file
@mcp.tool()
async def save_ingredients_to_file(meal_name: str, ingredients_with_measures: list, file_path: str) -> str:
    """Save ingredients of a meal to a file that could be used as a type of shopping list.

    Args:
        meal_name: Name of the meal
        ingredients_with_measures: List of ingredients with their measures
        file_path: Path where to save the ingredients file
    """
    import os
    
    # Create standardized filename with the pattern "<name of meal> - ingredients"
    filename = f"{meal_name} - ingredients.txt"
        
    # Combine directory with the new filename
    full_path = os.path.join(file_path, filename)
    
    # Write to file
    try:
        with open(full_path, 'w') as f:
            f.write(f"Ingredients for {meal_name}:\n\n")
            for item in ingredients_with_measures:
                if isinstance(item, dict) and 'ingredient' in item and 'measure' in item:
                    # Format as "measure ingredient"
                    f.write(f"- {item['measure']} {item['ingredient']}\n")
                else:
                    # If it's already a string or has another format, write it as is
                    f.write(f"- {item}\n")
        return f"Successfully saved ingredients for {meal_name} to {full_path}"
    except Exception as e:
        return f"Error saving file: {str(e)}"

# resource for accessing all meal categories
@mcp.resource(uri="http://localhost/meal_categories")
async def get_meal_categories_resource() -> dict:
    """Resource that provides a list of all available meal categories.
    
    This resource fetches all meal categories from TheMealDB API and returns them
    in a structured format that can be used as context for meal recommendations,
    filtering, or browsing.
    
    Returns:
        A dictionary containing a list of meal categories with their descriptions and thumbnails.
    """
    url = f"{MEALDB_API_BASE}/categories.php"
    data = await make_meal_request(url)
    
    if not data or "categories" not in data:
        return {"error": "Unable to fetch categories", "categories": []}
    
    categories = []
    for category in data["categories"]:
        categories.append({
            "name": category.get("strCategory", "Unknown"),
            "description": category.get("strCategoryDescription", "No description available"),
            "thumbnail": category.get("strCategoryThumb", "")
        })
    
    return {
        "count": len(categories),
        "categories": categories
    }

# resource for accessing all cuisine areas/countries
@mcp.resource(uri="http://localhost/cuisine_areas")
async def get_cuisine_areas_resource() -> dict:
    """Resource that provides a list of all available cuisine areas (countries).
    
    This resource fetches all cuisine areas from TheMealDB API and returns them
    in a structured format that can be used for geographical meal exploration
    and filtering.
    
    Returns:
        A dictionary containing a list of cuisine areas.
    """
    url = f"{MEALDB_API_BASE}/list.php?a=list"
    data = await make_meal_request(url)
    
    if not data or "meals" not in data:
        return {"error": "Unable to fetch cuisine areas", "areas": []}
    
    areas = []
    for area in data["meals"]:
        areas.append(area.get("strArea", "Unknown"))
    
    return {
        "count": len(areas),
        "areas": areas
    }

# resource for accessing common ingredients
@mcp.resource(uri="http://localhost/common_ingredients")
async def get_common_ingredients_resource() -> dict:
    """Resource that provides a list of common ingredients used in recipes.
    
    This resource fetches a list of ingredients from TheMealDB API and returns them
    in a structured format that can be used for recipe suggestions, substitutions,
    or ingredient-based meal exploration.
    
    Returns:
        A dictionary containing a list of common ingredients.
    """
    url = f"{MEALDB_API_BASE}/list.php?i=list"
    data = await make_meal_request(url)
    
    if not data or "meals" not in data:
        return {"error": "Unable to fetch ingredients", "ingredients": []}
    
    ingredients = []
    for item in data["meals"]:
        ingredient = {
            "name": item.get("strIngredient", "Unknown"),
            "description": item.get("strDescription", "No description available")
        }
        # Only include ingredients with a name
        if ingredient["name"] and ingredient["name"] != "Unknown":
            ingredients.append(ingredient)
    
    return {
        "count": len(ingredients),
        "ingredients": ingredients
    }

# prompt for showing recipes from a given cuisine and a given category
@mcp.prompt("Show me {cuisine} {category} recipes")
async def find_cuisine_category_recipes(cuisine: str, category: str) -> str:
    """Find recipes from a specific cuisine and category.
    
    Args:
        cuisine: The cuisine/area (e.g., Italian, Mexican)
        category: The meal category (e.g., Dessert, Seafood)
    """
    # Get meals by area first
    area_result = await get_meal_by_area(cuisine)
    if "No meal found" in area_result:
        return f"Sorry, I couldn't find any {cuisine} recipes."
    
    # Then get meals by category
    category_result = await get_meal_by_category(category)
    if "No meal found" in category_result:
        return f"Sorry, I couldn't find any {category} recipes."
    
    # Simple filtering by checking if meal names appear in both results
    area_meals = area_result.split("\n---\n")
    category_meals = category_result.split("\n---\n")
    
    matching_meals = []
    for area_meal in area_meals:
        area_meal_name = ""
        for line in area_meal.split("\n"):
            if line.startswith("Meal:"):
                area_meal_name = line.strip()
                break
        
        for category_meal in category_meals:
            if area_meal_name and area_meal_name in category_meal:
                matching_meals.append(area_meal)
                break
    
    if matching_meals:
        return "\n---\n".join(matching_meals)
    else:
        return f"I couldn't find any {cuisine} {category} recipes. Would you like to see all {cuisine} recipes or all {category} recipes instead?"

# prompt for showing all possible recipes of a given category
@mcp.prompt("What {category} recipes can I make?")
async def find_category_recipes(category: str) -> str:
    """Find recipes from a specific category.
    
    Args:
        category: The meal category (e.g., Seafood, Vegetarian)
    """
    return await get_meal_by_category(category)

# prompt for showing all possible recipes of a given category that start with a given first letter
@mcp.prompt("Find {category} recipes that start with {letter}")
async def find_recipes_by_letter_and_category(category: str, letter: str) -> str:
    """Find recipes from a category that start with a specific letter.
    
    Args:
        category: The meal category (e.g., Breakfast, Dessert)
        letter: The starting letter (e.g., A, B)
    """
    # Get meals by letter
    letter_result = await get_meal_by_letter(letter.upper())
    if "No meal found" in letter_result:
        return f"Sorry, I couldn't find any recipes starting with '{letter}'."
    
    # Get meals by category
    category_result = await get_meal_by_category(category)
    if "No meal found" in category_result:
        return f"Sorry, I couldn't find any {category} recipes."
    
    # Find meals that appear in both results
    letter_meals = letter_result.split("\n---\n")
    category_meals = category_result.split("\n---\n")
    
    matching_meals = []
    for letter_meal in letter_meals:
        letter_meal_name = ""
        for line in letter_meal.split("\n"):
            if line.startswith("Meal:"):
                letter_meal_name = line.strip()
                break
        
        for category_meal in category_meals:
            if letter_meal_name and letter_meal_name in category_meal:
                matching_meals.append(letter_meal)
                break
    
    if matching_meals:
        return "\n---\n".join(matching_meals)
    else:
        return f"I couldn't find any {category} recipes starting with '{letter}'. Would you like to see all recipes starting with '{letter}' or all {category} recipes instead?"

# prompt for showing all possible recipes of a given category
@mcp.prompt("Suggest a random recipe")
async def suggest_random_recipe() -> str:
    """Suggest a random recipe."""
    return await get_random_meal()

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')