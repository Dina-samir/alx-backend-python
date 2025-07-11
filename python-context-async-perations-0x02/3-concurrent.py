import asyncio
import aiosqlite

DB_NAME = "users.db"

#ref: https://aiosqlite.omnilib.dev/en/stable/

# Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        await cursor.close()
        print("All users:")
        for row in results:
            print(row)
        return results

# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        results = await cursor.fetchall()
        await cursor.close()
        print("\nUsers older than 40:")
        for row in results:
            print(row)
        return results

# Run both queries concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Run the concurrent fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
