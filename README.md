# 📚 Web Scraper przy użyciu Selenium

Ten projekt to prosty, ale elastyczny web scraper napisany w Pythonie, służący do zbierania danych z portalu **Lubimyczytać.pl**. Głównym celem jest automatyczne pobieranie informacji o książkach (np. tytuł, autor, ocena, półki użytkownika) z publicznego profilu użytkownika, a następnie zapisanie ich do pliku CSV w celu dalszej analizy.

## 📋 Spis treści
- [Obsługiwane strony](#obsługiwane-strony)
- [Technologie użyte w projekcie](#-technologie-użyte-w-projekcie)
- [Struktura projektu](#-struktura-projektu)
- [Instalacja](#-instalacja)
- [Konfiguracja](#-konfiguracja)
- [Użycie](#-użycie)
- [Funkcjonalności](#-funkcjonalności)
- [Testowanie](#-testowanie)
- [Możliwe rozszerzenia](#-możliwe-rozszerzenia)

## Obsługiwane strony

- **Goodreads** — Radzi sobię z większością importem większości tyułów

## 🔧 Technologie użyte w projekcie

- **Python 3**
- **Selenium** — automatyzacja przeglądarki (Chrome)
- **ChromeDriver** — sterowanie przeglądarką Chrome

## 📁 Struktura projektu

```
/web_scraping_lubimyczytac/
│
├── main.py                  # Główna aplikacja — punkt wejścia, uruchamia scrapowanie i zapis
├── scrapper.py              # Logika pobierania danych ze strony (Selenium)
├── table_utils.py           # Przetwarzanie i zapis danych do CSV
├── dane/                    # Katalog na wygenerowane dane
│   └── books.csv            # Plik wynikowy z danymi książek
└── requirements.txt         # Lista wymaganych bibliotek
```

## ✅ Funkcjonalności

- Obsługa paginacji (przechodzi przez wszystkie strony użytkownika)
- Pobieranie szczegółowych danych o książkach:
  - Tytuł, autor, cykl
  - Średnia ocena, ocena użytkownika
  - Liczba ocen, czytelników, opinii
  - Półki (`shelves` i `self_shelfs`)
  - Data przeczytania (jeśli dostępna)
- Obsługa wyjątków i błędów (np. brak danych na stronie, timeouty)
- Zapis danych do formatu CSV

## 🧪 Testowanie

Projekt zawiera testy jednostkowe, które sprawdzają poprawność działania głównych funkcji:

- **test_table_utils.py** - testy dla funkcji przetwarzania i zapisu danych
- **test_scrapper.py** - testy dla funkcji pobierania danych ze strony
- **test_sample.py** - podstawowe testy weryfikujące działanie projektu

### Uruchamianie testów

Aby uruchomić wszystkie testy, użyj skryptu `run_tests.py`:

```
python run_tests.py
```

Możesz również uruchomić poszczególne testy za pomocą pytest:

```
pytest -v tests/test_table_utils.py
pytest -v tests/test_scrapper.py
pytest -v tests/test_sample.py
```

### Dodawanie nowych testów

Aby dodać nowe testy, utwórz nowy plik w katalogu `tests/` z nazwą zaczynającą się od `test_`. Funkcje testowe powinny również zaczynać się od `test_`.

## 📥 Instalacja

1. Sklonuj repozytorium:
   ```
   git clone https://github.com/twoj-username/web_scraping_lubimyczytac.git
   cd web_scraping_lubimyczytac
   ```

2. Zainstaluj wymagane biblioteki:
   ```
   pip install -r requirements.txt
   ```

3. Pobierz i zainstaluj ChromeDriver:
   - Pobierz odpowiednią wersję [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) dla Twojej wersji przeglądarki Chrome
   - Rozpakuj plik i umieść go w ścieżce systemowej lub w katalogu projektu

## ⚙️ Konfiguracja

1. Otwórz plik `config.ini` i ustaw URL profilu użytkownika, którego książki chcesz pobrać:
   ```ini
   [settings]
   profile_url = https://lubimyczytac.pl/profil/TWOJ_PROFIL/
   ```

2. Dostosuj parametry w pliku `main.py` według potrzeb:
   - Odkomentuj odpowiednie sekcje kodu, aby włączyć lub wyłączyć poszczególne etapy przetwarzania
   - Możesz zmienić nazwy plików wyjściowych

## 🚀 Użycie

1. Uruchom skrypt główny:
   ```
   python main.py
   ```

2. Skrypt wykona następujące operacje (w zależności od odkomentowanych sekcji):
   - Pobranie danych o książkach z profilu użytkownika
   - Zapisanie danych do pliku CSV
   - Wzbogacenie danych o ISBN i oryginalne tytuły
   - Konwersja danych do formatu Goodreads

3. Wyniki zostaną zapisane w katalogu `dane/`:
   - `books.csv` - podstawowe dane o książkach
   - `books_enriched.csv` - dane wzbogacone o ISBN i oryginalne tytuły
   - `goodreads.csv` - dane w formacie gotowym do importu do Goodreads

## 🧠 Możliwe rozszerzenia

- Użycie SQLite lub pandas do dalszej analizy
- Eksport do Excela lub JSON
- GUI (np. przy użyciu Tkintera lub PyWebIO)
- Automatyczne logowanie (jeśli wymagane dla prywatnych danych)
- Obsługa wielu użytkowników jednocześnie
- Generowanie statystyk i wykresów na podstawie zebranych danych
- Integracja z API innych serwisów książkowych

# 📚 Web Scraper using Selenium

This project is a simple yet flexible web scraper written in Python, designed to collect data from the **Lubimyczytac.pl** portal. The main goal is to automatically retrieve information about books (e.g., title, author, rating, user shelves) from a user's public profile, and then save them to a CSV file for further analysis.

## 📋 Table of Contents
- [Supported Sites](#supported-sites)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Features](#-features)
- [Testing](#-testing-1)
- [Possible Extensions](#-possible-extensions)

## Supported Sites

- **Goodreads** — Handles the import of most titles

## 🔧 Technologies Used

- **Python 3**
- **Selenium** — browser automation (Chrome)
- **ChromeDriver** — Chrome browser control

## 📁 Project Structure

```
/web_scraping_lubimyczytac/
│
├── main.py                  # Main application — entry point, runs scraping and saving
├── scrapper.py              # Logic for retrieving data from the site (Selenium)
├── table_utils.py           # Processing and saving data to CSV
├── dane/                    # Directory for generated data
│   └── books.csv            # Output file with book data
└── requirements.txt         # List of required libraries
```

## ✅ Features

- Pagination handling (navigates through all user pages)
- Retrieving detailed book data:
  - Title, author, series
  - Average rating, user rating
  - Number of ratings, readers, reviews
  - Shelves (`shelves` and `self_shelfs`)
  - Date read (if available)
- Exception and error handling (e.g., missing data on the page, timeouts)
- Saving data to CSV format

## 🧪 Testing

The project includes unit tests that verify the correctness of the main functions:

- **test_table_utils.py** - tests for data processing and saving functions
- **test_scrapper.py** - tests for web scraping functions
- **test_sample.py** - basic tests verifying project functionality

### Running Tests

To run all tests, use the `run_tests.py` script:

```
python run_tests.py
```

You can also run individual tests using pytest:

```
pytest -v tests/test_table_utils.py
pytest -v tests/test_scrapper.py
pytest -v tests/test_sample.py
```

### Adding New Tests

To add new tests, create a new file in the `tests/` directory with a name starting with `test_`. Test functions should also start with `test_`.

## 📥 Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/web_scraping_lubimyczytac.git
   cd web_scraping_lubimyczytac
   ```

2. Install required libraries:
   ```
   pip install -r requirements.txt
   ```

3. Download and install ChromeDriver:
   - Download the appropriate version of [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for your Chrome browser version
   - Extract the file and place it in your system path or in the project directory

## ⚙️ Configuration

1. Open the `config.ini` file and set the URL of the user profile you want to scrape:
   ```ini
   [settings]
   profile_url = https://lubimyczytac.pl/profil/YOUR_PROFILE/
   ```

2. Adjust parameters in the `main.py` file as needed:
   - Uncomment the appropriate code sections to enable or disable specific processing stages
   - You can change the output filenames

## 🚀 Usage

1. Run the main script:
   ```
   python main.py
   ```

2. The script will perform the following operations (depending on which sections are uncommented):
   - Scrape book data from the user's profile
   - Save the data to a CSV file
   - Enrich the data with ISBN and original titles
   - Convert the data to Goodreads format

3. Results will be saved in the `dane/` directory:
   - `books.csv` - basic book data
   - `books_enriched.csv` - data enriched with ISBN and original titles
   - `goodreads.csv` - data in a format ready for import into Goodreads

## 🧠 Possible Extensions

- Using SQLite or pandas for further analysis
- Export to Excel or JSON
- GUI (e.g., using Tkinter or PyWebIO)
- Automatic login (if required for private data)
- Handling multiple users simultaneously
- Generating statistics and charts based on collected data
- Integration with APIs of other book services
