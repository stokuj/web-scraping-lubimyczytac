#csv_writer.py     

import csv

def write_to_csv(data, filename):
    if not data:
        print("Brak danych do zapisu.")
        return
    # Załóżmy, że każdy element listy to słownik z tymi samymi kluczami
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
