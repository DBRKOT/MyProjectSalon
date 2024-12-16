import functools
from datetime import datetime, timedelta
users = [
    {'username': 'john_doe', 'password': 'password', 'role': 'user', 'history': [], 'created_at': '2024-09-01'},
    {'username': 'admin_user', 'password': 'password', 'role': 'admin'}
]

services = [
    {'name': 'стрижка', 'price': 1500, 'rating': 4.5, 'added_at': '2024-09-01', 'addons': ['маска для волос', 'шампунь']},
    {'name': 'покраска', 'price': 2000, 'rating': 4.8, 'added_at': '2024-09-05', 'addons': ['маска для волос', 'краска для волос']},
    {'name': 'маникюр', 'price': 1200, 'rating': 4.7, 'added_at': '2024-09-10', 'addons': ['лак для ногтей', 'крем для рук']},
    {'name': 'педикюр', 'price': 1300, 'rating': 4.6, 'added_at': '2024-09-15', 'addons': ['лак для ногтей', 'крем для ног']},
    {'name': 'массаж', 'price': 2500, 'rating': 4.9, 'added_at': '2024-09-20', 'addons': ['масло для массажа', 'ароматические свечи']}
]

available_slots = [
    {'service': 'стрижка', 'date': '2024-10-01', 'time': '10:00'},
    {'service': 'стрижка', 'date': '2024-10-01', 'time': '12:00'},
    {'service': 'стрижка', 'date': '2024-10-02', 'time': '14:00'},
    {'service': 'покраска', 'date': '2024-10-02', 'time': '16:00'},
    {'service': 'покраска', 'date': '2024-10-03', 'time': '18:00'},
    {'service': 'маникюр', 'date': '2024-10-03', 'time': '10:00'},
    {'service': 'маникюр', 'date': '2024-10-04', 'time': '12:00'},
    {'service': 'педикюр', 'date': '2024-10-04', 'time': '14:00'},
    {'service': 'педикюр', 'date': '2024-10-05', 'time': '16:00'},
    {'service': 'массаж', 'date': '2024-10-05', 'time': '18:00'}
]


def filter_services_by_price(services, max_price):
    return list(filter(lambda service: service['price'] <= max_price, services))

def sort_services_by_rating(services):
    return sorted(services, key=lambda service: service['rating'], reverse=True)

def calculate_total_price(services):
    return functools.reduce(lambda acc, service: acc + service['price'], services, 0)


def authenticate(username, password):
    user = next(filter(lambda u: u['username'] == username and u['password'] == password, users), None)
    return user

def register(username, password, role):
    if any(u['username'] == username for u in users):
        print("Пользователь с таким именем уже существует.")
        return None
    new_user = {
        'username': username,
        'password': password,
        'role': role,
        'history': [],
        'created_at': '2024-09-01'
    }
    users.append(new_user)
    return new_user

def display_services(services):
    for service in services:
        print(f"{service['name']} - {service['price']} руб. - Рейтинг: {service['rating']}")
        if service['addons']:
            print(f"  Дополнительные товары: {', '.join(service['addons'])}")

def add_service(name, price, rating, addons):
    new_service = {
        'name': name,
        'price': price,
        'rating': rating,
        'added_at': '2024-09-01',
        'addons': addons
    }
    services.append(new_service)

def remove_service(name):
    global services
    services = list(filter(lambda service: service['name'] != name, services))

def edit_service(name, price, rating, addons):
    for service in services:
        if service['name'] == name:
            service['price'] = price
            service['rating'] = rating
            service['addons'] = addons
            break

def display_user_history(user):
    if not user['history']:
        print("История посещений пуста.")
    else:
        for visit in user['history']:
            print(f"Услуга: {visit['service']}, Дата: {visit['date']}, Время: {visit['time']}")
            if visit['addons']:
                print(f"  Дополнительные товары: {', '.join(visit['addons'])}")

def book_service(user, service_name, date, time, addons):
    user['history'].append({'service': service_name, 'date': date, 'time': time, 'addons': addons})
    global available_slots
    available_slots = list(filter(lambda slot: not (slot['service'] == service_name and slot['date'] == date and slot['time'] == time), available_slots))

def update_profile(user, new_password):
    user['password'] = new_password

def manage_users():
    while True:
        print("Выберите действие:")
        print("1. Добавить пользователя")
        print("2. Удалить пользователя")
        print("3. Редактировать данные пользователя")
        print("4. Просмотреть список пользователей")
        print("5. Вернуться назад")

        choice = input("Ваш выбор: ")
        if choice == '1':
            username = input("Логин: ")
            password = input("Пароль: ")
            role = input("Роль (user/admin): ")
            user = register(username, password, role)
            if user:
                print("Пользователь успешно добавлен!")
        elif choice == '2':
            username = input("Логин пользователя для удаления: ")
            global users
            users = list(filter(lambda u: u['username'] != username, users))
            print("Пользователь удален!")
        elif choice == '3':
            username = input("Логин пользователя для редактирования: ")
            user = next(filter(lambda u: u['username'] == username, users), None)
            if user:
                new_password = input("Новый пароль: ")
                update_profile(user, new_password)
                print("Данные пользователя обновлены!")
            else:
                print("Пользователь не найден.")
        elif choice == '4':
            for user in users:
                print(f"Логин: {user['username']}, Роль: {user['role']}")
        elif choice == '5':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def view_statistics():
    print("Статистика:")
    print(f"Количество пользователей: {len(users)}")
    print(f"Количество услуг: {len(services)}")
    total_price = calculate_total_price(services)
    print(f"Общая стоимость всех услуг: {total_price} руб.")


def display_available_slots(service_name):
    slots = list(filter(lambda slot: slot['service'] == service_name, available_slots))
    if not slots:
        print("Свободных слотов нет.")
    else:
        for i, slot in enumerate(slots, start=1):
            print(f"{i}. Дата: {slot['date']}, Время: {slot['time']}")
        return slots

def main():
    while True:
        print("Добро пожаловать в салон красоты!")
        print("Выберите действие:")
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("3. Выйти")

        choice = input("Ваш выбор: ")
        if choice == '1':
            username = input("Логин: ")
            password = input("Пароль: ")
            user = authenticate(username, password)
            if not user:
                print("Неверный логин или пароль.")
                continue
            break
        elif choice == '2':
            username = input("Логин: ")
            password = input("Пароль: ")
            role = input("Роль (user/admin): ")
            user = register(username, password, role)
            if user:
                print("Регистрация успешна!")
            continue
        elif choice == '3':
            return
        else:
            print("Неверный выбор. Попробуйте снова.")

    while True:
        if user['role'] == 'user':
            print("Выберите действие:")
            print("1. Просмотреть доступные услуги")
            print("2. Записаться на услугу")
            print("3. Просмотреть историю посещений")
            print("4. Сортировать услуги по цене")
            print("5. Фильтровать услуги по рейтингу")
            print("6. Обновить профиль")
            print("7. Выйти")

            choice = input("Ваш выбор: ")
            if choice == '1':
                display_services(services)
            elif choice == '2':
                service_name = input("Название услуги: ")
                slots = display_available_slots(service_name)
                if slots:
                    slot_choice = int(input("Выберите номер слота: ")) - 1
                    if 0 <= slot_choice < len(slots):
                        selected_slot = slots[slot_choice]
                        date = selected_slot['date']
                        time = selected_slot['time']
                        service = next(filter(lambda s: s['name'] == service_name, services), None)
                        if service:
                            print(f"Доступные дополнительные товары для услуги '{service_name}':")
                            for i, addon in enumerate(service['addons'], start=1):
                                print(f"{i}. {addon}")
                            addon_choices = input("Выберите дополнительные товары (через запятую): ").split(',')
                            addons = [service['addons'][int(choice) - 1] for choice in addon_choices if 1 <= int(choice) <= len(service['addons'])]
                            book_service(user, service_name, date, time, addons)
                            print("Запись успешна!")
                        else:
                            print("Услуга не найдена.")
                    else:
                        print("Неверный выбор слота.")
            elif choice == '3':
                display_user_history(user)
            elif choice == '4':
                max_price = float(input("Максимальная цена: "))
                filtered_services = filter_services_by_price(services, max_price)
                display_services(filtered_services)
            elif choice == '5':
                sorted_services = sort_services_by_rating(services)
                display_services(sorted_services)
            elif choice == '6':
                new_password = input("Новый пароль: ")
                update_profile(user, new_password)
                print("Профиль обновлен!")
            elif choice == '7':
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
        elif user['role'] == 'admin':
            print("Выберите действие:")
            print("1. Добавить услугу")
            print("2. Удалить услугу")
            print("3. Редактировать данные об услуге")
            print("4. Управление пользователями")
            print("5. Просмотреть статистику")
            print("6. Выйти")

            choice = input("Ваш выбор: ")
            if choice == '1':
                name = input("Название услуги: ")
                price = float(input("Цена: "))
                rating = float(input("Рейтинг: "))
                addons = input("Дополнительные товары (через запятую): ").split(',')
                add_service(name, price, rating, addons)
                print("Услуга добавлена!")
            elif choice == '2':
                name = input("Название услуги: ")
                remove_service(name)
                print("Услуга удалена!")
            elif choice == '3':
                name = input("Название услуги: ")
                price = float(input("Новая цена: "))
                rating = float(input("Новый рейтинг: "))
                addons = input("Дополнительные товары (через запятую): ").split(',')
                edit_service(name, price, rating, addons)
                print("Данные об услуге обновлены!")
            elif choice == '4':
                manage_users()
            elif choice == '5':
                view_statistics()
            elif choice == '6':
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
