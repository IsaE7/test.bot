import re
from aiogram import types, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import database
import logging
from aiogram.filters import Command


class Survey(StatesGroup):
    name: State = State()
    age: State = State()
    occupation: State = State()
    salary: State = State()


survey_router = Router()


@survey_router.message(Command('start'))
async def start_survey(message: types.Message, state: FSMContext):
    await state.set_state(Survey.name)
    await message.answer("Ваше имя: ")


@survey_router.message(Survey.name)
async def process_name(message: types.Message, state: FSMContext):
    logging.info(f"Received name: {message.text}")
    await state.update_data(name=message.text)
    await state.set_state(Survey.age)
    await message.answer("Ваш возраст (в полном формате): ")


@survey_router.message(Survey.age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) < 0:
        await message.answer("Пожалуйста, введите корректный возраст.")
        return

    age = int(message.text)
    if age < 17:
        await message.answer("Вы слишком молоды для участия в опросе.")
        await state.clear()
        return

    logging.info(f"Received age: {age}")
    await state.update_data(age=age)
    await state.set_state(Survey.occupation)
    await message.answer("Ваша профессия: ")


@survey_router.message(Survey.occupation)
async def process_occupation(message: types.Message, state: FSMContext):
    logging.info(f"Received occupation: {message.text}")
    await state.update_data(occupation=message.text)
    await state.set_state(Survey.salary)
    await message.answer("Ваша зарплата (в формате числа): ")


@survey_router.message(Survey.salary)
async def process_salary(message: types.Message, state: FSMContext):
    if not re.match(r'^\d+(\.\d+)?$', message.text):
        await message.answer("Пожалуйста, введите корректную зарплату.")
        return

    logging.info(f"Received salary: {message.text}")
    await state.update_data(salary=message.text)
    data = await state.get_data()
    await message.answer("Ваши данные были сохранены.")

    await database.execute("""
        INSERT INTO survey (name, age, occupation, salary)
        VALUES (?, ?, ?, ?)
    """, (data['name'], data['age'], data['occupation'], data['salary']))

    await state.clear()
