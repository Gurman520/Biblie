import json
import os
from APP.Book import Book


class NotExistBook(Exception):
    """
    Исключение для отлова отсутствия книги с указанным ID
    """
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code


class Library:
    """
    Класс библиотека - служит основным классом системы
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.books = self.load_data()

    def load_data(self):
        """
        Метод загрузки данных.\n
        Используется для загрузки информации из Json файла
        :return: Список книг загруженных из файла
        """
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Book(**book) for book in data]
        return []

    def save_data(self):
        """
        Метод для записи информации о новой книге в файл Json
        """
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump([book.__dict__ for book in self.books], file, ensure_ascii=False, indent=4)

    def generate_id(self):
        """
        Метод генерации уникального номера для книги
        :return: Уникальный ID для книги
        """
        if self.books:
            return max(book.id for book in self.books) + 1
        return 1

    def add_book(self):
        """
        Метод для получения информации о новой книги
        """
        title = input("* Введите название книги: ")
        author = input("* Введите автора книги: ")
        year = input("* Введите год издания книги: ")
        book = Book(self.generate_id(), title, author, year)
        self.books.append(book)
        self.save_data()
        print("\n *** Книга успешно добавлена!")

    def delete_book(self):
        """
        Метод удаления книги из базы
        """
        try:
            book_id = int(input("Введите id книги, которую нужно удалить: "))
            book_exists = any(book.id == book_id for book in self.books)
            if not book_exists:
                raise NotExistBook("\n -- Некорректный id. Книга с таким id не найдена.")
            self.books = [book for book in self.books if book.id != book_id]
            self.save_data()
            print("\n *** Книга успешно удалена!")
            self.display_books()
        except NotExistBook as e:
            print(f"{e}")
        except ValueError:
            print("\n -- Некорректный id. Пожалуйста, введите число.")

    def search_books(self):
        """
        Метод поиска книги по параметру
        В качестве входного параметра может быть указан любой из параметров.
        - Название
        - Автор
        - Год
        """
        query = input("Введите название, автора или год издания для поиска: ").lower()
        results = [book for book in self.books if query in book.title.lower() or query in book.author.lower() or query in book.year]
        if results:
            for book in results:
                print(book)
        else:
            print("\n -- Книги не найдены.")

    def display_books(self):
        """
        Метод отображения всех книг существующих в системе
        """
        print("\n *** Все доступные книги:\n (Формат: id: название by автор (год выпуска) - статус")
        if self.books:
            for book in self.books:
                print(book)
        else:
            print("\n -- Библиотека пуста.")

    def change_status(self):
        """
        Метод изменения статуса книги
        """
        try:
            book_id = int(input("Введите id книги, статус которой нужно изменить: "))
            book_exists = any(book.id == book_id for book in self.books)
            if not book_exists:
                raise NotExistBook("\n -- Некорректный id. Книга с таким id не найдена.")
            new_status = input("Введите новый статус (в наличии/выдана): ").strip()
            if new_status not in ["в наличии", "выдана"]:
                print("Некорректный статус. Пожалуйста, введите 'в наличии' или 'выдана'.")
                return
            for book in self.books:
                if book.id == book_id:
                    book.status = new_status
                    self.save_data()
                    print("\n *** Статус книги успешно изменен!")
                    self.display_books()
                    return
            print("\n -- Книга с таким id не найдена.")
        except NotExistBook as e:
            print(f"{e}")
        except ValueError:
            print("\n -- Некорректный id. Пожалуйста, введите число.")