from src.main import MainBot
import asyncio

if __name__ == "__main__":
    bot = MainBot()
    asyncio.run(bot.run())
