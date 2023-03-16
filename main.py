from settings import *


# Основная функция для получения ответа от ChatGPT-API
async def get_response(user_message):
    user_id = str(user_message.chat.id)

    # Создаем файл для хранения данных
    filename = f"{user_id}.json"

    # Проверяем существование файла и наличие сообщения в нем
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            if user_message.text in data:
                return data[user_message.text]

    # Если файл не существует или не содержит сообщение пользователя, то генерируем через  GPT ответ
    prompt = f"{user_message.text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Передаем ответ в переменную answer
    answer = response.choices[0].text.strip()

    # Обновляем данные data[сообщение пользователя] = [answer]
    # Еще раз проверяем существует ли файл
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    else:
        data = {}

    # Словарь наполняется данными
    data[user_message.text] = answer
    with open(filename, "w") as f:
        json.dump(data, f)

    # Возвращаем ответ
    return answer


# The function to handle the '/start' command
@dispatcher.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.chat.id
    user_name = message.chat.username
    user = session.query(User).filter(User.chat_id == user_id).first()  # Если пользователь существует в базе данных

    # Если пользователь не существует в базе данных
    if not user:
        # Добавляем в базу
        user = User(chat_id=user_id, username=message.chat.username)
        session.add(user)
        session.commit()

        if user_name in bad_username:
            await bot.send_message(text=f"Я был запрограммирован так, чтобы на расстоянии вычислять пидарасов", chat_id=user_id)
            await bot.send_message(text=f"че ты, {bad_username[user_name]}, походу нашелся педик))", chat_id=user_id)
            await bot.send_message(text=f"Пиши свой запрос, поищу что-нибудь:", chat_id=user_id)
        elif user_name in good_username:
            await bot.send_message(text=f"Привет, {good_username[user_name]})", chat_id=user_id)
            await bot.send_message(text="Кстати, когда пойдем на концерт классической музыки??", chat_id=user_id)
            await bot.send_message(text="Вот слушал этот плейлист, пока делал бота:\n"
                                        "https://music.yandex.ru/users/emelyanenkoig/playlists/1020?utm_medium"
                                        "=copy_link",
                                   chat_id=user_id)
            await bot.send_message(text=f"Пиши свой запрос, поищу что-нибудь:", chat_id=user_id)
        else:
            await message.reply(
                "Здравствуйте, отправьте сообщение, чтобы я ответил на ваш запрос.")

    # Если пользователь уже есть в базе данных, то
    else:
        if user_name in bad_username:
            await bot.send_message(text="Ооо пидарас прибыл", chat_id=user_id)
            await bot.send_message(text=f"че ты {bad_username[user_name]})", chat_id=user_id)

        elif user_name in good_username:
            await bot.send_message(text="Привет, моя хорошая", chat_id=user_id)
            await bot.send_message(text="Плейлистик:\n"
                                        "https://music.yandex.ru/users/emelyanenkoig/playlists/1020?utm_medium=copy_link",
                                   chat_id=user_id)
        await message.reply(
            "Случайный факт, только для тебя ..")

        prompt = f"Случайный факт о природе:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        ).choices[0].text.strip()
        await bot.send_message(text=response, chat_id=user_id)
        await bot.send_message(text=f"Пиши свой запрос, поищу что-нибудь:", chat_id=user_id)


# Функция для стоп команды
@dispatcher.message_handler(commands=['stop'])
async def stop_command(message: types.Message):
    user_id = str(message.chat.id)
    user_name = str(message.chat.username)
    filename = f"{user_id}.json"

    # Если файл с данными о пользователе существует, то удали
    if os.path.exists(filename):
        os.remove(filename)

    # Send a goodbye message
    if user_name in bad_username:
        await bot.send_message(text="нахуй отсюда вышел\nче ты))", chat_id=user_id)

    elif user_name in good_username:
        await bot.send_message(text="цЫлуYOU", chat_id=user_id)

    await message.reply("Отключился.")


# Принимает входящие сообщения
@dispatcher.message_handler()
async def chat_command(message: types.Message):
    user_message = message.text

    # Use GPT-3 to generate a response to the user's message
    response = await get_response(message)

    if response is not None and len(response.strip()) > 0:
        # If a response was generated, send it back to the user
        await message.reply(response)
    else:
        # If no response was generated, send an apology message
        await message.reply("Извините, я вообще ниче не понял")


if __name__ == '__main__':
    # Старт Бота
    executor.start_polling(dispatcher)
