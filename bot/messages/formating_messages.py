from datetime import date

from bot.config import month_by_index, day_of_week_by_index
from bot.messages.messages_texts import NO_PLANS_MES


def formatting_a_day_schedule_for_sending_a_message(
        query,
        date_: date,
):
    day_of_week = date_.weekday()
    day = date_.day
    month = date_.month
    message_head = f"{day} {month_by_index[month - 1]} " \
                   f"({day_of_week_by_index[day_of_week]})\n\n"
    events_str = ""
    message_for_day = ""
    for index, row in enumerate(query):
        if row.timeend:
            events_str += f"С {row.timestart} до {row.timeend}\n"
        else:
            events_str += f"В {row.timestart}\n"
        events_str += f"{row.event}\n\n"
    if events_str:
        message_for_day += message_head + events_str
    else:
        message_for_day += f"На {message_head}{NO_PLANS_MES}"
    return message_for_day
