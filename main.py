from os import environ
from APP.Library import Library


def menu():
    """
    Функция вывода функций программы
    """
    print("\n** Функции библиотеки: **")
    print("1 - Добавить новую книгу")
    print("2 - Удалить книгу")
    print("3 - Поиск книги")
    print("4 - Отображение всех книг")
    print("5 - Изменить статус книги")
    print("0 - Выход")


# Получение пути до файла базы данных, через переменную среду
FILE_NAME = environ.get('PATH_DB_Library', 'db/library.json')


def main():
    """
    Главная функция программы.
    Считывает номер функции, которую хочет выполнить пользователь.
    """
    library = Library(FILE_NAME)
    print("Приветсвенное сообщение")
    while True:
        menu()
        choice = input("Чтобы выбрать нужную функцию, введити номер функции без пробелов\nВыберите действие: ")
        if choice == '1':
            library.add_book()
        elif choice == '2':
            library.delete_book()
        elif choice == '3':
            library.search_books()
        elif choice == '4':
            library.display_books()
        elif choice == '5':
            library.change_status()
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("\n *** Некорректный выбор. Пожалуйста, выберите номер действия в числовом формате без пробелов. ***")


if __name__ == '__main__':
    main()
