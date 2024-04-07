import asyncio
from typing import Dict, Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from core.db.database_manager import DatabaseManager


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.db_manager = DatabaseManager()
        asyncio.create_task(self.db_manager.connect())

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        data['db_manager'] = self.db_manager
        return await handler(event, data)
