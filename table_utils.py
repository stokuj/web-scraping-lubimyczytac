import csv
import os

def save_books_to_csv(books, filename):
    # Utwórz katalog, jeśli nie istnieje
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'ID', 'Tytuł', 'Autor', 'ISBN', 'Cykl', 'Średnia ocena', 'Liczba ocen',
            'Czytelnicy', 'Opinie', 'Ocena użytkownika', 'Link', 'Data przeczytania', 'Na półkach Głowne', 'Na półkach Pozostałe'
        ])
        writer.writerows(books)


def convert_books_to_goodreads(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # Print the header to debug
        print("Headers in the input CSV:", reader.fieldnames)

        fieldnames = [
            'Title', 'Author', 'ISBN', 'My Rating', 'Average Rating', 'Publisher', 
            'Binding', 'Year Published', 'Original Publication Year', 'Date Read', 
            'Date Added', 'Shelves', 'Bookshelves', 'My Review'
        ]
        
        with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                # Check if 'Na półkach Główne' exists in row and handle it
                shelves = row.get('Na półkach Głowne', '')
                bookshelves = row.get('Na półkach Pozostałe', '')
                
                goodreads_row = {
                    'Title': row.get('Tytuł', ''),
                    'Author': row.get('Autor', ''),
                    'ISBN': row.get('ISBN', ''),
                    'My Rating': row.get('Ocena użytkownika', ''),
                    'Average Rating': row.get('Średnia ocena', ''),
                    'Publisher': '',  # No equivalent for Publisher
                    'Binding': '',  # No equivalent for Binding
                    'Year Published': '',  # No equivalent for Year Published
                    'Original Publication Year': '',  # No equivalent
                    'Date Read': row.get('Data przeczytania', ''),
                    'Date Added': '',  # No equivalent
                    'Shelves': shelves,  # Shelves from 'Na półkach Główne'
                    'Bookshelves': bookshelves,  # Bookshelves from 'Na półkach Pozostałe'
                    'My Review': '',  # No equivalent
                }
                
                writer.writerow(goodreads_row)