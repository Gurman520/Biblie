import json
import os
from APP.Book import Book


class Library:
    def __init__(self, file_name):
        self.file_name = file_name
        self.books = self.load_data()

    def load_data(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Book(**book) for book in data]
        return []

    def save_data(self):
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump([book.__dict__ for book in self.books], file, ensure_ascii=False, indent=4)

    def generate_id(self):
        if self.books:
            return max(book.id for book in self.books) + 1
        return 1

    def add_book(self):
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        year = input("Введите год издания книги: ")
        book = Book(self.generate_id(), title, author, year)
        self.books.append(book)
        self.save_data()
        print("Книга успешно добавлена!")

    def delete_book(self):
        try:
            book_id = int(input("Введите id книги, которую нужно удалить: "))
            self.books = [book for book in self.books if book.id != book_id]
            self.save_data()
            print("Книга успешно удалена!")
        except ValueError:
            print("Некорректный id. Пожалуйста, введите число.")

    def search_books(self):
        query = input("Введите название, автора или год издания для поиска: ").lower()
        results = [book for book in self.books if query in book.title.lower() or query in book.author.lower() or query in book.year]
        if results:
            for book in results:
                print(book)
        else:
            print("Книги не найдены.")

    def display_books(self):
        if self.books:
            for book in self.books:
                print(book)
        else:
            print("Библиотека пуста.")

    def change_status(self):
        try:
            book_id = int(input("Введите id книги, статус которой нужно изменить: "))
            new_status = input("Введите новый статус (в наличии/выдана): ").strip()
            if new_status not in ["в наличии", "выдана"]:
                print("Некорректный статус. Пожалуйста, введите 'в наличии' или 'выдана'.")
                return
            for book in self.books:
                if book.id == book_id:
                    book.status = new_status
                    self.save_data()
                    print("Статус книги успешно изменен!")
                    return
            print("Книга с таким id не найдена.")
        except ValueError:
            print("Некорректный id. Пожалуйста, введите число.")