import aiosqlite
from data.config import DB
import asyncio
from data.config import min_priority

flag = True
async def add_user(user_id: int, user_name: str, number: int, priority: int) -> None:
    async with aiosqlite.connect(DB) as conn:
        query_1 = "INSERT INTO queue(id, user_name, number, priority) VALUES(?, ?, ?, ?)"
        query_2 = "UPDATE queue SET number = number + 1 WHERE priority > ?"
        await conn.execute(query_1, (user_id, user_name, number, priority))
        await conn.execute(query_2, (priority,))
        await conn.commit()


async def find_max(priority: int) -> int:
    async with aiosqlite.connect(DB) as conn:
        query = "SELECT MAX(number) FROM queue WHERE priority = ?"
        cursor: aiosqlite.Cursor
        async with conn.execute(query, (priority,)) as cursor:
            num_tuple = await cursor.fetchone()
    if num_tuple[0] is not None:
        num = num_tuple[0]
        max_num = num + 1
    else:
        if priority > min_priority:
            await find_max(priority - 1)
        else:
            await find_max(priority - 1)
    return max_num


async def is_present(user_id: int):
    async with aiosqlite.connect(DB) as conn:
        query = "SELECT id FROM queue WHERE id = ?"
        cursor: aiosqlite.Cursor
        async with conn.execute(query, (user_id,)) as cursor:
            exists_tp = await cursor.fetchone()
            if exists_tp is not None:
                return True
    return False


async def get_number(user_id: int) -> int:
    async with aiosqlite.connect(DB) as conn:
        query = "SELECT number FROM queue WHERE id = ?"
        cursor: aiosqlite.Cursor
        async with conn.execute(query, (user_id,)) as cursor:
            id_tuple = await cursor.fetchone()
    num = id_tuple[0]
    return num


async def update_queue(num: int) -> None:
    async with aiosqlite.connect(DB) as conn:
        query = "UPDATE queue SET number = number - 1 WHERE number > ?"
        await conn.execute(query, (num,))
        await conn.commit()


async def remove_user(user_id: int) -> None:
    async with aiosqlite.connect(DB) as conn:
        query = "UPDATE queue SET number = NULL, quit = 1 WHERE id = ?"
        await conn.execute(query, (user_id,))
        await conn.commit()


async def reset_queue() -> None:
    async with aiosqlite.connect(DB) as conn:
        query = "DELETE FROM queue"
        await conn.execute(query)
        await conn.commit()


async def show_count() -> int:
    async with aiosqlite.connect(DB) as conn:
        query = "SELECT COUNT(quit) FROM queue WHERE quit = 1"
        cursor: aiosqlite.Cursor
        async with conn.execute(query) as cursor:
            count_tpl = await cursor.fetchone()
            count = count_tpl[0]
    return count


async def is_quit(user_id: int) -> bool:
    async with aiosqlite.connect(DB) as conn:
        query = "SELECT quit FROM queue WHERE id = ?"
        cursor: aiosqlite.Cursor
        async with conn.execute(query, (user_id,)) as cursor:
            quit_tpl = await cursor.fetchone()
            quit = quit_tpl[0]
    if quit == 0:
        return False
    return True


async def update_num(user_id: int, num: int) -> None:
    async with aiosqlite.connect(DB) as conn:
        query = "UPDATE queue SET number = ? WHERE id = ?"
        await conn.execute(query, (num, user_id))
        await conn.commit()


async def reset_quit(user_id: int) -> None:
    async with aiosqlite.connect(DB) as conn:
        query = "UPDATE queue SET quit = 0 WHERE id = ?"
        await conn.execute(query, (user_id,))
        await conn.commit()


async def get_user(num: int) -> str:
    async with aiosqlite.connect(DB) as conn:
        query = "SELECT user_name FROM queue WHERE number = ?"
        cursor: aiosqlite.Cursor
        async with conn.execute(query, (num,)) as cursor:
            name_tpl = await cursor.fetchone()
            if name_tpl[0] is not None:
                user_name = name_tpl[0]
    return user_name


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(find_max())
