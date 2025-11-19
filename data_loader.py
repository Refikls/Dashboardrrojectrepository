import json
from datetime import datetime

def load_schedule_data():
    try:
        with open('data/schedule.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("ОШИБКА: Файл data/schedule.json не найден")
        return {"schedule": []}

def get_day_info(date_str):
    if not date_str:
        return None, None
    
    selected_date = datetime.strptime(date_str.split('T')[0], '%Y-%m-%d')
    
    days_ru = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    day_of_week = days_ru[selected_date.weekday()]
    
    week_number = selected_date.isocalendar()[1]
    week_parity = "odd" if week_number % 2 != 0 else "even"
    
    return day_of_week, week_parity