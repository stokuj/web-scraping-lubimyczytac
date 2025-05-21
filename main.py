"""
Object-oriented version of the main application module for the Lubimyczytac.pl web scraper.

This script serves as the entry point for the application. It coordinates the scraping process,
data processing, and file operations using object-oriented programming principles.
The script reads configuration from config.ini, scrapes book data from a user's profile
on Lubimyczytac.pl, and saves the data to CSV files.
"""

import configparser
from models.book import Book
from repositories.book_repository import BookRepository
from scrapers.book_scraper import BookScraper

class ScraperApp:
    """
    Main application class for the Lubimyczytac.pl web scraper.
    
    This class orchestrates the scraping process, data processing, and file operations.
    It uses the BookScraper, Book, and BookRepository classes to implement the functionality.
    """
    
    def __init__(self, config_file='config.ini'):
        """
        Initialize the ScraperApp with a configuration file.
        
        Args:
            config_file (str): Path to the configuration file
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.profile_url = self.config.get('settings', 'profile_url')
        # Append parameters to the URL to access the user's book list
        self.profile_url += '/biblioteczka/lista?page=1&listId=booksFilteredList&findString=&kolejnosc=data-dodania&listType=list&objectId=605200&own=0&paginatorType=Standard'
    
    def scrape_books(self):
        """
        Scrape book data from the user's profile.
        
        Returns:
            list: A list of Book objects
        """
        with BookScraper(headless=False) as scraper:
            books = scraper.scrape_profile(self.profile_url)
            print(f"Scraped {len(books)} books from the user's profile")
            return books
    
    def save_books(self, books, filename):
        """
        Save book data to a CSV file.
        
        Args:
            books (list): A list of Book objects
            filename (str): Path to the output CSV file
        """
        BookRepository.save_books_to_csv(books, filename)
        print(f"Saved {len(books)} books to '{filename}'")
    
    def load_books(self, filename):
        """
        Load book data from a CSV file.
        
        Args:
            filename (str): Path to the input CSV file
        
        Returns:
            list: A list of Book objects
        """
        books = BookRepository.load_books_from_csv(filename)
        print(f"Loaded {len(books)} books from '{filename}'")
        return books
    
    def enrich_books(self, books):
        """
        Enrich book data with ISBN and original titles.
        
        Args:
            books (list): A list of Book objects
        
        Returns:
            list: The same list of books, but with ISBN and original title fields populated
        """
        with BookScraper(headless=False) as scraper:
            enriched_books = scraper.enrich_books(books)
            print(f"Enriched {len(enriched_books)} books with ISBN and original titles")
            return enriched_books
    
    def convert_to_goodreads(self, input_file, output_file):
        """
        Convert book data to Goodreads format.
        
        Args:
            input_file (str): Path to the input CSV file in Lubimyczytac.pl format
            output_file (str): Path to the output CSV file in Goodreads format
        """
        BookRepository.convert_books_to_goodreads(input_file, output_file)
        print(f"Converted book data to Goodreads format and saved to '{output_file}'")
    
    def run(self):
        """
        Run the scraper application.
        
        This method orchestrates the scraping process, data processing, and file operations.
        It can be customized by uncommenting the relevant code sections.
        """
        # STEP 1: Scrape book data and save to CSV
        # Uncomment these lines to scrape books from the user's profile
        # books = self.scrape_books()
        # self.save_books(books, 'dane/books.csv')
        
        # STEP 2: Load book data from CSV
        # Uncomment this line to load previously scraped books from CSV
        books = self.load_books('dane/books.csv')
        
        # STEP 3: Enrich book data with ISBN and original titles
        # Uncomment this line to add ISBN and original titles to book data
        enriched_books = self.enrich_books(books)
        
        # STEP 4: Save enriched book data to a new CSV file
        # Uncomment this line to save the enriched book data
        self.save_books(enriched_books, 'dane/books_enriched.csv')
        
        # STEP 5: Convert book data to Goodreads format
        # Uncomment this line to convert the enriched book data to Goodreads format
        self.convert_to_goodreads('dane/books_enriched.csv', 'dane/goodreads.csv')

if __name__ == "__main__":
    app = ScraperApp()
    app.run()