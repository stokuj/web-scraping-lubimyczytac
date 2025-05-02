from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time

from selenium.common.exceptions import TimeoutException

def get_isbn_from_book_page(driver, url):
    # jeśli URL jest nieprawidłowy, od razu zwracamy puste dane
    if not url or not url.startswith("http"):
        print(f"❌ Nieprawidłowy URL: {url}")
        return '', 'BRAK'
    
    isbn = ''
    original_title = 'BRAK'
    try:
        driver.get(url)

        # czekamy, aż strona się załaduje
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'head'))
        )

        # --- pobranie ISBN ---
        try:
            isbn_meta = driver.find_element(
                By.XPATH, '//meta[@property="books:isbn"]'
            )
            isbn = isbn_meta.get_attribute("content").strip()
        except:
            isbn = ''
        
        # Próba pobrania całej sekcji szczegółów
        try:
            # Oczekiwanie na załadowanie sekcji szczegółów
            details_section = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "book-details"))
            )
            
            # Pobierz całą zawartość HTML sekcji
            section_content = details_section.get_attribute("innerHTML")
            # print("=== ZAWARTOŚĆ SEKCJI SZCZEGÓŁÓW ===")
            # print(section_content)
            # print("===================================")
            start = section_content.find("Tytuł oryginału:")
            if start != -1:
                start = section_content.find("<dd>", start)
                end = section_content.find("</dd>", start)
                original_title = section_content[start+4:end].strip()
                #print(original_title)


        except TimeoutException:
            print(f"🔍 Nie znaleziono sekcji szczegółów książki na stronie {url}")
            original_title = "BRAK"
            
        except TimeoutException:
            # nie znaleziono dt -> zostawiamy default 'BRAK'
            print(f"🔍 Nie znaleziono sekcji 'Tytuł oryginału' na stronie {url}")
        
    except Exception as e:
        print(f"Błąd pobierania danych z {url}: {e}")
        original_title = 'test'       
    return isbn, original_title


def scrape_books(profile_url):
    chrome_options = Options()
    # chrome_options.add_argument("--headless=new")  # Tryb bezgłowy, jeśli potrzebujesz
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(profile_url)

    # Akceptacja ciasteczek, jeśli przycisk się pojawi
    try:
        accept_btn = WebDriverWait(driver, 10).until(
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
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'authorAllBooks__single'))
            )
        except TimeoutException:
            print("Brak książek na stronie — zakończono zbieranie.")
            break
        
        books = driver.find_elements(By.CLASS_NAME, 'authorAllBooks__single')

        for book in books:
            # ID książki
            try:
                book_id = book.get_attribute('id').replace('listBookElement', '')
            except:
                book_id = ''

            # Tytuł
            try:
                title = book.find_element(By.CLASS_NAME, 'authorAllBooks__singleTextTitle').text.strip()
            except:
                title = ''

            # Autor
            try:
                author = book.find_element(By.CLASS_NAME, 'authorAllBooks__singleTextAuthor').text.strip()
            except:
                author = ''

            # Link do książki
            try:
                book_link = book.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                book_link = ''

            # ISBN
            isbn = '' # Tymczasowo pusty, będzie uzupełniony później
            
            # Oryginalny tytuł
            original_title = '' # Tymczasowo pusty, będzie uzupełniony później
            
            # Cykl
            try:
                cycle_elem = book.find_elements(By.CLASS_NAME, 'listLibrary__info--cycles')
                cycle = cycle_elem[0].text[6:] if cycle_elem and len(cycle_elem[0].text) > 6 else ''
            except:
                cycle = ''

            # Średnia ocena
            try:
                rating_elements = book.find_elements(By.CLASS_NAME, 'listLibrary__rating')
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
                rating_count = book.find_element(
                    By.CLASS_NAME, 'listLibrary__ratingAll'
                ).text.replace('ocen', '').strip()
            except:
                rating_count = ''

            # Liczba czytelników i liczba opinii
            try:
                for ro in book.find_elements(By.CLASS_NAME, 'small.grey'):
                    text = ro.text.strip()
                    if 'Czytelnicy:' in text:
                        readers = text.replace('Czytelnicy:', '').strip()
                    elif 'Opinie:' in text:
                        opinions = text.replace('Opinie:', '').strip()
            except:
                readers = ''
                opinions = '' # zostają domyślne puste stringi

            # Data przeczytania
            try:
                read_date_elem = book.find_element(By.CLASS_NAME, 'authorAllBooks__read-dates')
                read_date = read_date_elem.text.replace('Przeczytał:', '').strip()
            except:
                read_date = '' # zostają domyślne puste stringi
            
            # Półki (shelves) oraz półki użytkownika (self_shelves)
            try:
                shelf_elem = book.find_element(By.CLASS_NAME, 'authorAllBooks__singleTextShelfRight')
                all_shelf_names = [a.text.strip() for a in shelf_elem.find_elements(By.TAG_NAME, 'a')]

                standard_shelves = {"Przeczytane", "Teraz czytam", "Chcę przeczytać"}
                shelves = ', '.join([s for s in all_shelf_names if s in standard_shelves])
                self_shelves = ', '.join([s for s in all_shelf_names if s not in standard_shelves])
            except:
                shelves = ''
                self_shelves = ''


            # Dodaj dane o książce do listy
            all_books.append([
                book_id,               # ID
                title,                 # Tytuł
                author,                # Autor
                isbn,                  # ISBN
                cycle,                 # Cykl
                avg_rating,            # Średnia ocena
                rating_count,          # Liczba ocen
                readers,               # Czytelnicy
                opinions,              # Opinie
                user_rating,           # Ocena użytkownika
                book_link,             # Link
                read_date,             # Data przeczytania
                shelves,               # Na półkach Główne
                self_shelves,          # Na półkach Pozostałe
                original_title         # Polski Tytuł (czyli na końcu!)
            ])

        # Przejście do następnej strony
        try:
            next_button = driver.find_element(By.CLASS_NAME, 'next-page')
            if 'disabled' in next_button.get_attribute('class'):
                break
            next_button.click()
            time.sleep(0.2)  # Poczekaj na załadowanie strony
        except:
            break  # Nie ma przycisku lub już ostatnia strona

    driver.quit()
    return all_books

def fill_isbn_and_original_titles(books):

    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)

    for book in books:
        link = book[10]
        isbn, original_title = get_isbn_from_book_page(driver, link)
        book[3] = isbn
        if original_title != 'BRAK':
            book[14] = original_title
        else:
            book[14] = book[1]
        

    driver.quit()
    return books