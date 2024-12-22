import pandas as pd
from datetime import datetime

# Словарь для замены русских месяцев на английские
month_translation = {
    "Янв": "Jan",
    "Фев": "Feb",
    "Мар": "Mar",
    "Апр": "Apr",
    "Май": "May",
    "Июн": "Jun",
    "Июл": "Jul",
    "Авг": "Aug",
    "Сен": "Sep",
    "Окт": "Oct",
    "Ноя": "Nov",
    "Дек": "Dec",
}

# Функция для замены месяца на английский
def translate_date(date_str):
    for ru, en in month_translation.items():
        if ru in date_str:
            return date_str.replace(ru, en)
    return date_str

# Загружаем данные из CSV-файла
csv_path = 'test_results.csv'  # Путь к вашему CSV-файлу
data = pd.read_csv(csv_path)

# Параметры задачи
threshold_date_str = translate_date("12 Май 2017 10:00")
threshold_date = datetime.strptime(threshold_date_str, "%d %b %Y %H:%M")
passing_score = 60

# Преобразуем столбец "Завершено" в формат datetime
data['Завершено'] = data['Завершено'].apply(
    lambda x: datetime.strptime(translate_date(x), "%d %b %Y %H:%M") if pd.notnull(x) else None
)

# Фильтруем данные: попытки после заданной даты и оценки ниже порога
failed_attempts = data[(data['Завершено'] > threshold_date) & (data['Оценка/100,00'] < passing_score)]

# Количество неудачных попыток
failed_count = failed_attempts.shape[0]

# Список людей, не прошедших тест
failed_people = failed_attempts[['Фамилия', 'Имя']].drop_duplicates()

# Вывод результатов
print(f"Количество неудачных попыток: {failed_count}")
print("Список людей, не прошедших тест:")
print(failed_people)

# Сохраняем результаты в файл
failed_people.to_csv('failed_people.csv', index=False, encoding='utf-8-sig')
