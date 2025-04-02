from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

from selenium.webdriver.chrome.options import Options

# Tworzenie obiektu Options dla Chrome
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Nowy tryb headless dostępny od Chrome 109

# Inicjalizacja przeglądarki
driver = webdriver.Chrome(options=chrome_options)
#driver.get('https://lubimyczytac.pl/profil/605200/stokuj/biblioteczka/lista?shelfs=4553078')
driver.get('https://lubimyczytac.pl/profil/132005/corkaksiegarza/biblioteczka/lista?shelfs=847500')
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

        # Pobranie informacji o cyklu
        cycle_element = book.find_elements(By.CLASS_NAME, 'listLibrary__info--cycles')
        if cycle_element:
            cycle = cycle_element[0].text
            if len(cycle) > 6:
                cycle = cycle[6:]  # Usuwa pierwsze 6 znaków
            else:
                cycle = ''  # Jeśli tekst jest krótszy niż 6 znaków, przypisuje pusty ciąg
        else:
            cycle = ''  # Jeśli element nie istnieje, przypisuje pusty ciąg

        # Pobranie ocen
        rating_elements = book.find_elements(By.CLASS_NAME, 'listLibrary__rating')

        # To jest średnia ocena
        try:
            avg_rating_element = rating_elements[0].find_elements(By.CLASS_NAME, 'listLibrary__ratingStarsNumber')
            avg_rating = avg_rating_element[0].text.strip() if avg_rating_element else ''
        except:
            avg_rating = ''
        try:
            # To jest ocena usera
            user_rating_element = rating_elements[1].find_elements(By.CLASS_NAME, 'listLibrary__ratingStarsNumber')
            user_rating = user_rating_element[0].text.strip() if user_rating_element else ''
        except:
            user_rating = ''

        # Pobranie liczby ocen
        rating_count_element = book.find_elements(By.CLASS_NAME, 'listLibrary__ratingAll')
        rating_count = rating_count_element[0].text.replace('ocen', '').strip() if rating_count_element else ''

        # Pobranie liczby czytelników i opinii
        readers_opinions = book.find_elements(By.CLASS_NAME, 'small.grey')
        readers = opinions = ''
        for ro in readers_opinions:
            text = ro.text.replace('\n', ' ').strip()
            if 'Czytelnicy:' in text:
                readers = text.replace('Czytelnicy:', '').strip()
            elif 'Opinie:' in text:
                opinions = text.replace('Opinie:', '').strip()

        # Dodanie zebranych danych do listy
        all_books.append([book_id, title, author, cycle, avg_rating, rating_count, readers, opinions, user_rating])



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
    writer.writerow(['ID', 'Tytuł', 'Autor', 'Cykl', 'Średnia ocena', 'Liczba ocen', 'Czytelnicy', 'Opinie', 'Ocena użytkownika'])
    writer.writerows(all_books)

driver.quit()
