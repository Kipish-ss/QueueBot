from __future__ import annotations
import aiosqlite
from data.config import DB
import asyncio
from data.config import MIN_PRIORITY
import sqlite3
from utils.misc.logging import get_logger
from typing import List, Dict

logger = get_logger()


async def save_msg_id(message_id: int, chat_id: int) -> None:
    async with aiosqlite.connect(DB) as conn:
        query = "INSERT INTO messages(ID, chat_id) VALUES (?, ?)"
        await conn.execute(query, (message_id, chat_id))
        await conn.commit()


async def get_messages(chat_id: int) -> List[int] | None:
    try:
        async with aiosqlite.connect(DB) as conn:
            query = "SELECT ID FROM messages WHERE chat_id = ? ORDER BY ID ASC"
            async with conn.execute(query, (chat_id,)) as cursor:
                id_tpl = await cursor.fetchall()
            if id_tpl:
                id_list = [x[0] for x in id_tpl]
                query = "DELETE FROM messages WHERE chat_id = ?"
                await conn.execute(query, (chat_id,))
                await conn.commit()
            else:
                id_list = None
        return id_list
    except Exception:
        logger.exception("An error occurred while getting messages from the database")


async def add_user(user_id: int, user_name: str, number: int, priority: int) -> None:
    try:
        async with aiosqlite.connect(DB) as conn:
            query_1 = "INSERT INTO queue(id, user_name, number, priority) VALUES(?, ?, ?, ?)"
            query_2 = "UPDATE queue SET number = number + 1 WHERE priority > ?"
            await conn.execute(query_1, (user_id, user_name, number, priority))
            await conn.execute(query_2, (priority,))
            await conn.commit()
    except Exception:
        logger.exception(f"An error occurred while adding {user_name} to the database")


def find_max(priority: int, user_id: int = 0) -> int:
    try:
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
                    if priority == MIN_PRIORITY:
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
                    if priority == MIN_PRIORITY:
                        max_num = 1
                        return max_num
                return find_max(priority - 1, user_id)
    except Exception:
        logger.exception("An error occurred in find_max function")


async def is_present(user_id: int) -> bool:
    try:
        async with aiosqlite.connect(DB) as conn:
            query = "SELECT id FROM queue WHERE id = ?"
            cursor: aiosqlite.Cursor
            async with conn.execute(query, (user_id,)) as cursor:
                exists_tp = await cursor.fetchone()
                if exists_tp is not None:
                    return True
        return False
    except Exception:
        logger.exception(f"An error occurred in is_present function")


async def get_number(user_id: int) -> int:
    try:
        async with aiosqlite.connect(DB) as conn:
            query = "SELECT number FROM queue WHERE id = ?"
            cursor: aiosqlite.Cursor
            async with conn.execute(query, (user_id,)) as cursor:
                id_tuple = await cursor.fetchone()
        num = id_tuple[0]
        return num
    except Exception:
        logger.exception("An error occurred in get_number function")


async def update_queue(num: int) -> None:
    try:
        async with aiosqlite.connect(DB) as conn:
            query = "UPDATE queue SET number = number - 1 WHERE number > ?"
            await conn.execute(query, (num,))
            await conn.commit()
    except Exception:
        logger.exception("An error occurred in update_queue function")


async def remove_user(user_id: int = 0, num: int = 0) -> None:
    try:
        async with aiosqlite.connect(DB) as conn:
            if num > 0:
                query = "UPDATE queue SET number = NULL, quit = 1 WHERE number = ?"
                await conn.execute(query, (num,))
            else:
                query = "UPDATE queue SET number = NULL, quit = 1 WHERE id = ?"
                await conn.execute(query, (user_id,))
            await conn.commit()
    except Exception:
        logger.exception("An error occurred in remove_user function")


async def reset_queue() -> None:
    try:
        async with aiosqlite.connect(DB) as conn:
            query = "DELETE FROM queue"
            await conn.execute(query)
            await conn.commit()
    except Exception:
        logger.exception("An error occurred in reset_queue function")


async def show_count() -> int:
    try:
        async with aiosqlite.connect(DB) as conn:
            query = "SELECT COUNT(quit) FROM queue WHERE quit = 1"
            cursor: aiosqlite.Cursor
            async with conn.execute(query) as cursor:
                count_tpl = await cursor.fetchone()
                count = count_tpl[0]
        return count
    except Exception:
        logger.exception("An error occurred in show_count function")


async def is_quit(user_id: int) -> bool:
    try:
        async with aiosqlite.connect(DB) as conn:
            query = "SELECT quit FROM queue WHERE id = ?"
            cursor: aiosqlite.Cursor
            async with conn.execute(query, (user_id,)) as cursor:
                quit_tpl = await cursor.fetchone()
                quit = quit_tpl[0]
        if quit == 0:
            return False
        return True
    except Exception:
        logger.exception("An error occurred in is_quit function")


async def update_num(user_id: int, num: int, priority: int, change=False) -> None:
    try:
        async with aiosqlite.connect(DB) as conn:
            query_1 = "UPDATE queue SET number = ? WHERE id = ?"
            query_2 = "UPDATE queue SET number = number + 1 WHERE priority > ?"
            await conn.execute(query_1, (num, user_id))
            if change:
                query_3 = "UPDATE queue SET priority = ? WHERE id = ?"
                await conn.execute(query_3, (priority, user_id))
            await conn.execute(query_2, (priority,))
            await conn.commit()
    except Exception:
        logger.exception("An error occurred in update_num function")


async def reset_quit(user_id: int) -> None:
    try:
        async with aiosqlite.connect(DB) as conn:
            query = "UPDATE queue SET quit = 0 WHERE id = ?"
            await conn.execute(query, (user_id,))
            await conn.commit()
    except Exception:
        logger.exception("An error occurred in reset_quit function")


async def get_user(num: int = 0, user_id: int = 0) -> str | None:
    try:
        async with aiosqlite.connect(DB) as conn:
            if num != 0:
                query = "SELECT user_name FROM queue WHERE number = ?"
                param = num
            else:
                query = "SELECT user_name FROM queue WHERE id = ?"
                param = user_id
            cursor: aiosqlite.Cursor
            async with conn.execute(query, (param,)) as cursor:
                name_tpl = await cursor.fetchone()
                if name_tpl is not None:
                    user_name = name_tpl[0]
                else:
                    user_name = None
        return user_name
    except Exception:
        logger.exception("An error occurred in get_user function")


async def get_priority(user_id: int) -> int:
    try:
        async with aiosqlite.connect(DB) as conn:
            query = "SELECT priority FROM queue WHERE id = ?"
            cursor: aiosqlite.Cursor
            async with conn.execute(query, (user_id,)) as cursor:
                pr_tpl = await cursor.fetchone()
        priority = pr_tpl[0]
        return priority
    except Exception:
        logger.exception("An error occurred in get_priority function")


async def display_queue() -> Dict[str, (int, int)] | None:
    try:
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
    except Exception:
        logger.exception("An error occurred in display_queue function")


async def is_empty() -> bool:
    try:
        async with aiosqlite.connect(DB) as conn:
            query = 'SELECT COUNT(*) FROM queue WHERE number is not NULL'
            cursor: aiosqlite.Cursor
            async with conn.execute(query) as cursor:
                count_tpl = await cursor.fetchone()
        if count_tpl[0]:
            return False
        return True
    except Exception:
        logger.exception("An error occurred in is_empty function")


async def set_queue_id() -> None:
    try:
        async with aiosqlite.connect(DB) as conn:
            query = 'INSERT INTO stats(queue_id) ' \
                    'SELECT CASE ' \
                    'WHEN MAX(queue_id) IS NULL THEN 1 ' \
                    'ELSE  MAX(queue_id)+1 ' \
                    'END FROM stats'
            await conn.execute(query)
            await conn.commit()
    except Exception:
        logger.exception("An error occurred in set_queue_id function")


async def is_deleted() -> bool:
    try:
        async with aiosqlite.connect(DB) as conn:
            query = 'SELECT is_deleted FROM stats WHERE queue_id = (SELECT MAX(queue_id) FROM stats)'
            async with conn.execute(query) as cursor:
                is_deleted_tpl = await cursor.fetchone()
        if is_deleted_tpl is not None:
            deleted = is_deleted_tpl[0] == 1
        else:
            deleted = True
        return deleted
    except Exception:
        logger.exception("An error occurred in is_deleted function")


async def set_queue_info(quit_num: int, curr_date: str) -> None:
    try:
        query = 'UPDATE stats SET quit_num = ?, date_deleted = ?, is_deleted = 1 ' \
                'WHERE queue_id = (SELECT MAX(queue_id) FROM stats)'
        async with aiosqlite.connect(DB) as conn:
            await conn.execute(query, (quit_num, curr_date))
            await conn.commit()
    except Exception:
        logger.exception("An error occurred in set_queue_info function")


async def delete_queue_info() -> None:
    try:
        async with aiosqlite.connect(DB) as conn:
            query = "DELETE FROM stats WHERE queue_id = (SELECT MAX(queue_id) FROM stats)"
            await conn.execute(query)
            await conn.commit()
    except Exception:
        logger.exception("An error occurred in delete_queue_info function")


async def get_avg_quit_num() -> int:
    try:
        async with aiosqlite.connect(DB) as conn:
            query = "SELECT AVG(quit_num) FROM stats WHERE is_deleted = 1"
            async with conn.execute(query) as cursor:
                avg_quit_num_tpl = await cursor.fetchone()
        if avg_quit_num_tpl is not None:
            avg_quit_num = avg_quit_num_tpl[0]
        else:
            avg_quit_num = 0
        return avg_quit_num
    except Exception:
        logger.exception("An error occurred in get_avg_quit_num function")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(is_deleted())
