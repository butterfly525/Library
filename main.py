import json
import os
import uuid
from datetime import datetime
from typing import NoReturn, Optional, List, Dict, Union


class Book:
    """
    Класс Book содержит в себе поля, описывающие одну книгу, позволяет создать объект книги.
    Инициализируемые поля проходят валидацию, id для новой книги читается из файла, увеличивается на 1, обновленное значение записывается в файл.
    Методы to_dict и from_dict позволяют преобразовать объект класса Book в элемент словарь, и обратно из словаря в объект Book соответственно.
            Описание полей класса:
            'id' - уникальный номер книги,
            'title' - название книги,
            'author' - автор книги,
            'year' - год первой публикации книги,
            'status' - статус книги в библиотеке (выдана или в наличии)
    """
    id_counter: int = 0

    def __init__(self, title: str, author: str, year: str, id: Optional[int] = None, status: str = 'в наличии'):

        self.title: str = title
        self.author: str = author
        self.year: str = year
        self.status: str = status
        if not id:
            self.id: int = Book.get_id_counter()
        else:
            self.id: int = id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> NoReturn:
        if len(value.strip()) == 0 or not isinstance(value, str):
            raise ValueError("Название книги должно быть не пустой строкой.")
        self._title = value

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value: str) -> NoReturn:
        if len(value.strip()) == 0 or not isinstance(value, str):
            raise ValueError("Имя автора должно быть не пустой строкой.")
        self._author = value

    @property
    def year(self) -> str:
        return self._year

    @year.setter
    def year(self, value: str) -> NoReturn:
        if len(value.strip()) != 4 or not value.isdigit() or int(value) > datetime.now().year:
            raise ValueError(
                "Год публикации книги должен быть числом от 1000 до текущего года.")
        self._year = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> NoReturn:
        valid_statuses = ['в наличии', 'выдана']
        if value.lower() not in [s for s in valid_statuses]:
            raise ValueError(f"Статус должен быть одним из следующих: {', '.join(valid_statuses)}")
        self._status = value

    @classmethod #Получает id для книги и записывает в файл значение уваеличенное на 1
    def get_id_counter(cls) -> int:
        counter_filename: str = 'counter.txt'
        if os.path.exists(counter_filename):
            with open(counter_filename, 'r') as f:
                cls.id_counter = f.read()
                cls.id_counter = int(cls.id_counter) + 1
            with open(counter_filename, 'w') as f:
                f.write(str(cls.id_counter))
            return cls.id_counter
        else:
            with open(counter_filename, 'w') as f:
                f.write(str(cls.id_counter))
        return cls.id_counter

    def to_dict(self) -> Dict[str, Union[str, int]]: #Преобразует Book в словарь
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, int]]) -> 'Book': #Преобразует словарь в Book
        return cls(data['title'], data['author'], data['year'], data['id'], data['status'])

    def __str__(self) -> str:
        return f"id: {self.id}\nНазвание: {self.title}\nАвтор: {self.author}\nГод издания: {self.year}\nСтатус: {self.status}\n"


class Library:
    """
    Класс Library отвечает за управление книгами в библиотеке.
    Описание методов класса:
    'add_book' - создание нового объекта Book и запись в библиотеку
    'remove_book' - удаление книги из библиотеки по id
    'search_book' - поиск книги в библиотеке (производится по полным значениям полей title, author, year. 
                    Будут найдены все книги, у которых есть совпадение по любому из этих полей)
    'change_book_status' - изменение статуса книги в библиотеке, вводимый статус проходит валидацию
                             и должен иметь одно из двух значений: "выдана" или "в наличии".
    'save_list_book' - сохранение списка книнг в json-файл
    'load_from_file_list_book' - чтение списка книг из json-файла           
    'print_list_books' - вывод списка книг в консоль  
    """
    filename: str = 'library.json'

    def __init__(self):
        self.books: List[Book] = []

    def add_book(self, title, author, year) -> NoReturn: #Добавляет книгу в список books и в файл
        new_book = Book(title, author, year)
        self.load_from_file_list_book()
        self.books.append(new_book)
        self.save_list_book()
        print(f"Книга \"{title}\" успешно сохранена", end='\n\n')

    def remove_book(self, id: str) -> NoReturn: #удаляет книгу из books и из файла
        if not id.isdigit():
            raise ValueError("ID книги должен быть числом.")
        id: int = int(id)
        self.load_from_file_list_book()
        book_found: bool = False

        for book in self.books:
            if book.id == id:
                book_found = True
                self.books = [book for book in self.books if book.id != id]
                self.save_list_book()
        if book_found:
            print(f"Книга \"{book.title}\" была успешно удалена.", end='\n\n')
        else:
            raise ValueError(f"Книга с ID {id} не найдена.\n\n")

    def search_book(self, search_field: str) -> NoReturn: #выводит список книг соответствующих поисковой строке
        self.load_from_file_list_book()
        search_books = []
        for book in self.books:
            if book.title == search_field or book.author == search_field or book.year == search_field:
                search_books.append(book)
                print(book)
        if not search_books:
            print("Ни одна книга не соответсвует поисковому запросу.", end="\n\n")

    def change_book_status(self, id: str, new_status: str) -> None: # изменяет статус книги в библиотеке и обновляет файл со списком книг
        if not id.isdigit():
            raise ValueError("ID книги должен быть целым числом.")
        id = int(id)
        book_found = False
        self.load_from_file_list_book()
        for book in self.books:
            if book.id == id:
                book.status = new_status
                book_found = True
                print(f"Статус книги \"{book.title}\" изменен на \"{book.status}\"")
                self.save_list_book()
                return
        if not book_found:
            raise ValueError(f"Книга с ID {id} не найдена.\n\n")

    def save_list_book(self) -> NoReturn: # сохраняет список books в файл со списком книг
        try:
            with open(self.filename, 'w') as f:
                json.dump([book.to_dict() for book in self.books], f, indent=4)
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON: {e}")
        except Exception as e:
            raise RuntimeError(f"Возникло исключение: {e}\n\n")

    def load_from_file_list_book(self) -> NoReturn: # читает список книг из файла в books
        try:
            with open(self.filename, 'r') as f:
                books_data = json.load(f)
                self.books = [Book.from_dict(book) for book in books_data]
        except FileNotFoundError as e:
            print("Файла с библиотекой нет. Будет создан пустой файл.")
            with open(self.filename, 'w') as f:
                pass
        except json.JSONDecodeError as e:
            print(f"Ничего не прочитано из json файла с библотекой.")
        except Exception as e:
            raise RuntimeError(f"Возникло исключение: {e}")

    def print_list_books(self) -> NoReturn: # выводит в консоль список books
        self.load_from_file_list_book()
        if self.books:
            print("Список книг в библиотеке:")
            for book in self.books:
                print(book)
        else:
            print('В библиотеке нет книг', end='\n\n')


class LibraryManagement:
    """
    LibraryManagement обеспечивает взаимодействие между библиотекой книг и пользвоателем.
    'add_book_in_library' - запрашивает у пользователя данные о добавляемой книге и инициирует добавление книги в библиотеку.
    'delete_book_from_library' - запрашивает у пользователя id удаляемой книги и инициирует удаление книги из библиотеки.
    'search_book_in_library' - запрашивает у пользователя поисковую строку и инициирует поиск по библиотеке.
    'change_book_status_in_library' - запрашивает у пользователя id  и новый статус книги и инициирует изменение статуса книги в библиотеке.
    'start_managing_library' - запускает управления библиотекой для пользователя.
    """
    library: Library = Library()

    def add_book_in_library(self) -> NoReturn:
        title: str = input("Введите название книги: ")
        author: str = input("Введите автора: ")
        year: str = input("Введите год публикации: ")
        self.library.add_book(title, author, year)

    def delete_book_from_library(self) -> NoReturn:
        id: str = input("Введите ID книги, которую хотите удалить: ")
        self.library.remove_book(id)

    def search_book_in_library(self) -> NoReturn:
        search_field: str = input(
            "Введите название или автора или год публикации книги для поиска в библиотеке: ")
        self.library.search_book(search_field)

    def change_book_status_in_library(self) -> NoReturn:
        id: str = input("Введите ID книги, статус которой хотите изменить: ")
        new_status: str = input(
            "Введите новый статус (\"в наличии\" или \"выдана\"): ")
        self.library.change_book_status(id, new_status)

    def start_managing_library(self) -> NoReturn:
        print("Добро пожаловать в библиотеку!")
        while True:
            try:
                menu: int = int(input(
                    "Введите число от 1 до 6:\n\
                            1 - Добавить книгу\n\
                            2 - Удалить книгу\n\
                            3 - Поиск книги\n\
                            4 - Отображение всех книг\n\
                            5 - Изменить статус книги\n\
                            6 - Выход\n\n"))

                if menu == 1:
                    self.add_book_in_library()
                elif menu == 2:
                    self.delete_book_from_library()
                elif menu == 3:
                    self.search_book_in_library()
                elif menu == 4:
                    self.library.print_list_books()
                elif menu == 5:
                    self.change_book_status_in_library()
                elif menu == 6:
                    print("До встречи!")
                    break
                else:
                    print("Введен некорректный пункт меню", end="\n\n")
            except Exception as e:
                print(f"{e}", end="\n\n")

if __name__ == '__main__':
    l: LibraryManagement = LibraryManagement()
    l.start_managing_library()
