from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from mimetypes import init

from pip._internal.vcs import git


class TestState(StatesGroup):
    Waiting_for_first_voice = State()
    Waiting_for_second_voice = State()
    Waiting_for_third_voice = State()
    Waiting_for_fourth_voice = State()

class AdminState(StatesGroup):
    Waiting_for_user_id = State()
    Waiting_for_message = State()

bot = Bot(token='6332956391:AAH8fEw597EqewnLwMj64XNTlgOqfXRxpCo')
dp = Dispatcher(bot, storage=MemoryStorage())



@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    inline_kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Начать', callback_data='button_clicked')
    inline_kb.add(btn)
    print(f"User ID = {message.from_user.id}")
    await bot.send_message(message.chat.id,
                           'Тебе предстоит пройти устный тест на определение навыка разговорного английского🌸\n\n'
                           '🖇️Инструкция:\n\n'
                           '▫️<b>Дай развернутые ответы</b> на 4 сообщения. <b>Вопросы</b> будут появляться последовательно.\n\n'
                           '▫️1 сообщение с вопросами = <b>1 голосовой ответ</b>, итого 4 ответа.\n\n'
                           '▫️<b>Рекомендуемая длительность</b> каждого голосового <b>не более 2 минут</b>.\n\n'
                           '▫️<b>Если не можешь ответить</b> на какой-то из вопросов, <b>произнеси</b> фразу <b>“I don’t know”</b>.\n\n'
                           '▫️Не волнуйся, отвечай в своем темпе и <b>good luck</b>))\n\n'
                           '<b>Нажми на кнопку ниже, чтобы начать</b>.',
                           parse_mode = 'html', reply_markup=inline_kb)


@dp.callback_query_handler(lambda c: c.data == 'button_clicked')
async def on_button_click(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, 'What’s your name? How’re you?')
    await TestState.Waiting_for_first_voice.set()

@dp.message_handler(state=TestState.Waiting_for_first_voice, content_types=['voice'])
async def process_first_voice(message: types.Message, state: FSMContext):
    await state.update_data(
        first_voice=message.voice.file_id
    )
    await bot.send_message(message.chat.id, 'What do you usually do in your free time?')
    await TestState.next()

@dp.message_handler(state=TestState.Waiting_for_second_voice, content_types=['voice'])
async def process_second_voice(message: types.Message, state: FSMContext):
    await state.update_data(
        second_voice=message.voice.file_id
    )
    await bot.send_message(message.chat.id, 'How long have you been studying English? (+ tell me about your experience of learning English).')
    await TestState.next()

@dp.message_handler(state=TestState.Waiting_for_third_voice, content_types=['voice'])
async def process_third_voice(message: types.Message, state: FSMContext):
    await state.update_data(
        third_voice=message.voice.file_id
    )
    await bot.send_message(message.chat.id, 'What’re the problems associated with learning English at an upper-intermediate or advanced level? How can you continue to make progress?')
    await TestState.next()

# Обработчик голосового ответа
@dp.message_handler(state=TestState.Waiting_for_fourth_voice, content_types=['voice'])
async def process_fourth_voice(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(chat_id=1499426060, text = f'Проверь уровень пользователя {message.from_user.username} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.id}')
    await bot.send_voice(chat_id=1499426060, voice=data.get('first_voice'), caption='Первое аудио от пользователя')
    await bot.send_voice(chat_id=1499426060, voice=data.get('second_voice'), caption='Второе аудио от пользователя')
    await bot.send_voice(chat_id=1499426060, voice=data.get('third_voice'), caption='Третье аудио от пользователя')
    await bot.send_voice(chat_id=1499426060, voice=message.voice.file_id, caption='Четвертое аудио от пользователя')
    await state.finish()
    inline_kb = types.InlineKeyboardMarkup()
    btn_chek = types.InlineKeyboardButton('ЧЕК-ЛИСТ', callback_data='btn_chek')
    btn_tel = types.InlineKeyboardButton('ТГ-КАНАЛ', callback_data='btn_tel')
    btn_ind = types.InlineKeyboardButton('ПРОМОКОД НА ИНДИВИДУАЛЬНЫЕ', callback_data='btn_ind')
    btn_group = types.InlineKeyboardButton('ПРОМОКОД НА ГРУППОВЫЕ', callback_data='btn_group')
    inline_kb.add(btn_chek, btn_tel, btn_ind, btn_group)
    await bot.send_message(message.chat.id,
                           'У тебя получилось🤩\n\n'
                           '‼️<b>Ответ</b> придет <b>в рабочее время после проверки</b> преподавателем Елизаветой @english_liza.\n\n'
                           '✅ За участие в тестировании дарю тебе <b>промокод</b> на скидку <b>10% на одно индивидуальное занятие</b> с Елизаветой.\n\n'
                           'Нажми на кнопку <b>«ПРОМОКОД НА ИНДИВИДУАЛЬНЫЕ»</b> ниже.🌸\n\n'
                           '✅ Также ты получаешь <b>промокод на скидку 10%</b> на абонемент <b>на 4 групповых занятия</b>.\n\n'
                           'Групповые занятия:\n\n'
                           '💎 отличное средство для избавления от языкового барьера; \n'
                           '💎 групповые домашние задания для быстрого повышения уровня разговорного английского;\n'
                           '💎 расширение словарного запаса современными выражениями; \n'
                           '💎 разнообразие активностей во время занятий.\n\n'
                           'Нажими на кнопку <b>«ПРОМОКОД НА ГРУППОВЫЕ» ниже.🌸</b> ниже.\n\n'
                           '✅ Забирай <b>бесплатный чек-лист</b> «20 разговорных выражений, чтобы звучать как носитель 🇺🇸».\n\n'
                           'Нажми на кнопку <b>«ЧЕК-ЛИСТ»</b> ниже.🌸',
                           parse_mode = 'html', reply_markup=inline_kb)

@dp.callback_query_handler(lambda c: c.data == 'btn_chek')
async def on_button_click(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, 'https://t.me/english_liza/180')

@dp.callback_query_handler(lambda c: c.data == 'btn_tel')
async def on_button_click(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, 'https://t.me/english_liza')


@dp.callback_query_handler(lambda c: c.data == 'btn_ind')
async def on_button_click(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, 'Твой промокод на индивидуальные занятия INDZN10. Напиши его мне в лс @Lizaveta_Rozhkova или на сайте во время записи на занятие.')


@dp.callback_query_handler(lambda c: c.data == 'btn_group')
async def on_button_click(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, 'Твой промокод на групповые занятия GRPZN10. Напиши его мне в лс @Lizaveta_Rozhkova или на сайте во время записи на занятие.')

@dp.message_handler(state='*', user_id=1499426060)
async def admin_handler(message: types.Message, state: FSMContext):
    if not str(await state.get_state()):
        await AdminState.Waiting_for_user_id.set()
    else:
        await state.update_data(admin_id=message.from_user.id)

        if message.text.isdigit():
            await state.update_data(user_id=message.text)
            await bot.send_message(message.from_user.id, 'Введите сообщение для пользователя')
            await AdminState.next()
        else:
            data = await state.get_data()
            user_id = data.get('user_id')

            if user_id:
                # Отправляем сообщение пользователю
                await bot.send_message(chat_id=user_id, text=message.text)
                await state.finish()
            else:
                await bot.send_message(message.from_user.id, 'Вы ввели неверный ID, попробуйте снова')

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
