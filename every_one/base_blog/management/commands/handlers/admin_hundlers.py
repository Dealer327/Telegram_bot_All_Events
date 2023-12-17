from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message

from ..lexicon.lexicon_ru import Lexicon_ru
from ..keyboards.main_menu import create_inline_kb
from ..date_base import datebase

router: Router = Router()


@router.callback_query(F.data == 'Yes_reg_new_event' or F.data == 'No_reg_new_event')
async def process_add_id_event(callback: CallbackQuery):
    if callback.data == 'Yes_reg_new_event':
        await callback.message.delete_reply_markup()

        @router.message()
        async def add_id_event(message: Message, bot: Bot):
            await datebase.add_new_event(int(message.text))
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            all_not_read_events = await datebase.show_count_not_read_event_in_menu(message.from_user.id)
            keyboard_menu = create_inline_kb(1, all_not_read_events, 'calendar', 'new_event')
            send_msg_users = await datebase.all_users()
            for user in send_msg_users:
                try:
                    await bot.send_message(chat_id=user.external_id,
                                           text=Lexicon_ru['/start'],
                                           reply_markup=keyboard_menu
                                           )
                except Exception as e:
                    print(f"Failed to send message to user {user.name}: {e}")
