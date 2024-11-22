import json
import os
import uuid
from datetime import datetime


class Book:
    id_counter = 0

    def __init__(self, title, author, year, id=None, status='в наличии'):
        self.validate_title(title)
        self.validate_author(author)
        self.validate_year(year)

        self.title = title
        self.author = author
        self.year = year
        self.status = status
        if not id:
            self.id = Book.get_id_counter()
        else:
            self.id = id

    def validate_title(self, title):
        if len(title.strip()) == 0 or not isinstance(title, str):
            raise ValueError("Название книги должно быть не пустой строкой.")

    def validate_author(self, author):
        if len(author.strip()) == 0 or not isinstance(author, str):
            raise ValueError("Имя автора должно быть не пустой строкой.")

    def validate_year(self, year):
        if len(year.strip()) != 4 or not year.isdigit() or int(year) > datetime.now().year:
            raise ValueError(
                "Год издания книги должен быть числом от 1000 до текущего года.")

    @classmethod
    def get_id_counter(cls):
        counter_filename = 'counter.txt'
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

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['title'], data['author'], data['year'], data['id'], data['status'])

    def __str__(self):
        return f"id: {self.id}\nНазвание: {self.title}\nАвтор: {self.author}\nГод издания: {self.year}\nСтатус: {self.status}\n"


class Library:
    filename = 'library.json'

    def __init__(self):
        self.books = []

    def add_book(self, title, author, year):
        new_book = Book(title, author, year)
        self.load_from_file_list_book()
        self.books.append(new_book)
        self.save_list_book()
        print(f"Книга \"{title}\" успешно сохранена", end='\n\n')

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        self.validate_status(new_status)
        self._status

    def validate_status(self, new_status):
        valid_statuses = ['в наличии', 'выдана']
        if status.lower() not in [s.lower() for s in valid_statuses]:
            raise ValueError(f"Статус должен быть одним из следующих: {', '.join(valid_statuses)}")
            
    def remove_book(self, id):
        if not id.isdigit():
            raise ValueError("ID книги должен быть числом.")
        id = int(id)
        self.load_from_file_list_book()
        book_found = False

        for book in self.books:
            if book.id == id:
                book_found = True
                self.books = [book for book in self.books if book.id != id]
                self.save_list_book()
        if book_found:
            print(f"Книга \"{book.title}\" была успешно удалена.", end='\n\n')
        else:
            raise ValueError(f"Книга с ID {id} не найдена.\n\n")

    def search_book(self, search_field):
        self.load_from_file_list_book()
        search_books = []
        for book in self.books:
            if book.title == search_field or book.author == search_field or book.year == search_field:
                search_books.append(book)
                print(book)
        if not search_books:
            print("Ни одна книга не соответсвует поисковому запросу.", end="\n\n")

    def change_book_status(self, id, new_status):
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

    def save_list_book(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump([book.to_dict() for book in self.books], f, indent=4)
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON: {e}")
        except Exception as e:
            raise RuntimeError(f"Возникло исключение: {e}\n\n")

    def load_from_file_list_book(self):
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

    def print_list_books(self):
        self.load_from_file_list_book()
        if self.books:
            print("Список книг в библиотеке:")
            for book in self.books:
                print(book)
        else:
            print('В библиотеке нет книг', end='\n\n')


class LibraryManagement:
    library = Library()

    def add_book_in_library(self):
        title = input("Введите название книги: ")
        author = input("Введите автора: ")
        year = input("Введите год издания: ")
        self.library.add_book(title, author, year)

    def delete_book_from_library(self):
        id = input("Введите ID книги, которую хотите удалить: ")
        self.library.remove_book(id)

    def search_book_in_library(self):
        search_field = input(
            "Введите название или автора или год издания книги для поиска в библиотеке: ")
        self.library.search_book(search_field)

    def change_book_status_in_library(self):
        id = input("Введите ID книги, статус которой хотите изменить: ")
        new_status = input(
            "Введите новый статус (\"в наличии\" или \"выдана\"): ")
        self.library.change_book_status(id, new_status)

    def start_managing_library(self):
        print("Добро пожаловать в библиотеку!")
        while True:
            try:
                menu = int(input(
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


l = LibraryManagement()
l.start_managing_library()
