from aiogram.filters.callback_data import CallbackData


class CallbackFactoryForEvent(CallbackData, prefix="Event", sep="_"):
    id_event: int
