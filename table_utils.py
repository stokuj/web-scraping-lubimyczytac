"""
Utility module for data processing and CSV operations.

This module provides functions for saving, loading, and converting book data
to and from CSV files. It handles the data structure used by the scraper and
provides conversion to Goodreads format for import into Goodreads.
"""

import csv
import os

def save_books_to_csv(books, filename):
    """
    Save book data to a CSV file.

    Args:
        books (list): A list of book data as returned by scrape_books()
        filename (str): Path to the output CSV file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
    'ID', 'Polski Tytuł', 'Autor', 'ISBN', 'Cykl', 'Średnia ocena', 'Liczba ocen',
    'Czytelnicy', 'Opinie', 'Ocena użytkownika', 'Link', 'Data przeczytania',
    'Na półkach Głowne', 'Na półkach Pozostałe', 'Tytuł'
])
        writer.writerows(books)

def load_books_from_csv(filename):
    """
    Load book data from a CSV file.

    Args:
        filename (str): Path to the input CSV file

    Returns:
        list: A list of lists, where each inner list contains data for one book
    """
    books = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader, None)  # Skip header row
        for row in reader:
            books.append(row)
    return books

def convert_books_to_goodreads(input_file, output_file):
    """
    Convert book data from Lubimyczytac.pl format to Goodreads format.

    This function reads book data from a CSV file in the format produced by
    save_books_to_csv() and converts it to a format that can be imported into
    Goodreads.

    Args:
        input_file (str): Path to the input CSV file in Lubimyczytac.pl format
        output_file (str): Path to the output CSV file in Goodreads format
    """
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        # Print the header to debug
        print("Headers in the input CSV:", reader.fieldnames)

        fieldnames = [
            'Title', 'Polish Title', 'Author', 'ISBN', 'My Rating', 'Average Rating', 'Publisher', 
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
                    'Polish Title': row.get('Polski Tytuł', ''), 
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
