from main import Book
import unittest
from unittest.mock import patch, mock_open
from datetime import datetime
import os

class TestBook(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='0')
    def test_initialization_with_new_id(self, mock_file): # тест создания нового объекта Book без указания id в init 
        book = Book(title="Горе от ума", author="Александр Грибоедов", year="1825")
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Горе от ума")
        self.assertEqual(book.author, "Александр Грибоедов")
        self.assertEqual(book.year, "1825")
        self.assertEqual(book.status, 'в наличии')

    @patch('builtins.open', new_callable=mock_open, read_data='4')
    def test_initialization_with_existing_id(self, mock_file): # тест создания объекта Book на основе данных, например, прочитанных из файла
        book = Book(title="Горе от ума", author="Александр Грибоедов", year="1825", id=5) #тут id ранее известен - прочитан из файла, это используется в методе from_dict()
        self.assertEqual(book.id, 5)

    def test_title_setter_invalid(self): 
        with self.assertRaises(ValueError): # тестирование ввода пустой строки с названием книги
            book = Book(title="", author="Автор", id=5, year="2000")

    def test_author_setter_invalid(self):
        with self.assertRaises(ValueError): # тестирование ввода пустой строки с именем автора книги
            book = Book(title="Название", author="", id=5, year="2000")

    def test_year_setter_invalid(self):
        with self.assertRaises(ValueError):  
            book = Book(title="Название", author="Автор", id=5, year="3000")  # тестирование ввода года большего, чем текущий год
        with self.assertRaises(ValueError):
            book = Book(title="Название", author="Автор", id=5, year="abc")  # тестирование ввода года, который невозможно преобразовать в int
        with self.assertRaises(ValueError):
            book = Book(title="Название", author="Автор", id=5, year="999") # тестирование ввода года, длина которого меньше 4 символов


    def test_status_setter_invalid(self):
        with self.assertRaises(ValueError): # тестирование присваемого статуса книги, который не является допустимым
            book = Book(title="Название", author="Автор", id=5, year="2000", status="другой статус")

    @patch('builtins.open', new_callable=mock_open)
    def test_get_id_counter(self, mock_file): # тестирование получения id_counter из файла. Возвращаемое значение должно быть на единицу больше прочитанного
        mock_file.return_value.read.return_value = '2'
        new_id = Book.get_id_counter()
        self.assertEqual(new_id, 3)

    def test_to_dict(self):  #тестирование преобразования объекта book  в словарь
        book = Book(title="Название", author="Автор", id=5, year="2000")
        expected_dict = {
            'id': 5,
            'title': "Название",
            'author': "Автор",
            'year': "2000",
            'status': 'в наличии'
        }
        self.assertEqual(book.to_dict(), expected_dict)

    def test_from_dict(self): #тестирование преобразования словарь в объекта book
        data = {
            'id': 1,
            'title': "Название",
            'author': "Автор",
            'year': "2000",
            'status': 'в наличии'
        }
        book = Book.from_dict(data)
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Название")
        self.assertEqual(book.author, "Автор")
        self.assertEqual(book.year, "2000")
        self.assertEqual(book.status, 'в наличии')

    def test_str_method(self):
        book = Book(title="Название", author="Автор", id=5, year="2000")
        expected_str = f"id: {book.id}\nНазвание: Название\nАвтор: Автор\nГод издания: 2000\nСтатус: в наличии\n"
        self.assertEqual(str(book), expected_str)

if __name__ == '__main__':
    unittest.main()