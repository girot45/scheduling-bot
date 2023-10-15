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
        date_today: date,
):
    day_of_week = date_today.weekday()
    day = date_today.day
    month = date_today.month
    message_for_day = f"{day_of_week_by_index[day_of_week]} {day} " \
                     f"{month_by_index[month - 1]}\n\n"
    for index, row in enumerate(query):
        event_str = f"С {row.timestart} до {row.timeend}\n" \
                    f"{row.event}\n\n"
        message_for_day += event_str
    return message_for_day
