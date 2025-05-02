# 📚 Web Scraper przy użyciu Selenium

Ten projekt to prosty, ale elastyczny web scraper napisany w Pythonie, służący do zbierania danych z portalu **Lubimyczytać.pl**. Głównym celem jest automatyczne pobieranie informacji o książkach (np. tytuł, autor, ocena, półki użytkownika) z publicznego profilu użytkownika, a następnie zapisanie ich do pliku CSV w celu dalszej analizy.


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

## 🧠 Możliwe rozszerzenia

- Użycie SQLite lub pandas do dalszej analizy
- Eksport do Excela lub JSON
- GUI (np. przy użyciu Tkintera lub PyWebIO)
- Automatyczne logowanie (jeśli wymagane dla prywatnych danych)
- Obsługa wielu użytkowników jednocześnie
