# Web Scraper przy użyciu BeautifulSoup/selenium

Ten projekt to prosty web scraper w Pythonie, który wykorzystuje bibliotekę BeautifulSoup do pobierania danych (np. tytułów książek i autorów) ze strony oraz zapisu wyników do pliku CSV.

## Struktura projektu

/web_scraping_lubimyczytac/
│
├── main.py                  # Uruchamia skrypt, kontroluje przepływ
├── scrapper.py              # Zawiera logikę Selenium do pobierania danych
├── table_utils.py           # Operacje na danych (np. analiza, czyszczenie, eksport do CSV)
└── books.csv                # Plik wyjściowy z danymi (tworzony przez program)
