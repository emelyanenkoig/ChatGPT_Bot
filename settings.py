# ОСНОВНЫЕ МОДУЛИ
import json
import os
import openai
import aiogram

# МОДУЛИ AIOGRAM
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ParseMode

# МОДУЛИ ДЛЯ DATA BASE
from database import session, User, Base, engine
from sqlalchemy.orm import scoped_session, sessionmaker


# TOKEN SETTINGS
openai.api_key = "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"
bot = Bot(token='5621569001:AAGfx4Gya_BfMZsiT3-gXdKWJ4SO8ulE1bo')

# DISPATCHER
dispatcher = Dispatcher(bot)

# СОЗДАЮТСЯ ТАБЛИЦЫ ЕСЛИ НЕ БЫЛИ СОЗДАНЫ ДО ЭТОГО
Base.metadata.create_all(bind=engine)

# КОНФИГУРАЦИЯ SQLAlchemy
scoped_session(sessionmaker(bind=engine)).configure(bind=engine)

# BAD_ID Определенных пользователей
bad_username = {'felwod': "куница", 'Bipip2': "черный", 'Kankonovs': "конь", 'DanZan_8': "рыба", 'PrinceOfMononoke': "игорян", 'russia2027': "gricenius omskius"}
good_username = {'melaadele': "киса"}