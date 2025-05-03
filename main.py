from scrapper import scrape_books, fill_isbn_and_original_titles
from table_utils import save_books_to_csv, load_books_from_csv, convert_books_to_goodreads
import configparser

if __name__ == "__main__":
    # Pobieranie URL z pliku config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    profile_url = config.get('settings', 'profile_url')
    profile_url += 'biblioteczka/lista?page=1&listId=booksFilteredList&findString=&kolejnosc=data-dodania&listType=list&objectId=605200&own=0&paginatorType=Standard'

    # # Scrapowanie danych i zapis do CSV
    # books = scrape_books(profile_url)
    # save_books_to_csv(books, 'dane/books.csv')
    # print(f"Scraped {len(books)} books and saved to 'dane/books.csv'")
    
    # # Wczytanie danych z CSV
    # books_from_csv = load_books_from_csv('dane/books.csv')
    # print(f"Loaded {len(books_from_csv)} books from 'dane/books.csv'")
    
    # # Uzupełnienie ISBN i oryginalnego tytułu
    # enriched_books = fill_isbn_and_original_titles(books_from_csv)

    # # Zapis danych do nowego pliku
    # save_books_to_csv(enriched_books, 'dane/books_enriched.csv')
    # print(f"Saved enriched books to 'dane/books_enriched.csv'")
    
    # Konwersja do formatu Goodreads
    # convert_books_to_goodreads('dane/books_enriched.csv', 'dane/goodreads.csv')
    
    