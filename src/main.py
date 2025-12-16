import asyncio
import json
import os
import random
from typing import Any, Dict, Optional, Tuple

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command

_LOOP: Optional[asyncio.AbstractEventLoop] = None
_BOT: Optional[Bot] = None
_DP: Optional[Dispatcher] = None
MESSAGES = [
    "Вижу мысль о курении. Ты сильнее импульса — сделай вдох, выпей воды, вспомни, зачем тебе свобода. 🚭💪",
    "Импульс к сигарете — всего лишь волна. Пережди её: глубокий вдох, вода, движение. Ты справляешься.",
    "Каждая мысль — шанс стать свободнее. Заметь её, пропусти и выбери себя. Ты на правильном пути.",
    "Ты уже делаешь шаги к чистому воздуху. Дыши, отвлекись, вспомни, ради чего ты бросаешь. Ты молодец.",
    "Желание курить — просто сигнал. Ответь ему заботой: вода, прогулка, несколько глубоких вдохов. Ты контролируешь выбор.",
]

THOUGHT_BUTTON = "Получить мысль"


def _get_token() -> str:
    token = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN or TELEGRAM_BOT_TOKEN is required")
    return token


def _keyboard() -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=THOUGHT_BUTTON)]],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


async def start_handler(message: types.Message) -> None:
    await message.answer(
        "Жми «Получить мысль», чтобы получить поддержку.",
        reply_markup=_keyboard(),
    )


async def thought_handler(message: types.Message) -> None:
    await message.answer(random.choice(MESSAGES), reply_markup=_keyboard())


def setup(dp: Dispatcher) -> None:
    dp.message.register(start_handler, Command("start"))
    dp.message.register(thought_handler, Command("thought"))
    dp.message.register(thought_handler, F.text == THOUGHT_BUTTON)


def _get_app() -> Tuple[Bot, Dispatcher]:
    global _BOT, _DP
    if _BOT is None or _DP is None:
        bot = Bot(_get_token())
        dp = Dispatcher()
        setup(dp)
        _BOT, _DP = bot, dp
    return _BOT, _DP


async def process_update(update_data: Dict[str, Any]) -> None:
    bot, dp = _get_app()
    update = types.Update(**update_data)
    await dp.feed_webhook_update(bot, update)


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    global _LOOP
    if _LOOP is None:
        _LOOP = asyncio.new_event_loop()
        asyncio.set_event_loop(_LOOP)

    body = event.get("body")
    if not body:
        return {"statusCode": 400}

    update_data = json.loads(body)
    _LOOP.run_until_complete(process_update(update_data))
    return {"statusCode": 200}
