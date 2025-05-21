# Object-Oriented Refactoring of Lubimyczytac.pl Web Scraper

This document provides an overview of the object-oriented refactoring of the Lubimyczytac.pl web scraper. The refactoring aims to improve code organization, maintainability, and reusability by applying object-oriented programming principles and design patterns.

## Project Structure

The refactored project has the following structure:

```
web_scraping_lubimyczytac/
├── models/                  # Data models
│   ├── __init__.py
│   └── book.py              # Book class representing a book with all its attributes
├── repositories/            # Data access classes
│   ├── __init__.py
│   └── book_repository.py   # BookRepository class for saving, loading, and converting book data
├── scrapers/                # Web scraping classes
│   ├── __init__.py
│   └── book_scraper.py      # BookScraper class for scraping book data from Lubimyczytac.pl
├── main_oop.py              # Object-oriented version of the main application
└── ...                      # Other files from the original project
```

## Key Classes

### Book

The `Book` class represents a book with all its attributes. It provides methods for converting to and from different formats, including lists, dictionaries, and Goodreads format.

```python
from models.book import Book

# Create a book
book = Book(
    book_id="1",
    title="Example Title",
    author="Example Author",
    # ... other attributes
)

# Convert to list
book_list = book.to_list()

# Convert to dictionary
book_dict = book.to_dict()

# Convert to Goodreads dictionary
goodreads_dict = book.to_goodreads_dict()
```

### BookRepository

The `BookRepository` class handles saving, loading, and converting book data. It provides static methods for these operations.

```python
from repositories.book_repository import BookRepository
from models.book import Book

# Save books to CSV
books = [Book(...), Book(...)]
BookRepository.save_books_to_csv(books, "dane/books.csv")

# Load books from CSV
books = BookRepository.load_books_from_csv("dane/books.csv")

# Convert to Goodreads format
BookRepository.convert_books_to_goodreads("dane/books_enriched.csv", "dane/goodreads.csv")
```

### BookScraper

The `BookScraper` class handles scraping book data from Lubimyczytac.pl. It provides methods for scraping a user's profile, extracting book data, getting book details, and enriching book data with ISBN and original titles.

```python
from scrapers.book_scraper import BookScraper

# Use with statement to manage WebDriver lifecycle
with BookScraper(headless=False) as scraper:
    # Scrape books from a user's profile
    books = scraper.scrape_profile("https://lubimyczytac.pl/profil/123456")
    
    # Enrich books with ISBN and original titles
    enriched_books = scraper.enrich_books(books)
```

### ScraperApp

The `ScraperApp` class orchestrates the scraping process, data processing, and file operations. It provides methods for each step of the process and a run method that orchestrates the entire process.

```python
from main import ScraperApp

# Create and run the application
app = ScraperApp()
app.run()
```

## Design Patterns Used

The refactored code uses several design patterns:

1. **Repository Pattern**: The `BookRepository` class abstracts data access operations, making it easier to change the data storage mechanism in the future.

2. **Facade Pattern**: The `ScraperApp` class provides a simplified interface to the complex subsystems, making it easier to use the application.

3. **Context Manager Pattern**: The `BookScraper` class implements the context manager protocol (`__enter__` and `__exit__`), making it easier to manage the WebDriver lifecycle.

## Benefits of the Refactoring

The refactoring provides several benefits:

1. **Improved Code Organization**: The code is organized into classes with clear responsibilities, making it easier to understand and maintain.

2. **Better Encapsulation**: Data and behavior are encapsulated within classes, reducing global state and making the code more robust.

3. **Increased Reusability**: The classes can be reused in different contexts, making it easier to extend the application.

4. **Enhanced Testability**: The classes can be tested in isolation, making unit testing easier.

5. **Clearer Dependencies**: Dependencies between components are explicit through class relationships, making the code easier to understand.

## How to Use the Refactored Code

To use the refactored code, run the `main_oop.py` script:

```bash
python main.py
```

This will execute the same steps as the original `main.py` script, but using the object-oriented code.

You can also use the individual classes in your own code, as shown in the examples above.

## Backward Compatibility

The refactored code maintains backward compatibility with the original code. The `BookRepository` class can handle both `Book` objects and lists, making it easy to transition from the procedural code to the object-oriented code.