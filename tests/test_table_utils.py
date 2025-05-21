import os
import csv
import pytest
from repositories.book_repository import BookRepository
from models.book import Book

def test_save_and_load_books(sample_books, temp_csv_file):
    """Test saving books to CSV and loading them back."""
    # Convert sample_books to Book objects
    books = [Book.from_list(book) for book in sample_books]

    # Save books to CSV
    BookRepository.save_books_to_csv(books, temp_csv_file)

    # Verify file exists
    assert os.path.exists(temp_csv_file)

    # Load books from CSV
    loaded_books = BookRepository.load_books_from_csv(temp_csv_file)

    # Verify loaded books match original books
    assert len(loaded_books) == len(books)
    for i in range(len(books)):
        assert loaded_books[i].to_list() == books[i].to_list()

def test_convert_books_to_goodreads(sample_books, temp_csv_file, tmp_path):
    """Test converting books to Goodreads format."""
    # Convert sample_books to Book objects
    books = [Book.from_list(book) for book in sample_books]

    # Save books to CSV
    BookRepository.save_books_to_csv(books, temp_csv_file)

    # Define output file
    goodreads_file = os.path.join(tmp_path, "goodreads.csv")

    # Convert to Goodreads format
    BookRepository.convert_books_to_goodreads(temp_csv_file, goodreads_file)

    # Verify Goodreads file exists
    assert os.path.exists(goodreads_file)

    # Read Goodreads file and verify content
    with open(goodreads_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

        # Verify number of rows
        assert len(rows) == len(books)

        # Verify first book data
        assert rows[0]['Title'] == 'Original Title 1'
        assert rows[0]['Polish Title'] == 'Tytuł Polski 1'
        assert rows[0]['Author'] == 'Autor 1'
        assert rows[0]['ISBN'] == 'ISBN1'
        assert rows[0]['My Rating'] == '5'
        assert rows[0]['Average Rating'] == '4.5'
        assert rows[0]['Date Read'] == '2023-01-01'
        assert rows[0]['Shelves'] == 'Przeczytane'
        assert rows[0]['Bookshelves'] == 'Fantasy, Sci-Fi'
