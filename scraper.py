# import re
# import requests
# from bs4 import BeautifulSoup
# from csv_writer import write_to_csv

# def get_max_page(url, headers):
#     """
#     Pobiera stronę i wyciąga maksymalną liczbę stron z atrybutu data-maxpage
#     znajdującego się w elemencie input.
#     """
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         print("Błąd pobierania strony:", response.status_code)
#         return 1
#     soup = BeautifulSoup(response.text, 'html.parser')
#     pagination_input = soup.select_one('input.paginationList__input.jsPagerInput')
#     if pagination_input and pagination_input.has_attr('data-maxpage'):
#         try:
#             return int(pagination_input['data-maxpage'])
#         except ValueError:
#             pass
#     # Alternatywnie, spróbuj wyciągnąć liczbę stron z innego elementu
#     info = soup.select_one('li.paginationList__info span')
#     if info:
#         try:
#             return int(info.get_text(strip=True))
#         except ValueError:
#             pass
#     return 1

# def scrape_books(url, headers):
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         print("Błąd pobierania strony:", response.status_code)
#         return []
    
#     soup = BeautifulSoup(response.text, 'html.parser')
#     books = []
    
#     # Iterujemy po każdym bloku książki
#     for block in soup.select('div.authorAllBooks__single'):
#         book = {}
        
#         # ID książki z atrybutu id (np. "listBookElement5095549")
#         id_attr = block.get('id', '')
#         match = re.search(r'listBookElement(\d+)', id_attr)
#         if match:
#             book['id'] = match.group(1)
        
#         # Tytuł
#         title_elem = block.select_one('a.authorAllBooks__singleTextTitle')
#         if title_elem:
#             book['title'] = title_elem.get_text(strip=True)
        
#         # Autor
#         author_elem = block.select_one('div.authorAllBooks__singleTextAuthor a')
#         if author_elem:
#             book['author'] = author_elem.get_text(strip=True)
        
#         # Cykl
#         cycle_elem = block.select_one('div.listLibrary__info--cycles a')
#         book['cycle'] = cycle_elem.get_text(strip=True) if cycle_elem else None
        
#         # Średnia ocen
#         avg_rating_elem = block.select_one('span.listLibrary__ratingStarsNumber')
#         if avg_rating_elem:
#             book['avg_rating'] = avg_rating_elem.get_text(strip=True)
        
#         # Liczba ocen – usuwamy tekst "ocen"
#         rating_count_elem = block.select_one('div.listLibrary__ratingAll')
#         if rating_count_elem:
#             rating_text = rating_count_elem.get_text(strip=True)
#             book['rating_count'] = rating_text.replace('ocen', '').strip()
        
#         # Czytelnicy i Opinie – iterujemy po wszystkich spanach w kontenerze
#         readers = None
#         opinions = None
#         for span in block.select('div.l-h-1-3 span'):
#             text = span.get_text(strip=True)
#             if text.startswith("Czytelnicy:"):
#                 readers = text.replace("Czytelnicy:", "").strip()
#             elif text.startswith("Opinie:"):
#                 opinions = text.replace("Opinie:", "").strip()
#         book['readers'] = readers
#         book['opinions'] = opinions
        
#         books.append(book)
#     return books

# if __name__ == "__main__":
#     # Nowy base URL z parametrem page; używamy formatu, aby łatwo zmieniać numer strony
#     base_url = ("https://lubimyczytac.pl/profil/605200/stokuj/biblioteczka/lista?"
#                 "page={page}&listId=booksFilteredList&shelfs=4553078&showFirstLetter=0"
#                 "&objectId=605200&own=0&paginatorType=Standard")
    
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
#     }
    
#     # Pobieramy maksymalną liczbę stron z pierwszej strony
#     first_page_url = base_url.format(page=1)
#     max_page = get_max_page(first_page_url, headers)
#     print(f"Znaleziono {max_page} stron.")
    
#     all_books = []
#     # Iterujemy po stronach od 1 do max_page
#     for page in range(1, max_page + 1):
#         url = base_url.format(page=page)
#         print(f"Pobieranie strony: {url}")
#         books = scrape_books(url, headers)
#         all_books.extend(books)
    
#     if all_books:
#         write_to_csv(all_books, "books.csv")
#         print(f"Pobrano łącznie {len(all_books)} książek i zapisano do pliku books.csv")
#     else:
#         print("Nie znaleziono książek.")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Inicjalizacja przeglądarki
driver = webdriver.Chrome()
driver.get('https://lubimyczytac.pl/profil/605200/stokuj/biblioteczka/lista?shelfs=4553078')

# Akceptacja ciasteczek
try:
    accept_cookies_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Akceptuję"]'))
    )
    accept_cookies_button.click()
except:
    pass  # Jeśli przycisk nie pojawi się, przejdź dalej

all_books = []

while True:
    # Poczekaj na załadowanie książek
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'authorAllBooks__single')))

    # Pobierz informacje o książkach
    books = driver.find_elements(By.CLASS_NAME, 'authorAllBooks__single')
    for book in books:
        book_id = book.get_attribute('id').replace('listBookElement', '')
        title = book.find_element(By.CLASS_NAME, 'authorAllBooks__singleTextTitle').text.strip()
        author = book.find_element(By.CLASS_NAME, 'authorAllBooks__singleTextAuthor').text.strip()
        cycle_element = book.find_elements(By.CLASS_NAME, 'listLibrary__info--cycles')
        if cycle_element:
            cycle = cycle_element[0].text
            if len(cycle) > 6:
                cycle = cycle[6:]  # Usuwa pierwsze 6 znaków
            else:
                cycle = ''  # Jeśli tekst jest krótszy niż 6 znaków, przypisuje pusty ciąg
        else:
            cycle = ''  # Jeśli element nie istnieje, przypisuje pusty ciąg
        avg_rating_element = book.find_elements(By.CLASS_NAME, 'listLibrary__ratingStarsNumber')
        avg_rating = avg_rating_element[0].text.strip() if avg_rating_element else ''
        rating_count_element = book.find_elements(By.CLASS_NAME, 'listLibrary__ratingAll')
        rating_count = rating_count_element[0].text.replace('ocen', '').strip() if rating_count_element else ''
        readers_opinions = book.find_elements(By.CLASS_NAME, 'small.grey')
        readers = opinions = ''
        for ro in readers_opinions:
            text = ro.text.replace('\n', ' ').strip()
            if 'Czytelnicy:' in text:
                readers = text.replace('Czytelnicy:', '').strip()
            elif 'Opinie:' in text:
                opinions = text.replace('Opinie:', '').strip()
        all_books.append([book_id, title, author, cycle, avg_rating, rating_count, readers, opinions])

    # Sprawdź, czy jest przycisk "Następna strona"
    try:
        next_button = driver.find_element(By.CLASS_NAME, 'next-page')
        if 'disabled' in next_button.get_attribute('class'):
            break
        next_button.click()
        time.sleep(2)  # Poczekaj na załadowanie nowej strony
    except:
        break

# Zapisz dane do pliku CSV
with open('books.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['ID', 'Tytuł', 'Autor', 'Cykl', 'Średnia ocena', 'Liczba ocen', 'Czytelnicy', 'Opinie'])
    writer.writerows(all_books)

driver.quit()
