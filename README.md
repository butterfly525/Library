# Library
Описание 
Консольное приложение для управления библоитекой книг. Приложение использует объектно-ориентированный подход и хранит данные о книгах в формате JSON.    
Приложение позволяет добавлять, удалять, искать и отображать книги.    
Каждая книга содержит поля:    
- id (уникальный идентиикатор, является счетчиком: при добавлнии книги увеличивается на 1)
- title (название книги)
- author (автор книги)
- year (год извания книги)
- статус книги (может быть "выдана" или "в наличии")

Функциональные возможности:
- Добавление книги: пользователи могут добавлять новые книги, указывая title, author и year. status по умолчанию = "в наличии".
- Удаление книги из библиотеки по id.
- Поиск книги по title, author или year.
- Отображение списка книг, хранящихся в библиотеке, с их id, title, author, year.
- Изменение статуса книги: пользователи могут изменять статус книги на "в наличии" или "выдана".


Структура проекта
Классы:
- Book    
Хранит информацию о книге (ID, название, автор, год публикации, статус).
Методы для преобразования объекта в словарь и обратно.
Валидация полей при создании экземпляра.
- Library    
Управляет списком книг.
Методы для добавления, удаления, поиска книг и изменения их статусов.
Сохранение и загрузка списка книг из файла.
- LibraryManagement    
Обеспечивает взаимодействие между пользователем и библиотекой.
Запрашивает ввод данных от пользователя и вызывает соответствующие методы класса Library.


Установка    
Для запуска проекта необходимо:    
1) Убедиться, что установлен Python 3.8.    
2) Склонировать репозиторий на компьютер: git clone https://github.com/butterfly525/Library.git     
3) Перейти в папку с проектом: cd Library.   
4) Запустить приложение с помощью команды: python main.py    



Модуль тестирования

Тесты написаны с использованием библиотеки unittest и обеспечивают проверку корректности работы методов, а также валидацию входных данных.    

Класс TestBook    
test_initialization_with_new_id: проверяет создание нового объекта Book без указания id, ожидая, что id будет равен 1.    
test_initialization_with_existing_id: проверяет создание объекта Book с указанным id, который был прочитан из файла.    
test_title_setter_invalid: проверяет, что при попытке установить пустое название книги выбрасывается исключение ValueError.    
test_author_setter_invalid: проверяет, что при попытке установить пустое имя автора выбрасывается исключение ValueError.    
test_year_setter_invalid: проверяет различные сценарии установки года публикации, включая будущие годы и некорректные значения.    
test_status_setter_invalid: проверяет, что при установке недопустимого статуса выбрасывается исключение ValueError.    
test_get_id_counter: проверяет правильность получения id из файла.    
test_to_dict: проверяет преобразование объекта Book в словарь.    
test_from_dict: проверяет создание объекта Book из словаря.    
test_str_method: проверяет корректность строкового представления объекта Book.   
     

Класс TestLibrary    
test_add_book: проверяет добавление книги в библиотеку и правильность сохранения данных.    
test_remove_book: проверяет удаление книги из библиотеки по id.    
test_search_book: проверяет поиск книги по названию и вывод информации о найденной книге.    
test_search_book_no_results: проверяет сценарий, когда книга не найдена по заданному запросу.    
test_change_book_status: проверяет изменение статуса книги на "выдана".    
test_change_book_status_invalid: проверяет обработку попытки установить недопустимый статус.    
test_print_list_books: проверяет вывод списка книг в консоль.    
test_print_list_books_empty: проверяет вывод сообщения о пустом списке книг.    


Запуск тестов    
Для запуска тестов необходимо выполнить следующий команду в терминале: python -m unittest test.py