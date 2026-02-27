from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from controllers.nutrition_controller import analyze_food_image

routerNutrition = APIRouter()


class FoodImageRequest(BaseModel):
    image: str


@routerNutrition.post("/analyze-food")
async def analyze_food(request: FoodImageRequest):
    try:
        return await analyze_food_image(request.image)
    except Exception as e:
        print("nutrition error:", e)
        raise HTTPException(status_code=500, detail=str(e))
