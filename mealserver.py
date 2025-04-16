from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mealserver", host="127.0.0.1", port=8080)

# Constants
MEALDB_API_BASE = "https://www.themealdb.com/api/json/v1/1"
USER_AGENT = "mealserver-app/1.0"

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
        
def format_meal(meal: dict) -> str:
    """Format a meal into a readable string."""
    props = meal
    return f"""
Meal: {props.get('strMeal', 'Unknown')}
Category: {props.get('strCategory', 'Unknown')}
Country: {props.get('strArea', 'Unknown')}
Instructions: {props.get('strInstructions', 'No instruction available')}
Thumbnail: {props.get('strMealThumb', 'No thumbnail provided')}
Tags: {props.get('strTags', 'No tags provided')}
Youtube: {props.get('strYoutube', 'No YouTube link provided')}
"""

def format_category(category: dict) -> str:
    """Format a category into a readable string."""
    props = category
    return f"""
Category: {props.get('strCategory', 'Unknown')}
Thumbnail: {props.get('strCategoryThumb', 'No thumbnail provided')}
Description: {props.get('strCategoryDescription', 'No description provided')}
"""

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

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')