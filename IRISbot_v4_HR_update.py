import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from config import TOKEN, CHANNEL_ID, CHANNEL_ID_AXO, CHANNEL_ID_HR, NEWS_CHANNEL_ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# States
class Form(StatesGroup):
    no_state = State()
    task_executor = State()
    start = State()
    department = State()  # Will be represented in storage as 'Form:department'
    consult = State()
    default_error = State()  # Will be represented in storage as 'Form:default_error'
    unusual_error = State()  # Will be represented in storage as 'Form:unusual_error'
    photo = State()
    get_fio = State()

class Specific(StatesGroup):
    internet = State()
    shit = State()
    ass = State()

delete_kb = types.ReplyKeyboardRemove()


async def bot_restart():
    await bot.send_message(CHANNEL_ID_AXO, "Бот Айрис (@IRIS_IT_Bot) была перезагружена. Для возобновления работы нужно будет написать ОТМЕНА в диалоге с ботом. \n\n⭐Приятного рабочего дня!⭐")

new_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
new_kb.add("У меня есть заявка", "Отмена")

task_executor_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
task_executor_kb.add("АХО", "IT", "HR", "Отмена")

department_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
department_kb.add("АХО","ДП","КС","СО","ОП","HR","Маркетинг","ФИН","ДСО", "Отмена")

common_problem_aho_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
common_problem_aho_kb.add("Необходимо заказать", "Сломалось оборудование", "Бытовые работы","Нет в списке", "Отмена")

common_problem_hr_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
common_problem_hr_kb.add("Увольнение", "Приём", "Отпуск", "Нет в списке (HR)", "Отмена")

common_problem_it_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
common_problem_it_kb.add("Интернет", "CRM", "Компьютер", "Принтер", "Телефония", "ПАУ", "WORK", "Нет в списке", "Отмена")

@dp.message_handler(state='*', commands='Отмена')
@dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Отменено. Нажмите или напишите /start, чтобы начать заново.', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state='*', commands='/creator')
@dp.message_handler(Text(equals='/creator', ignore_case=True), state='*')
async def creator_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Вы воспользовались командой [/creator]. Мой создатель - @stygianyurei, в узких кругах известный как Юлий Учиха, а также в ещё более узких - Benedict Eurico. Он крайне рад, что вы разговариваете с Айрис, то есть со мной. Я - его первый хуманизированный бот и он очень мною дорожит.\n\n/start?', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state='*', commands='/help')
@dp.message_handler(Text(equals='/help', ignore_case=True), state='*')
async def help_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action and request help
    """
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Нажмите или напишите /start, чтобы начать заново. В случае, если я не смогла вам помочь, прошу меня извинить, я еще очень молодой бот и мне еще столько нужно узнать. Но я обещаю исправиться! А пока - обращайтесь к @stygianyurei или @BKITEGOR. Но, может быть, все же попробуем вместе снова? /start?', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands='start')
async def process_greeting(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.task_executor.set()

    await message.answer("Добрый день! Я - бот-помощник <b>Айрис</b>. С моей помощью вы сможете составить и отправить вашу заявку. Нажмите на кнопку <b>[У меня есть заявка]</b>, чтобы оставить заявку для отдела IT, отдела АХО или отдела HR. \n\n<b>Внимание!</b>\n1) Все введеные вами данные будут переданы в заявке!\n2) Если в тексте заявки ваш ник отображается как @None, зайдите в [Настройки] - [Изменить профиль] - [Имя пользователя], и добавьте свой ник, а затем заново отправьте вашу заявку.\n\nВы можете в любой момент нажать или написать <b>[Отмена]</b>, чтобы отменить незаконченную заявку или перезагрузить меня, или написать /help, если вас не устроит моя помощь.\n\nПриступим?", reply_markup=new_kb)

@dp.message_handler(state=Form.task_executor)
async def process_task_executor(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['start_choice'] = message.text

    if data['start_choice'] == "У меня есть заявка":
        await Form.next()
        await message.reply("В какой отдел адресована заявка?", reply_markup=task_executor_kb)
    elif data['start_choice'] == "Отмена":
        await message.reply("Отмена")
    else:
        await state.finish()
        await message.reply('Ошибка. Выбирайте только из пунктов меню. Нажмите или напишите /start, чтобы начать заново.', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=Form.start)
async def process_task_executor(message: types.Message, state: FSMContext):
    """
    Process task executor
    """
    async with state.proxy() as data:
        data['task_executor'] = message.text
    
    if data['task_executor'] == "IT":
        await message.answer("Выберите отдел, в котором вы работаете.", reply_markup=department_kb)
        await Form.next()
    elif data['task_executor'] == "АХО":
        await message.answer("Выберите отдел, в котором вы работаете.", reply_markup=department_kb)
        await Form.next()
    elif data['task_executor'] == "HR":
        await message.answer("Выберите причину вашего обращения.", reply_markup=common_problem_hr_kb)
        await Form.default_error.set()
    else:
        await state.finish()
        await message.reply('Ошибка. Выбирайте только из пунктов меню. Нажмите или напишите /start, чтобы начать заново.', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=Form.department)
async def process_department(message: types.Message, state: FSMContext):
    """
    Process department
    """
    async with state.proxy() as data:
        data['department'] = message.text

    if data['department'] == "АХО":
        await message.reply("Так и запишем. А теперь - напишите номер своего CONSULT (номер вашего ПК). Если вы работаете с домашнего/личного компьютера, напишите 0.", reply_markup=delete_kb)
        await Form.next()
    elif data['department'] == "ДП":
        await message.reply("Так и запишем. А теперь - напишите номер своего CONSULT (номер вашего ПК). Если вы работаете с домашнего/личного компьютера, напишите 0.", reply_markup=delete_kb)
        await Form.next()
    elif data['department'] == "КС": 
        await message.reply("Так и запишем. А теперь - напишите номер своего CONSULT (номер вашего ПК). Если вы работаете с домашнего/личного компьютера, напишите 0.", reply_markup=delete_kb)
        await Form.next()
    elif data['department'] == "СО":
        await message.reply("Так и запишем. А теперь - напишите номер своего CONSULT (номер вашего ПК). Если вы работаете с домашнего/личного компьютера, напишите 0.", reply_markup=delete_kb)
        await Form.next()
    elif data['department'] == "ОП":
        await message.reply("Так и запишем. А теперь - напишите номер своего CONSULT (номер вашего ПК). Если вы работаете с домашнего/личного компьютера, напишите 0.", reply_markup=delete_kb)
        await Form.next()
    elif data['department'] == "HR":
        await message.reply("Так и запишем. А теперь - напишите номер своего CONSULT (номер вашего ПК). Если вы работаете с домашнего/личного компьютера, напишите 0.", reply_markup=delete_kb)
        await Form.next()
    elif data['department'] == "Маркетинг":
        await message.reply("Так и запишем. А теперь - напишите номер своего CONSULT (номер вашего ПК). Если вы работаете с домашнего/личного компьютера, напишите 0.", reply_markup=delete_kb)
        await Form.next()
    elif data['department'] == "ФИН": 
        await message.reply("Так и запишем. А теперь - напишите номер своего CONSULT (номер вашего ПК). Если вы работаете с домашнего/личного компьютера, напишите 0.", reply_markup=delete_kb)
        await Form.next()
    elif data['department'] == "ДСО":
        await message.reply("Так и запишем. А теперь - напишите номер своего CONSULT (номер вашего ПК). Если вы работаете с домашнего/личного компьютера, напишите 0.", reply_markup=delete_kb)
        await Form.next()
    else:
        await state.finish()
        await message.reply('Ошибка. Выбирайте только из пунктов меню. Нажмите или напишите /start, чтобы начать заново.', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=Form.consult)
async def process_consult(message: types.Message, state: FSMContext):
    """
    Process consult
    """
    async with state.proxy() as data:
        data['consult'] = message.text

    consult_number = data['consult']

    await Form.next()

    if data['task_executor'] == "IT" and consult_number.isnumeric():
        await message.reply("Хорошо. Далее - выберите тип проблемы из предложенных.", reply_markup=common_problem_it_kb)
    elif data['task_executor'] == "АХО" and consult_number.isnumeric():
        await message.reply("Хорошо. Далее - выберите тип проблемы из предложенных.", reply_markup=common_problem_aho_kb)
    else:
        await state.finish()
        await message.reply('Ошибка. Используйте только числа в этом поле. Нажмите или напишите /start, чтобы начать заново.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.default_error)
async def process_type(message: types.Message, state: FSMContext):
    """
    Process error type
    """
    async with state.proxy() as data:
        data['default_error'] = message.text

    if message.text == "Интернет":
        await Form.unusual_error.set()
        await message.reply("Принято! Теперь введите текст заявки.", reply_markup=delete_kb)
    elif message.text =="CRM":
        await Form.unusual_error.set()
        await message.reply("Возможно, я смогу вам помочь самостоятельно. Если проблема не связана с введением логина и пароля, попробуйте вначале закрыть браузер, а затем через 10 секунд открыть снова. Если это не поможет, попробуйте перезагрузить компьютер.\n\n<b>(Внимание! Не забудьте сохранить важные файлы и вкладки!)</b>\n\nВ случае, если это вам помогло - отмените заявку (Отмена) и спокойно продолжайте работу или напишите, что вам помогла Айрис, мне будет очень приятно.\n\nЕсли не помогло - опишите вашу проблему подробно для наших системных администраторов в поле ввода.", reply_markup=delete_kb)
    elif message.text =="Компьютер":
        await Form.unusual_error.set()
        await message.reply("Возможно, я смогу вам помочь самостоятельно. Попробуйте просто перезагрузить компьютер. Также постарайтесь не открывать больше 10 вкладок в браузере и постарайтесь не иметь большое количество одновременно работающих программ - если эти инструкции не соблюдать, то это может привести к медленной работе всего компьютера.\n\n<b>(Внимание! Не забудьте сохранить важные файлы и вкладки!)</b>\n\nВ случае, если это вам помогло - отмените заявку (Отмена) и спокойно продолжайте работу или напишите, что вам помогла Айрис, мне будет очень приятно.\n\nЕсли не помогло - опишите вашу проблему подробно для наших системных администраторов в поле ввода.", reply_markup=delete_kb)
    elif message.text =="Принтер":
        await Form.unusual_error.set()
        await message.reply("Хорошо. Теперь введите текст заявки.", reply_markup=delete_kb)
    elif message.text =="Телефония":
        await Form.unusual_error.set()
        await message.reply("Услышала вас. Теперь введите текст заявки.", reply_markup=delete_kb)
    elif message.text =="ПАУ":
        await Form.unusual_error.set()
        await message.reply("Окей. Теперь введите текст заявки.", reply_markup=delete_kb)
    elif message.text =="WORK":
        await Form.unusual_error.set()
        await message.reply("Принято. Теперь введите текст заявки.", reply_markup=delete_kb)
    elif message.text =="Нет в списке":
        await Form.unusual_error.set()
        await message.reply("Поняла вас. Теперь введите текст заявки.", reply_markup=delete_kb)
    elif message.text =="Необходимо заказать":
        await Form.unusual_error.set()
        await message.reply("Что-то новенькое? Введите текст заявки.", reply_markup=delete_kb)
    elif message.text =="Сломалось оборудование":
        await Form.unusual_error.set()
        await message.reply("Больше всего не люблю, когда что-то ломается. Введите текст заявки.", reply_markup=delete_kb)
    elif message.text =="Бытовые работы":
        await Form.unusual_error.set()
        await message.reply("Сделаем всё мигом! Теперь введите текст заявки.", reply_markup=delete_kb)
    elif message.text =="Увольнение":
        await Form.get_fio.set()
        await message.reply("Оу... Поняла. Введите ФИО увольняемого сотрудника и его отдел.", reply_markup=delete_kb)
    elif message.text =="Приём":
        await Form.get_fio.set()
        await message.reply("Новая кровь, свежий взгляд! Введите ФИО зачисляемого сотрудника и его отдел.", reply_markup=delete_kb)
    elif message.text =="Отпуск":
        await Form.get_fio.set()
        await message.reply("Хороший отдых помогает хорошо работать. Введите ФИО уходящего в отпуск сотрудника и его отдел.", reply_markup=delete_kb)
    elif message.text =="Нет в списке (HR)":
        await Form.get_fio.set()
        await message.reply("Хм. Окей. Введите ФИО и отдел сотрудника, о котором создается эта заявка. Если заявка создается не о сотруднике, напишите 0.", reply_markup=delete_kb)
    else:
        await state.finish()
        await message.reply('Ошибка. Выбирайте только из пунктов меню. Нажмите или напишите /start, чтобы начать заново.', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=Form.unusual_error)
async def process_data(message: types.Message, state: FSMContext):
    """
    Process data
    """
    async with state.proxy() as data:
        data['unusual_error'] = message.text

    user_name = str(message.from_user.username)
    
    if data['task_executor'] == 'IT': 
        await bot.send_message(CHANNEL_ID, '<b>Заявка от юзера:</b> @' + user_name + '\n\n<b>ФИО:</b> ' + message.from_user.full_name + '\n\n<b>Для:</b> ' + data['task_executor'] + '\n\n<b>CONSULT:</b> ' + data['consult'] + '\n\n<b>Из отдела:</b> ' + data['department'] + '\n\n<b>Тип заявки:</b> ' + data['default_error'] + '\n\n<b>Текст заявки:</b> ' + data['unusual_error'])
    elif data['task_executor'] == 'АХО':
        await bot.send_message(CHANNEL_ID_AXO, '<b>Заявка от сотрудника:</b> @' + user_name + '\n\n<b>ФИО:</b> ' + message.from_user.full_name + '\n\n<b>Для:</b> ' + data['task_executor'] + '\n\n<b>CONSULT:</b> ' + data['consult'] + '\n\n<b>Из отдела:</b> ' + data['department'] + '\n\n<b>Тип заявки:</b> ' + data['default_error'] + '\n\n<b>Текст заявки:</b> ' + data['unusual_error'])
    elif data['task_executor'] == 'HR':
        if data['default_error'] == "Увольнение":
            await bot.send_message(CHANNEL_ID_AXO, '<b>Заявка от сотрудника:</b> @' + user_name + '\n\n<b>ФИО:</b> ' + message.from_user.full_name + '\n\n<b>Для:</b> ' + data['task_executor'] + '\n\n<b>Тип заявки:</b> ' + data['default_error'] + '\n\n<b>ФИО и отдел сотрудника:</b> ' + data['get_fio'] + '\n\n<b>Текст заявки:</b> ' + data['unusual_error'])
            await bot.send_message(CHANNEL_ID, '<b>Заявка от сотрудника:</b> @' + user_name + '\n\n<b>ФИО:</b> ' + message.from_user.full_name + '\n\n<b>Для:</b> ' + data['task_executor'] + '\n\n<b>Тип заявки:</b> ' + data['default_error'] + '\n\n<b>ФИО и отдел сотрудника:</b> ' + data['get_fio'] + '\n\n<b>Текст заявки:</b> ' + data['unusual_error'])
        elif data['default_error'] == "Приём":
            await bot.send_message(CHANNEL_ID_AXO, '<b>Заявка от сотрудника:</b> @' + user_name + '\n\n<b>ФИО:</b> ' + message.from_user.full_name + '\n\n<b>Для:</b> ' + data['task_executor'] + '\n\n<b>Тип заявки:</b> ' + data['default_error'] + '\n\n<b>ФИО и отдел сотрудника:</b> ' + data['get_fio'] + '\n\n<b>Текст заявки:</b> ' + data['unusual_error'])
            await bot.send_message(CHANNEL_ID, '<b>Заявка от сотрудника:</b> @' + user_name + '\n\n<b>ФИО:</b> ' + message.from_user.full_name + '\n\n<b>Для:</b> ' + data['task_executor'] + '\n\n<b>Тип заявки:</b> ' + data['default_error'] + '\n\n<b>ФИО и отдел сотрудника:</b> ' + data['get_fio'] + '\n\n<b>Текст заявки:</b> ' + data['unusual_error'])
        elif data['default_error'] == "Отпуск":
            await bot.send_message(CHANNEL_ID_AXO, '<b>Заявка от сотрудника:</b> @' + user_name + '\n\n<b>ФИО:</b> ' + message.from_user.full_name + '\n\n<b>Для:</b> ' + data['task_executor'] + '\n\n<b>Тип заявки:</b> ' + data['default_error'] + '\n\n<b>ФИО и отдел сотрудника:</b> ' + data['get_fio'] + '\n\n<b>Текст заявки:</b> ' + data['unusual_error'])
    await Form.task_executor.set()
    if user_name == 'None':
        await bot.send_message(message.from_user.id, user_name)
        await bot.send_message(message.from_user.id, '<b>ОШИБКА!</b>\n\nВаш ник отображается как @None, зайдите в [Настройки] - [Изменить профиль] - [Имя пользователя], и добавьте свой ник, а затем заново отправьте вашу заявку.', reply_markup=new_kb)
    else:
        if data['task_executor'] == 'IT':
            await message.reply('Ваша заявка принята. IT отдел займется вашей проблемой в ближайшее время.', reply_markup=new_kb)
            await bot.send_message(message.from_user.id, 'Вот текст вашей заявки: \n\n<b>Заявка от пользователя:</b> @' + user_name + '\n\n<b>ФИО:</b> ' + message.from_user.full_name + '\n\n<b>Для:</b> ' + data['task_executor'] + '\n\n<b>CONSULT:</b> ' + data['consult'] + '\n\n<b>Из отдела:</b> ' + data['department'] + '\n\n<b>Тип заявки:</b> ' + data['default_error'] + '\n\n<b>Текст заявки:</b> ' + data['unusual_error'])
            await bot.send_message(message.from_user.id, "Если вам снова понадобится помощь, нажмите на кнопку <b>[У меня проблема!]</b>, чтобы оставить новую заявку.")
        elif data['task_executor'] == 'АХО':
            await message.reply('Ваша заявка принята. Отдел АХО займется вашей проблемой в ближайшее время.', reply_markup=new_kb)
            await bot.send_message(message.from_user.id, 'Вот текст вашей заявки: \n\n<b>Заявка от пользователя:</b> @' + user_name + '\n\n<b>ФИО:</b> ' + message.from_user.full_name + '\n\n<b>Для:</b> ' + data['task_executor'] + '\n\n<b>CONSULT:</b> ' + data['consult'] + '\n\n<b>Из отдела:</b> ' + data['department'] + '\n\n<b>Тип заявки:</b> ' + data['default_error'] + '\n\n<b>Текст заявки:</b> ' + data['unusual_error'])
            await bot.send_message(message.from_user.id, "Если вам снова понадобится помощь, нажмите на кнопку <b>[У меня проблема!]</b>, чтобы оставить новую заявку.")
        elif data['task_executor'] == 'HR':
            await message.reply('Ваша заявка принята. Отдел HR займется вашей проблемой в ближайшее время.', reply_markup=new_kb)
            await bot.send_message(message.from_user.id, 'Вот текст вашей заявки: \n\n<b>Заявка от пользователя:</b> @' + user_name + '\n\n<b>ФИО:</b> ' + message.from_user.full_name + '\n\n<b>Для:</b> ' + data['task_executor'] + '\n\n<b>Тип заявки:</b> ' + data['default_error'] + '\n\n<b>ФИО и отдел сотрудника:</b> ' + data['get_fio'] + '\n\n<b>Текст заявки:</b> ' + data['unusual_error'])
            await bot.send_message(message.from_user.id, "Если вам снова понадобится помощь, нажмите на кнопку <b>[У меня проблема!]</b>, чтобы оставить новую заявку.")

@dp.message_handler(state=Form.get_fio)
async def get_fio(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['get_fio'] = message.text

    await message.answer("Принято! А теперь введите информацию по этой заявке.", reply_markup=delete_kb)

    await Form.unusual_error.set()


if __name__ == '__main__':
    executor.start(dp, bot_restart())
    executor.start_polling(dp, skip_updates=True)