"""
Book scraper for the Lubimyczytac.pl web scraper.

This module contains the BookScraper class that handles scraping book data
from Lubimyczytac.pl.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
from models.book import Book

class BookScraper:
    """
    Scraper for book data from Lubimyczytac.pl.
    
    This class handles scraping book data from a user's profile and
    extracting detailed information about each book.
    """
    
    def __init__(self, headless=False):
        """
        Initialize the BookScraper with a WebDriver.
        
        Args:
            headless (bool): Whether to run the browser in headless mode
        """
        self.driver = None
        self.headless = headless
    
    def __enter__(self):
        """
        Set up the WebDriver when entering a context.
        
        Returns:
            BookScraper: The BookScraper instance
        """
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=chrome_options)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Clean up the WebDriver when exiting a context.
        
        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def scrape_profile(self, profile_url):
        """
        Scrape book data from a user's profile on Lubimyczytac.pl.
        
        This method navigates through all pages of a user's book list,
        extracting detailed information about each book.
        
        Args:
            profile_url (str): URL of the user's profile page
        
        Returns:
            list: A list of Book objects
        """
        if not self.driver:
            raise ValueError("WebDriver not initialized. Use with statement.")
        
        self.driver.get(profile_url)
        
        # Akceptacja ciasteczek, jeśli przycisk się pojawi
        try:
            accept_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Akcept")]'))
            )
            time.sleep(1)
            accept_btn.click()
        except:
            print("Nie znaleziono przycisku akceptacji ciasteczek.")
        
        all_books = []
        
        while True:
            # Czekaj aż książki się załadują
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'authorAllBooks__single'))
                )
            except TimeoutException:
                print("Brak książek na stronie — zakończono zbieranie.")
                break
            
            books = self.driver.find_elements(By.CLASS_NAME, 'authorAllBooks__single')
            
            for book in books:
                # Extract book data
                book_data = self._extract_book_data(book)
                all_books.append(book_data)
            
            # Przejście do następnej strony
            try:
                next_button = self.driver.find_element(By.CLASS_NAME, 'next-page')
                if 'disabled' in next_button.get_attribute('class'):
                    break
                next_button.click()
                time.sleep(1)  # Poczekaj na załadowanie strony
            except:
                break  # Nie ma przycisku lub już ostatnia strona
        
        return all_books
    
    def _extract_book_data(self, book_element):
        """
        Extract data from a book element.
        
        Args:
            book_element: Selenium WebElement representing a book
        
        Returns:
            Book: A Book object with the extracted data
        """
        # ID książki
        try:
            book_id = book_element.get_attribute('id').replace('listBookElement', '')
        except:
            book_id = ''
        
        # Tytuł
        try:
            title_element = book_element.find_element(By.CLASS_NAME, 'authorAllBooks__singleTextTitle')
            title = title_element.text
            if isinstance(title, str):
                title = title.strip()
        except:
            title = ''
        
        # Autor
        try:
            author = book_element.find_element(By.CLASS_NAME, 'authorAllBooks__singleTextAuthor').text.strip()
        except:
            author = ''
        
        # Link do książki
        try:
            book_link = book_element.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            book_link = ''
        
        # ISBN
        isbn = '' # Tymczasowo pusty, będzie uzupełniony później
        
        # Oryginalny tytuł
        original_title = '' # Tymczasowo pusty, będzie uzupełniony później
        
        # Cykl
        try:
            cycle_elem = book_element.find_elements(By.CLASS_NAME, 'listLibrary__info--cycles')
            cycle = cycle_elem[0].text[6:] if cycle_elem and len(cycle_elem[0].text) > 6 else ''
        except:
            cycle = ''
        
        # Średnia ocena
        try:
            rating_elements = book_element.find_elements(By.CLASS_NAME, 'listLibrary__rating')
            avg_rating = rating_elements[0].find_element(
                By.CLASS_NAME, 'listLibrary__ratingStarsNumber'
            ).text.strip()
        except:
            avg_rating = ''
        
        # Ocena użytkownika
        try:
            user_rating = rating_elements[1].find_element(
                By.CLASS_NAME, 'listLibrary__ratingStarsNumber'
            ).text.strip()
        except:
            user_rating = ''
        
        # Liczba ocen
        try:
            rating_count = book_element.find_element(
                By.CLASS_NAME, 'listLibrary__ratingAll'
            ).text.replace('ocen', '').strip()
        except:
            rating_count = ''
        
        # Liczba czytelników i liczba opinii
        readers = ''
        opinions = ''
        try:
            for ro in book_element.find_elements(By.CLASS_NAME, 'small.grey'):
                text = ro.text.strip()
                if 'Czytelnicy:' in text:
                    readers = text.replace('Czytelnicy:', '').strip()
                elif 'Opinie:' in text:
                    opinions = text.replace('Opinie:', '').strip()
        except:
            pass # zostają domyślne puste stringi
        
        # Data przeczytania
        try:
            read_date_elem = book_element.find_element(By.CLASS_NAME, 'authorAllBooks__read-dates')
            read_date = read_date_elem.text.replace('Przeczytał:', '').strip()
        except:
            read_date = '' # zostają domyślne puste stringi
        
        # Półki (shelves) oraz półki użytkownika (self_shelves)
        shelves = ''
        self_shelves = ''
        try:
            shelf_elem = book_element.find_element(By.CLASS_NAME, 'authorAllBooks__singleTextShelfRight')
            all_shelf_names = [a.text.strip() for a in shelf_elem.find_elements(By.TAG_NAME, 'a')]
            
            standard_shelves = {"Przeczytane", "Teraz czytam", "Chcę przeczytać"}
            shelves = ', '.join([s for s in all_shelf_names if s in standard_shelves])
            self_shelves = ', '.join([s for s in all_shelf_names if s not in standard_shelves])
        except:
            pass # zostają domyślne puste stringi
        
        # Create and return a Book object
        return Book(
            book_id=book_id,
            title=title,
            author=author,
            isbn=isbn,
            cycle=cycle,
            avg_rating=avg_rating,
            rating_count=rating_count,
            readers=readers,
            opinions=opinions,
            user_rating=user_rating,
            book_link=book_link,
            read_date=read_date,
            shelves=shelves,
            self_shelves=self_shelves,
            original_title=original_title
        )
    
    def get_book_details(self, book):
        """
        Get additional details for a book.
        
        This method visits the book's page to extract additional information
        that is not available on the user's profile page.
        
        Args:
            book (Book): A Book object with at least the book_link attribute set
        
        Returns:
            Book: The same Book object, but with ISBN and original title fields populated
        """
        if not self.driver:
            raise ValueError("WebDriver not initialized. Use with statement.")
        
        url = book.book_link
        
        # Return the book unchanged if URL is invalid
        if not url or not url.startswith("http"):
            print(f"❌ Nieprawidłowy URL: {url}")
            return book
        
        try:
            self.driver.get(url)
            
            # czekamy, aż strona się załaduje
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, 'head'))
            )
            
            # --- pobranie ISBN ---
            try:
                isbn_meta = self.driver.find_element(
                    By.XPATH, '//meta[@property="books:isbn"]'
                )
                book.isbn = isbn_meta.get_attribute("content").strip()
            except:
                book.isbn = ''
            
            # Próba pobrania całej sekcji szczegółów
            try:
                # Oczekiwanie na załadowanie sekcji szczegółów
                details_section = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, "book-details"))
                )
                
                # Pobierz całą zawartość HTML sekcji
                section_content = details_section.get_attribute("innerHTML")
                start = section_content.find("Tytuł oryginału:")
                if start != -1:
                    start = section_content.find("<dd>", start)
                    end = section_content.find("</dd>", start)
                    book.original_title = section_content[start+4:end].strip()
                else:
                    book.original_title = "BRAK"
            
            except TimeoutException:
                print(f"🔍 Nie znaleziono sekcji szczegółów książki na stronie {url}")
                book.original_title = "BRAK"
            
        except Exception as e:
            print(f"Błąd pobierania danych z {url}: {e}")
            book.original_title = 'BRAK'
        
        # If original title is not found, use the Polish title
        if book.original_title == 'BRAK':
            book.original_title = book.title
        
        return book
    
    def enrich_books(self, books):
        """
        Enrich book data with ISBN and original titles.
        
        This method visits each book's page to extract additional information
        that is not available on the user's profile page.
        
        Args:
            books (list): A list of Book objects
        
        Returns:
            list: The same list of books, but with ISBN and original title fields populated
        """
        if not self.driver:
            raise ValueError("WebDriver not initialized. Use with statement.")
        
        for book in books:
            self.get_book_details(book)
        
        return books