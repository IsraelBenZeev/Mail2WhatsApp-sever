import asyncio
from dotenv import load_dotenv
load_dotenv()

from agents import Runner
from nutrition_agent import init_nutrition_agent

async def main():
    agent = init_nutrition_agent()
    result = await Runner.run(agent, "What is the nutritional value of 100g of chicken breast? Return JSON.")
    print(result.final_output)

asyncio.run(main())
