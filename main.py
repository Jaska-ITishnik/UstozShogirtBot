import asyncio
import json
import logging
import sys
from os import getenv

# pip install Babel
# pip instal aiogram[i18n]
# sudo apt-get install gettext

from aiogram import Bot, Dispatcher, html, F, BaseMiddleware
from aiogram.enums import ParseMode, ChatType
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, KeyboardButton, CallbackQuery, InlineKeyboardButton, BotCommand
from aiogram.utils.i18n import I18n, FSMI18nMiddleware
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from redis.asyncio import Redis
from redis_dict import RedisDict
from aiogram.utils.i18n import lazy_gettext as __  # FOR FILTERS
from aiogram.utils.i18n import gettext as _  # INSIDE FILTERS


TOKEN = "7195553632:AAHsvU0i7N_o-CfBD8z3PKiCal3kNGbdWm4"
redis = Redis()
storage = RedisStorage(redis=redis)
dp = Dispatcher(storage=storage)
database = RedisDict('ish_uchun_malumot')

ADMIN = 6297575730,
CHANNEL_ID = -1002023267672

class Questions(StatesGroup):
    in_addition = State()
    work_time = State()
    office_name = State()
    locale = State()
    name = State()
    username = State()
    age = State()
    technology = State()
    phone = State()
    place = State()
    price = State()
    profession = State()
    time_to_talk = State()
    aim = State()
    who_needs = State()
    current_user_id = State()


def menu_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text=_('Sherik kerak')),
        KeyboardButton(text=_('Ish joyi kerak')),
        KeyboardButton(text=_('Hodim kerak')),
        KeyboardButton(text=_('Ustoz kerak')),
        KeyboardButton(text=_('Shogirt kerak'))
    )
    return rkb.adjust(2, repeat=True)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    ikb = InlineKeyboardBuilder()
    ikb.add(
        InlineKeyboardButton(text='Uz🇺🇿', callback_data='lang_uz'),
        InlineKeyboardButton(text='En🇬🇧', callback_data='lang_en')
    )
    await message.answer(_('Tilni tanlang'), reply_markup=ikb.as_markup())

@dp.callback_query(F.data.startswith('lang_'))
async def lang_handler(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("lang_")[-1]
    if lang == 'uz':
        await state.update_data(locale='uz')
        await callback.answer(_("O'zbek tili tanlandi"), locale=lang)
    else:
        await state.update_data(locale=lang)
        await callback.answer(_("Ingiliz  tili tanlandi"), locale=lang)

    await callback.message.answer(text=_("UstozShogird kanalining no rasmiy botiga xush kelibsiz /help yordam buyrugi orqali nimalarga qodir ekanligimni bilib oling!", locale=lang), reply_markup=menu_button().as_markup(resize_keyboard=True, locale=lang))

@dp.message(F.text == '/help')
async def help_handler(message: Message):
    await message.answer(text=_("""
UzGeeks faollari tomonidan tuzilgan Ustoz-Shogird kanali.

Bu yerda Programmalash bo`yicha
  #Ustoz,
  #Shogird,
  #oquvKursi,
  #Sherik,
  #Xodim va
  #IshJoyi
 topishingiz mumkin.

E'lon berish: @UstozShogirdBot

Admin @UstozShogirdAdminBot
    """))

@dp.message(F.text.in_([__('Sherik kerak'), __('Ish joyi kerak'), __('Hodim kerak'), __('Ustoz kerak'), __('Shogirt kerak')]))
async def categories_handler(message: Message, state: FSMContext):
    who_needs = message.text.split(_(' kerak'))[0].strip()
    await state.set_state(Questions.name)
    await state.update_data(username=message.from_user.first_name)
    await state.update_data(who_needs=who_needs)
    await message.answer(text=_("""
                {who_needs} topish uchun ariza berish

Hozir sizga birnecha savollar beriladi.
Har biriga javob bering.
Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.
                    """).format(who_needs = who_needs))
    if who_needs == _('Hodim') or who_needs == "Employee need":
        await message.answer(text=_("🎓 Idora nomi?"))
        return
    await message.answer(text=_("<b>Ism, familiyangizni kiriting?</b>"), parse_mode=ParseMode.HTML)

@dp.message(Questions.name)
async def name_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Questions.age)
    data = await state.get_data()
    if data['who_needs'] == _('Hodim') or data['who_needs'] == 'Employee need':
        await message.answer(text=_("✍️Mas'ul ism sharifi?"))
        return
    await message.answer(text=_("""
🕑 Yosh: 
                    
Yoshingizni kiriting?
Masalan, 19
"""))
@dp.message(Questions.age)
async def technology_handler(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Questions.technology)
    await message.answer(text=_("""
📚 Texnologiya:

Talab qilinadigan texnologiyalarni kiriting?
Texnologiya nomlarini vergul bilan ajrating. Masalan,
Java, C++, C#
"""))
@dp.message(Questions.technology)
async def phone_handler(message: Message, state: FSMContext):
    await state.update_data(technology=message.text)
    await state.set_state(Questions.phone)
    await message.answer(text=_("""
📞 Aloqa:
            
Bog`lanish uchun raqamingizni kiriting?
Masalan, +998 90 123 45 67
"""))
@dp.message(Questions.phone)
async def place_handler(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(Questions.place)
    await message.answer(text=_("""
🌐 Hudud:
            
Qaysi hududdansiz?
Viloyat nomi, Toshkent shahar yoki Respublikani kiriting.
"""))

@dp.message(Questions.place)
async def place_handler(message: Message, state: FSMContext):
    await state.update_data(place=message.text)
    await state.set_state(Questions.price)
    data = await state.get_data()
    if data['who_needs'] == _('Hodim') or data['who_needs'] == 'Employee need':
        await message.answer(text=_("""
💰 Maoshni kiriting?
"""))
        return
    await message.answer(text=_("""
💰 Narxi:
            
Tolov qilasizmi yoki Tekinmi?
Kerak bo`lsa, Summani kiriting?
"""))
@dp.message(Questions.price)
async def profession_handler(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(Questions.profession)
    data = await state.get_data()
    if data['who_needs'] == _('Hodim') or data['who_needs'] == 'Employee need':
        await message.answer(text=_("""
🕰 Ish vaqtini kiriting?
"""))
        return
    await message.answer(text=_("""
👨🏻‍💻 Kasbi: 
                    
Ishlaysizmi yoki o`qiysizmi?
Masalan, Talaba
"""))


@dp.message(Questions.profession)
async def profession_handler(message: Message, state: FSMContext):
    await state.update_data(profession=message.text)
    await state.set_state(Questions.time_to_talk)
    await message.answer(text=_("""
🕰 Murojaat qilish vaqti: 

Qaysi vaqtda murojaat qilish mumkin?
Masalan, 9:00 - 18:00
"""))

@dp.message(Questions.time_to_talk)
async def aim_handler(message: Message, state: FSMContext):
    await state.update_data(time_to_talk=message.text)
    await state.set_state(Questions.aim)
    data = await state.get_data()
    if data['who_needs'] == _('Hodim') or data['who_needs'] == 'Employee need':
        await message.answer(text=_("""
‼️ Qo`shimcha ma`lumotlar?
"""))
        return
    await message.answer(text=_("""
🔎 Maqsad: 
                        
Maqsadingizni qisqacha yozib bering.                            
"""))

@dp.message(Questions.aim)
async def aim_handler(message: Message, state: FSMContext):
    await state.update_data(aim=message.text)
    data = await state.get_data()
    xodim = _('👨‍💼 Xodim')
    Yosh = _('🕑 Yosh')
    Texnologiya = _('📚 Texnologiya')
    Aloqa = _('📞 Aloqa')
    Hudud = _('🌐 Hudud')
    Narxi = _('💰 Narxi')
    Kasbi = _('👨🏻💻 Kasbi')
    Murojat = _('🕰 Murojaat')
    Maqsad = _('🔎 Maqsad')
    if data['who_needs'] == _('Hodim') or data['who_needs'] == 'Employee need':
        xodim = _('🏢 Idora')
        Yosh = _("✍️Mas'ul")
        Narxi = _("💰 Maosh")
        Kasbi = _("🕰 Ish vaqti")
        Maqsad = _("‼️ Qo`shimcha ma`lumotlar")
    if data['who_needs'] == _('Ustoz') or data['who_needs'] == 'Teacher':
        xodim = _('🎓 Shogirt')
    if data['who_needs'] == _('Sherik') or data['who_needs'] == 'Partner':
        xodim = _('🏅 Sherik')
    if data['who_needs'] == _('Shogirt') or data['who_needs'] == 'Pupil':
        xodim = _('🎓 Ustoz')
    mess = f"""
    {data['who_needs']} kerak
    {xodim}:  {data['name']}
    {Yosh}: {data['age']}
    {Texnologiya}: {data['technology']}
    🇺🇿 Telegram: {data['username']}
    {Aloqa}: {data['phone']}
    {Hudud}: {data['place']}
    {Narxi}: {data['price']}
    {Kasbi}: {data['profession']}
    {Murojat}: {data['time_to_talk']}
    {Maqsad}: {data['aim']}
    """
    ikb = InlineKeyboardBuilder()
    ikb.add(
        InlineKeyboardButton(text=_('Ha'), callback_data='confirm'),
        InlineKeyboardButton(text=_('Yo\'q'), callback_data='ignore')
    )
    await message.answer(text=_('To\'ldirilgan ma\'lumotlar to\'g\'rimi?'))
    await message.answer(text=mess, reply_markup=ikb.as_markup())
    return

# @dp.channel_post()
# async def dscsd(message: Message):
#     await message.send_copy(chat_id=CHANNEL_ID)

@dp.callback_query(F.data == 'confirm')
async def confirmation_handler(callback: CallbackQuery, state: FSMContext):
    text = callback.message.text
    ikb = InlineKeyboardBuilder()
    ikb.add(
        InlineKeyboardButton(text=_('Ha'), callback_data='admin_confirm'),
        InlineKeyboardButton(text=_('Yo\'q'), callback_data='admin_ignore')
    )
    # database.clear()
    database['current_user'] = callback.from_user.model_dump_json()
    await callback.message.bot.send_message(ADMIN[0], text, reply_markup=ikb.as_markup())
    # await callback.message.send_copy(chat_id=ADMIN[0])
    await callback.message.delete()
    await callback.message.answer(text=_("Adminga yuborildi"), reply_markup=menu_button().as_markup(resize_keyboard=True))

@dp.callback_query(F.data.in_({"admin_confirm", "admin_ignore"}))
async def admin_desicion_handler(callback: CallbackQuery, state: FSMContext):
    # current_user = await state.get_data()
    database['current_user'] = json.loads(database['current_user'])
    if callback.data == 'admin_confirm':
        await callback.message.bot.send_message(chat_id=CHANNEL_ID, text=callback.message.text)
        await callback.message.delete()
        await callback.message.bot.send_message(chat_id=database['current_user']['id'], text=_("{first_name} arizangiz kanalga yuborildi!😎").format(first_name=f"{database['current_user']['first_name']}"))
    elif callback.data == 'admin_ignore':
        await callback.message.delete()
        await callback.message.bot.send_message(chat_id=database['current_user']['id'], text=_("{first_name} arizangiz inkor qilindi!🤕").format(first_name=f"{database['current_user']['first_name']}"))

@dp.callback_query(F.data == 'ignore')
async def confirmation_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer(_("Ma'lumotlar bekor qilindi!"), reply_markup=menu_button().as_markup(resize_keyboard=True))

async def on_start_up(dispatcher: Dispatcher, bot: Bot):
    commands = [
        BotCommand(command='start', description='Botni boshlash uchun'),
        BotCommand(command='help', description='Bot haqida')
    ]
    await bot.set_my_commands(commands=commands)

async def on_shut_down(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_my_commands()

async def main() -> None:
    bot = Bot(token=TOKEN)
    i18 = I18n(path='locales')
    dp.update.outer_middleware.register(FSMI18nMiddleware(i18))
    dp.startup.register(on_start_up)
    dp.startup.register(on_shut_down)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())



