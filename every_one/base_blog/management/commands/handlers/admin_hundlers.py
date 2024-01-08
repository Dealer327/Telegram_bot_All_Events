from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message

from base_blog.management.commands.lexicon.lexicon_ru import Lexicon_ru
from base_blog.management.commands.keyboards.main_menu import create_inline_kb
from base_blog.management.commands.date_base import datebase

router: Router = Router()


# Хендлер для регистрации новых эвентов, уведомление приходит админам бота
@router.callback_query(F.data == 'Yes_reg_new_event' or F.data == 'No_reg_new_event')
async def process_add_id_event(callback: CallbackQuery):
    if callback.data == 'Yes_reg_new_event':
        await callback.message.delete_reply_markup()

        @router.message()
        async def add_id_event(message: Message, bot: Bot):
            # получаем id эвента от админа
            id_event = int(message.text)
            # Публикуем эвент по id в чат бота
            await datebase.add_new_event(id_event)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            # Берем этот эвент и пересылаем его в канал телеграма
            event = await datebase.process_posting_event_in_chanel(id_event)
            msg_id = await bot.send_message(chat_id=-1002007237265,
                                            text=f'<b>{event.name_event}</b>\n\n'
                                                 f'<b>{Lexicon_ru["about_event"]}</b>\n'
                                                 f'{event.info_event}\n'
                                                 f'<b>Начало:</b> '
                                                 f'{event.start_time.strftime("%Y-%m-%d в %H:%M")}\n'
                                                 f'Ссылка: {event.url}')
            await datebase.url_in_chanel_for_events(id_event, msg_id.message_id)
            # Цикл для отправки уведомление всем пользователям, что появилось новое событие в чат боте
            send_msg_users = await datebase.all_users()
            for user in send_msg_users:
                all_not_read_events = await datebase.show_count_not_read_event_in_menu(user.external_id)
                keyboard_menu = create_inline_kb(1, all_not_read_events, 'calendar', 'new_event')
                try:
                    await bot.send_message(chat_id=user.external_id,
                                           text=Lexicon_ru['/start'],
                                           reply_markup=keyboard_menu
                                           )
                # Исключение на случай если пользователь по каким то причинам нее получил уведомление
                except Exception as e:
                    print(f"Failed to send message to user {user.name}: {e}")
