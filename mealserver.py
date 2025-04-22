from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mealserver", host="127.0.0.1", port=8080)

# Constants for mealdb connection
MEALDB_API_BASE = "https://www.themealdb.com/api/json/v1/1"
USER_AGENT = "mealserver-app/1.0"

# function to make a request to the meal api
async def make_meal_request(url: str) -> dict[str, Any] | None:
    """Make a request to the MealDB API with proper error handling."""
    print(f"Making request to: {url}")
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    print(f"Headers: {headers}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
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

# function to format a mesl category reponse
def format_category(category: dict) -> str:
    """Format a category into a readable string."""
    props = category
    return f"""
Category: {props.get('strCategory', 'Unknown')}
Thumbnail: {props.get('strCategoryThumb', 'No thumbnail provided')}
Description: {props.get('strCategoryDescription', 'No description provided')}
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

# tool for getting all existing meal categories
@mcp.tool()
async def get_categories() -> str:
    """Get all meal categories.
    """
    url = f"{MEALDB_API_BASE}/categories.php"
    data = await make_meal_request(url)
    
    if not data or "categories" not in data:
        return "Unable to fetch any category."

    if not data["categories"]:
        return "No category found."

    meals = [format_category(category) for category in data["categories"]]
    return "\n---\n".join(meals)

# tool of gettinng meals by their main ingredient
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

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')