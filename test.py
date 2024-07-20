import unittest
import os
from io import StringIO
from unittest.mock import patch
from APP.Book import Book
from APP.Library import Library


# Тесты
class TestLibrary(unittest.TestCase):
    def setUp(self):
        """
        Функция для создания тестовой библиотеки с тестовым файлом
        :return:
        """
        self.library = Library('test_library.json')
        # Очищаем библиотеку перед каждым тестом
        self.library.books = []
        self.library.save_data()

    def tearDown(self):
        """
        Функция для, удаления тестового файла после каждого теста
        :return:
        """
        if os.path.exists('test_library.json'):
            os.remove('test_library.json')

    def add_test_books(self):
        '''
        Функция для добавления тестовых книг
        '''
        book1 = Book(1, "Test Title 1", "Test Author 1", "2021")
        book2 = Book(2, "Test Title 2", "Test Author 2", "2022")
        book3 = Book(3, "Another Title", "Another Author", "2020")
        self.library.books = [book1, book2, book3]
        self.library.save_data()

    @patch('builtins.input', side_effect=['Test Title 3', 'Test Author 3', '2023'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_book(self, mock_stdout, mock_input):
        """
        Тест добавления книги
        :param mock_stdout:
        :param mock_input:
        :return:
        """
        self.library.add_book()
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "*** Книга успешно добавлена!")
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Title 3")

    @patch('builtins.input', side_effect=['1'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_delete_book(self, mock_stdout, mock_input):
        """
        Тест удаления книги
        :param mock_stdout:
        :param mock_input:
        :return:
        """
        self.add_test_books()
        self.library.delete_book()
        output = mock_stdout.getvalue().strip().split('\n')
        self.assertEqual(output[0], "*** Книга успешно удалена!")
        self.assertEqual(len(self.library.books), 2)

        # Попробуем удалить несуществующую книгу
        with patch('builtins.input', side_effect=['99']):
            self.library.delete_book()
        output = mock_stdout.getvalue().strip().split('\n')
        self.assertEqual(output[-1], " -- Некорректный id. Книга с таким id не найдена.")

    @patch('builtins.input', side_effect=['Test'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_search_books(self, mock_stdout, mock_input):
        """
        Тест поиска книг
        :param mock_stdout:
        :param mock_input:
        :return:
        """
        self.add_test_books()
        self.library.search_books()
        output = mock_stdout.getvalue().strip().split('\n')
        self.assertIn("1: Test Title 1 by Test Author 1 (2021)", output[-2])
        self.assertIn("2: Test Title 2 by Test Author 2 (2022)", output[-1])

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_books(self, mock_stdout):
        """
        Тест вывода списка книг
        :param mock_stdout:
        :return:
        """
        self.add_test_books()
        self.library.display_books()
        output = mock_stdout.getvalue().strip().split('\n')
        self.assertIn("1: Test Title 1 by Test Author 1 (2021)", output[2])
        self.assertIn("2: Test Title 2 by Test Author 2 (2022)", output[3])

    @patch('builtins.input', side_effect=['1', 'выдана'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_change_status(self, mock_stdout, mock_input):
        """
        Тест изменения статуса
        :param mock_stdout:
        :param mock_input:
        :return:
        """
        self.add_test_books()
        self.library.change_status()
        output = mock_stdout.getvalue().strip().split('\n')
        self.assertEqual(output[0], "*** Статус книги успешно изменен!")
        self.assertEqual(self.library.books[0].status, "выдана")


if __name__ == '__main__':
    unittest.main()
