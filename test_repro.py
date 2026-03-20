import asyncio
import json
import os
import pathlib
from dotenv import load_dotenv
from dailytasks.newsfeed import NewsFeed

async def main():
    # Load env
    base_dir = pathlib.Path(__file__).parent.resolve()
    env_path = base_dir / "config" / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    
    nf = NewsFeed()
    print("Testing get_daily_news_from_redis...")
    try:
        data = await nf.get_daily_news_from_redis()
        print("Success!")
        # print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Caught error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
