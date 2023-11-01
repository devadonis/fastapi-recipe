import asyncio
import httpx

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from app import crud
from app.dependencies.get_db import get_db
from app.schemas.recipe import Recipe, RecipeCreate, RecipeSearchResults


router = APIRouter()
RECIPE_SUBREDDITS = ["recipes", "easyrecipes", "TopSecretRecipes"]


@router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(*, recipe_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Fetch a single recipe by ID
    """
    result = crud.recipe.get(db=db, id=recipe_id)
    if not result:
        # The exception is raised, not returned, - you will get a validation error otherwise
        raise HTTPException(
            status_code=404, detail=f"Recipe with ID {recipe_id} not found"
        )

    return result


@router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipes(
    *,
    keyword: Optional[str] = Query(None, min_length=3, examples=["chicken"]),
    max_results: Optional[int] = 10,
    db: Session = Depends(get_db)
) -> dict:
    """
    Search for recipes based on label keyword
    """
    recipes = crud.recipe.get_multi(db=db, limit=max_results)
    if not keyword:
        return {"results": recipes}

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), recipes)
    return {"results": list(results)[:max_results]}


@router.post("/recipe/", status_code=201, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate, db: Session = Depends(get_db)) -> dict:
    """
    Create a new recipe (in memory only)
    """
    recipe = crud.recipe.create(db=db, obj_in=recipe_in)

    return recipe


async def get_reddit_top_async(subreddit: str) -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t-day&limit=5",
            headers={"User-agent": "recipe bot 0.1"}
        )

    subreddit_recipes = response.json()
    subreddit_data = []

    for entry in subreddit_recipes["data"]["children"]:
        score, title, url = entry["data"]
        subreddit_data.append(f"{str(score)}: {title} ({url})")

    return subreddit_data


def get_reddit_top(subreddit: str) -> list:
    response = httpx.get(
        f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
        headers={"Usr-agent": "recipe bot 0.1"}
    )

    subreddit_recipes = response.json()
    subreddit_data = []

    for entry in subreddit_recipes["data"]["childred"]:
        score, title, url = entry["data"]
        subreddit_data.append(f"{str(score)}: {title} ({url})")

    return subreddit_data


@router.get("/ideas/async")
async def fetch_ideas_async() -> dict:
    results = await asyncio.gather(
        *[get_reddit_top_async(subreddit=subreddit) for subreddit in RECIPE_SUBREDDITS]
    )

    return dict(zip(RECIPE_SUBREDDITS, results))


@router.get("/ideas/")
def fetch_ideas() -> dict:
    return {key: get_reddit_top(subreddit=key) for key in RECIPE_SUBREDDITS}
