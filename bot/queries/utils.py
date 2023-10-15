import time
from datetime import date
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU')

day_of_week_by_index = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье"
}

month_by_index = {
    0: 'Января',
    1: 'Февраля',
    2: 'Марта',
    3: 'Апреля',
    4: 'Мая',
    5: 'Июня',
    6: 'Июля',
    7: 'Августа',
    8: 'Сентября',
    9: 'Октября',
    10: 'Ноября',
    11: 'Декабря',
}

def formatting_a_day_schedule_for_sending_a_message(
        query,
        date_: date,
):
    day_of_week = date_.weekday()
    day = date_.day
    month = date_.month
    message_head = f"{day_of_week_by_index[day_of_week]} {day} " \
                     f"{month_by_index[month - 1]}\n\n"
    events_str = ""
    message_for_day = ""
    for index, row in enumerate(query):
        events_str += f"С {row.timestart} до {row.timeend}\n" \
                      f"{row.event}\n\n"
    print()
    print()
    print(events_str, 12312312312312312231232123123)
    print()
    print()
    if events_str:
        message_for_day += message_head + events_str
    else:
        message_for_day += f"На {message_head} ничего не " \
                           f"запланировано"
    return message_for_day
