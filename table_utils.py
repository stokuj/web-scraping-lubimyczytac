import csv
import os

def save_books_to_csv(books, filename):
    # Utwórz katalog, jeśli nie istnieje
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'ID', 'Tytuł', 'Autor', 'Cykl', 'Średnia ocena', 'Liczba ocen',
            'Czytelnicy', 'Opinie', 'Ocena użytkownika', 'Link', 'Data przeczytania', 'Na półkach Głowne', 'Na półkach Pozostałe'
        ])
        writer.writerows(books)
