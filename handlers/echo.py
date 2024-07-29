from aiogram import Router, types

echo_router = Router()


@echo_router.message()
async def echo(message: types.Message):
    words = message.text.split()
    reversed_words = ' '.join(reversed(words))
    await message.answer(reversed_words)
