from main import Book, Library, LibraryManagement
import unittest
from unittest.mock import patch, mock_open
from datetime import datetime
import os

class TestBook(unittest.TestCase):
    """
    Тестирование класса Book: инициализации создаваемого объекта и считываемого из файла, 
    проверка присваеваемых значений в поля, преобразование объекта book в словарь и из словаря в объект book
    """
    @patch('builtins.open', new_callable=mock_open, read_data="1")
    def test_initialization_with_new_id(self, mock_file): # тестирование создания нового объекта Book без указания id в init 
        book = Book(title="Горе от ума", author="Александр Грибоедов", year="1825")
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Горе от ума")
        self.assertEqual(book.author, "Александр Грибоедов")
        self.assertEqual(book.year, "1825")
        self.assertEqual(book.status, 'в наличии')

    @patch('builtins.open', new_callable=mock_open, read_data='4')
    def test_initialization_with_existing_id(self, mock_file): # тестирование создания объекта Book на основе данных, например, прочитанных из файла
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
        self.assertEqual(new_id, 2)

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

    def test_from_dict(self): # тестирование преобразования словарь в объекта book
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

    def test_str_method(self): # тестирование преобразования объекта Book в строку
        book = Book(title="Название", author="Автор", id=5, year="2000")
        expected_str = f"id: {book.id}\nНазвание: Название\nАвтор: Автор\nГод издания: 2000\nСтатус: в наличии\n"
        self.assertEqual(str(book), expected_str)

class TestLibrary(unittest.TestCase):
    """
    Тестирование методов класса Library с использованием подмены чтения и записи данных в файловой системе.
    """

    @patch('builtins.print')
    @patch.object(Library, 'save_list_book')
    @patch.object(Library, 'load_from_file_list_book')
    @patch('builtins.open', new_callable=mock_open, read_data='0')
    def test_add_book(self, mock_open, mock_load, mock_save, mock_print): # тестирование доабвления книги через библиотеку,
                                                                            # при успешном выполнении должна напечататься соответсвующая строка
        library = Library()

        library.add_book("Название", "Автор", "2000")
        self.assertEqual(len(library.books), 1)
        self.assertEqual(library.books[0].title, "Название") 
        self.assertEqual(library.books[0].author, "Автор") 
        self.assertEqual(library.books[0].year, "2000")
    
        mock_load.assert_called_once() 
        mock_save.assert_called_once() 
        mock_print.assert_called_once_with("Книга \"Название\" успешно сохранена", end='\n\n')

    @patch('builtins.print')
    @patch.object(Library, 'save_list_book')
    @patch.object(Library, 'load_from_file_list_book')
    @patch('builtins.open', new_callable=mock_open, read_data="1")
    def test_remove_book(self, mock_open, mock_load, mock_save, mock_print): # тестирование метода удаления книги через библиотеку
        library = Library()
        new_book = Book("Название", "Автор", "2000")
        library.books.append(new_book)
        self.assertEqual(len(library.books), 1)
        library.remove_book("1")
        self.assertEqual(len(library.books), 0)
        mock_load.assert_called_once() 
        mock_save.assert_called_once() 
        mock_print.assert_called_once_with("Книга \"Название\" была успешно удалена.", end='\n\n')

    @patch('builtins.print')
    @patch.object(Library, 'load_from_file_list_book')
    @patch('builtins.open', new_callable=mock_open, read_data="1")
    def test_search_book(self, mock_open, mock_load, mock_print): # тестирование поиска книги, если она будет найдена, в терминал выведется строка с данным
        library = Library()
        new_book = Book("Название", "Автор", "2000")
        library.books.append(new_book)
        library.search_book("Название")
        mock_load.assert_called_once() 
        mock_print.assert_called_once_with(new_book)

    @patch('builtins.print')
    @patch.object(Library, 'load_from_file_list_book')
    @patch('builtins.open', new_callable=mock_open, read_data="1")
    def test_search_book_no_results(self, mock_open, mock_load, mock_print): # при отсутвии книг соответствующим поисковой строке, 
                                                                            #  будет выведена уведомляющая об этом строка
        library = Library()
        new_book = Book("Название", "Автор", "2000")
        library.books.append(new_book)
        library.search_book("Другое название")
        mock_load.assert_called_once() 
        mock_print.assert_called_once_with("Ни одна книга не соответствует поисковому запросу.", end="\n\n")

    @patch('builtins.print')
    @patch.object(Library, 'save_list_book')
    @patch.object(Library, 'load_from_file_list_book')
    @patch('builtins.open', new_callable=mock_open, read_data="1")
    def test_change_book_status(self, mock_open, mock_load, mock_save, mock_print): # тестирование изменения статуса с корректным значением
        library = Library()
        new_book = Book("Название", "Автор", "2000")
        library.books.append(new_book)
        library.change_book_status("1", "выдана")
        mock_load.assert_called_once() 
        mock_print.assert_called_once_with("Статус книги \"Название\" изменен на \"выдана\"")

    @patch('builtins.print')
    @patch.object(Library, 'save_list_book')
    @patch.object(Library, 'load_from_file_list_book')
    @patch('builtins.open', new_callable=mock_open, read_data="1")
    def test_change_book_status_invalid(self, mock_open, mock_load, mock_save, mock_print):# тестирование изменения статуса с некорректным значением
        with self.assertRaises(ValueError):
            library = Library()
            new_book = Book("Название", "Автор", "2000")
            library.books.append(new_book)
            library.change_book_status("1", "другой статус")
            mock_load.assert_called_once() 
            mock_print.assert_called_once_with("Статус должен быть одним из следующих: в наличии, выдана")
    
    @patch('builtins.print')
    @patch.object(Library, 'save_list_book')
    @patch.object(Library, 'load_from_file_list_book')
    @patch('builtins.open', new_callable=mock_open, read_data="1")
    def test_print_list_books(self, mock_open, mock_load, mock_save, mock_print): # тестирование вывода списка книг в терминал
        library = Library()
        new_book1 = Book("Название1", "Автор1", "2000")
        new_book2 = Book("Название2", "Автор2", "2000")
        library.books.append(new_book1)
        library.books.append(new_book2)
        library.print_list_books()
        mock_load.assert_called_once() 
        mock_print.assert_any_call("Список книг в библиотеке:")
        mock_print.assert_any_call(new_book1)
        mock_print.assert_any_call(new_book2)

    @patch('builtins.print')
    @patch.object(Library, 'load_from_file_list_book')
    @patch('builtins.open', new_callable=mock_open, read_data="1")
    def test_print_list_books_empty(self, mock_open, mock_load, mock_print): # тестирование вывода пустого списка книг
        library = Library()
        library.print_list_books()
        mock_load.assert_called_once() 
        mock_print.assert_called_once_with('В библиотеке нет книг', end='\n\n')


if __name__ == '__main__':
    unittest.main()