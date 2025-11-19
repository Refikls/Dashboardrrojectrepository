# Работа с данными


# Пример структуры данных
SCHEDULE_DATA = {
    'group1': {
        '2024-01-15': [
            {'time': '09:00', 'subject': 'Мат. ан', 'teacher': 'Иванов'},
            {'time': '11:00', 'subject': 'Физика', 'teacher': 'Петров'},
        ]
    }
}

def get_schedule(group, date):
    return SCHEDULE_DATA.get(group, {}).get(date, [])
