from scrapper import scrape_books
from table_utils import save_books_to_csv

if __name__ == "__main__":
    profile_url = "https://lubimyczytac.pl/profil/605200/stokuj/biblioteczka/lista?page=1&listId=booksFilteredList&findString=&kolejnosc=data-dodania&listType=list&objectId=605200&own=0&paginatorType=Standard"
    books = scrape_books(profile_url)
    save_books_to_csv(books, 'dane/books.csv')
    print(f"Scraped {len(books)} books and saved to 'dane/books.csv'")
