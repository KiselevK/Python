import requests  # Імпортуємо бібліотеку для виконання HTTP-запитів
import tkinter as tk  # Імпортуємо бібліотеку для створення графічного інтерфейсу
from tkinter import messagebox  # Імпортуємо модуль для відображення повідомлень
import json  # Імпортуємо модуль для роботи з JSON-даними
import os  # Імпортуємо модуль для роботи з файловою системою

def fetch_holidays():  # Функція для отримання списку свят з API
    url = "https://date.nager.at/api/v3/PublicHolidays/2024/UA"  # URL для запиту свят для України на 2024 рік
    try:
        response = requests.get(url)  # Виконуємо GET-запит до API
        if response.status_code == 200:  # Перевіряємо, чи успішний запит
            holidays = response.json()  # Конвертуємо відповідь з JSON у Python-об'єкт
            return holidays  # Повертаємо список свят
        else:
            messagebox.showerror("Помилка", "Не вдалося отримати дані з API.")  # Відображаємо помилку користувачу
            return None  # Повертаємо None у разі помилки
    except Exception as e:
        messagebox.showerror("Помилка", f"Виникла помилка: {e}")  # Відображаємо деталі винятку
        return None  # Повертаємо None у разі винятку

def check_holidays():  # Функція для перевірки свят у введеному місяці
    month = entry_month.get()  # Отримуємо значення з поля введення
    if not month.isdigit() or int(month) < 1 or int(month) > 12:  # Перевіряємо коректність введеного місяця
        messagebox.showwarning("Попередження", "Будь ласка, введіть номер місяця від 1 до 12.")  # Попереджаємо про помилку
        return  # Зупиняємо виконання функції
    holidays = fetch_holidays()  # Отримуємо список свят
    if holidays is None:
        return  # Зупиняємо виконання, якщо не вдалося отримати свята
    month = int(month)  # Конвертуємо місяць у ціле число
    holidays_in_month = [h for h in holidays if int(h['date'][5:7]) == month]  # Фільтруємо свята за місяцем
    if holidays_in_month:  # Якщо є свята у вибраному місяці
        message = "У цьому місяці є свята:"  # Початкове повідомлення
        for h in holidays_in_month:
            message += f"\n{h['date']}: {h['localName']}"  # Додаємо кожне свято до повідомлення
    else:
        message = "У цьому місяці немає свят."  # Повідомлення, якщо свят немає
    messagebox.showinfo("Результат", message)  # Відображаємо результат користувачу

def save_holidays():  # Функція для збереження свят у файл
    holidays = fetch_holidays()  # Отримуємо список свят
    if holidays is None:
        return  # Зупиняємо виконання, якщо не вдалося отримати свята
    file_path = os.path.join(os.getcwd(), "holidays.json")  # Формуємо шлях до файлу
    try:
        with open(file_path, 'w', encoding='utf-8') as f:  # Відкриваємо файл для запису з кодуванням UTF-8
            json.dump(holidays, f, ensure_ascii=False, indent=4)  # Записуємо дані у форматі JSON
        messagebox.showinfo("Збережено", f"Свята збережено у файл:\n{file_path}")  # Повідомляємо про успішне збереження
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося зберегти файл: {e}")  # Відображаємо помилку збереження

# Створення інтерфейсу
root = tk.Tk()  # Створюємо головне вікно програми
root.title("Перевірка свят")  # Встановлюємо заголовок вікна

label_month = tk.Label(root, text="Введіть номер місяця (1-12):")  # Створюємо мітку для введення місяця
label_month.pack(pady=5)  # Розміщуємо мітку в інтерфейсі з відступом

entry_month = tk.Entry(root)  # Створюємо поле для введення номера місяця
entry_month.pack(pady=5)  # Розміщуємо поле введення з відступом

button_check = tk.Button(root, text="Перевірити", command=check_holidays)  # Створюємо кнопку для перевірки свят
button_check.pack(pady=5)  # Розміщуємо кнопку з відступом

button_save = tk.Button(root, text="Зберегти всі свята у файл", command=save_holidays)  # Створюємо кнопку для збереження свят
button_save.pack(pady=5)  # Розміщуємо кнопку з відступом

root.mainloop()  # Запускаємо головний цикл програми
