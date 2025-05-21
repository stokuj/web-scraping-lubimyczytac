"""
Book repository for the Lubimyczytac.pl web scraper.

This module contains the BookRepository class that handles saving, loading,
and converting book data.
"""

import csv
import os
from models.book import Book

class BookRepository:
    """
    Repository for book data operations.
    
    This class handles saving, loading, and converting book data to and from
    different formats.
    """
    
    @staticmethod
    def save_books_to_csv(books, filename):
        """
        Save book data to a CSV file.
        
        Args:
            books (list): A list of Book objects
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
            
            # Convert Book objects to lists and write to CSV
            for book in books:
                if isinstance(book, Book):
                    writer.writerow(book.to_list())
                else:
                    # For backward compatibility, handle lists directly
                    writer.writerow(book)
    
    @staticmethod
    def load_books_from_csv(filename):
        """
        Load book data from a CSV file.
        
        Args:
            filename (str): Path to the input CSV file
        
        Returns:
            list: A list of Book objects
        """
        books = []
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader, None)  # Skip header row
            for row in reader:
                books.append(Book.from_list(row))
        return books
    
    @staticmethod
    def convert_books_to_goodreads(input_file, output_file):
        """
        Convert book data from Lubimyczytac.pl format to Goodreads format.
        
        This method reads book data from a CSV file in the format produced by
        save_books_to_csv() and converts it to a format that can be imported into
        Goodreads.
        
        Args:
            input_file (str): Path to the input CSV file in Lubimyczytac.pl format
            output_file (str): Path to the output CSV file in Goodreads format
        """
        # Load books from CSV
        books = BookRepository.load_books_from_csv(input_file)
        
        # Define Goodreads fieldnames
        fieldnames = [
            'Title', 'Polish Title', 'Author', 'ISBN', 'My Rating', 'Average Rating', 'Publisher', 
            'Binding', 'Year Published', 'Original Publication Year', 'Date Read', 
            'Date Added', 'Shelves', 'Bookshelves', 'My Review'
        ]
        
        # Write books to Goodreads CSV
        with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for book in books:
                writer.writerow(book.to_goodreads_dict())