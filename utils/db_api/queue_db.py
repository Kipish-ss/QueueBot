import aiosqlite
from data.config import DB
import asyncio
from data.config import min_priority
import sqlite3


async def add_user(user_id: int, user_name: str, number: int, priority: int) -> None:
    async with aiosqlite.connect(DB) as conn:
        query_1 = "INSERT INTO queue(id, user_name, number, priority) VALUES(?, ?, ?, ?)"
        query_2 = "UPDATE queue SET number = number + 1 WHERE priority > ?"
        await conn.execute(query_1, (user_id, user_name, number, priority))
        await conn.execute(query_2, (priority,))
        await conn.commit()


def find_max(priority: int, user_id: int = 0) -> int:
    with sqlite3.connect(DB) as conn:
        if user_id == 0:
            query = "SELECT MAX(number) FROM queue WHERE priority = ?"
            cursor = conn.cursor()
            num_tuple = cursor.execute(query, (priority,)).fetchone()
            cursor.close()
            if num_tuple[0] is not None:
                num = num_tuple[0]
                max_num = num + 1
                return max_num
            else:
                if priority == min_priority:
                    max_num = 1
                    return max_num
            return find_max(priority-1)
        else:
            query = "SELECT MAX(number) FROM queue WHERE priority = ? AND id != ?"
            cursor = conn.cursor()
            num_tuple = cursor.execute(query, (priority, user_id)).fetchone()
            cursor.close()
            if num_tuple[0] is not None:
                num = num_tuple[0]
                max_num = num + 1
                return max_num
            else:
                if priority == min_priority:
                    max_num = 1
                    return max_num
            return find_max(priority - 1, user_id)


async def is_present(user_id: int) -> bool:
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


async def remove_user(user_id: int = 0, num: int = 0) -> None:
    async with aiosqlite.connect(DB) as conn:
        if num > 0:
            query = "UPDATE queue SET number = NULL, quit = 1 WHERE number = ?"
            await conn.execute(query, (num,))
        else:
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


async def update_num(user_id: int, num: int, priority: int, change=False) -> None:
    async with aiosqlite.connect(DB) as conn:
        query_1 = "UPDATE queue SET number = ? WHERE id = ?"
        query_2 = "UPDATE queue SET number = number + 1 WHERE priority > ?"
        await conn.execute(query_1, (num, user_id))
        if change:
            query_3 = "UPDATE queue SET priority = ? WHERE id = ?"
            await conn.execute(query_3, (priority, user_id))
        await conn.execute(query_2, (priority,))
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
            if name_tpl is not None:
                user_name = name_tpl[0]
            else:
                user_name = None
    return user_name


async def get_priority(user_id: int) -> int:
    async with aiosqlite.connect(DB) as conn:
        query = "SELECT priority FROM queue WHERE id = ?"
        cursor: aiosqlite.Cursor
        async with conn.execute(query, (user_id,)) as cursor:
            pr_tpl = await cursor.fetchone()
    priority = pr_tpl[0]
    return priority


async def display_queue():
    async with aiosqlite.connect(DB) as conn:
        query = "SELECT user_name, number, priority FROM queue WHERE number is not NULL ORDER BY number ASC"
        cursor: aiosqlite.Cursor
        async with conn.execute(query) as cursor:
            queue_tpl = await cursor.fetchall()
    if queue_tpl:
        queue_dict = {}
        for elem in queue_tpl:
            queue_dict[elem[0]] = elem[1:]
        return queue_dict
    else:
        return None


async def is_empty() -> bool:
    async with aiosqlite.connect(DB) as conn:
        query = 'SELECT COUNT(*) FROM queue WHERE number is not NULL'
        cursor: aiosqlite.Cursor
        async with conn.execute(query) as cursor:
            count_tpl = await cursor.fetchone()
    if count_tpl[0]:
        return False
    return True


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
