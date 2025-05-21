"""
Book model for the Lubimyczytac.pl web scraper.

This module contains the Book class that represents a book with all its attributes.
"""

class Book:
    """
    Represents a book with all its attributes.
    
    This class encapsulates all the data for a book scraped from Lubimyczytac.pl.
    It provides methods for converting to and from different formats.
    """
    
    def __init__(self, book_id="", title="", author="", isbn="", cycle="", 
                 avg_rating="", rating_count="", readers="", opinions="", 
                 user_rating="", book_link="", read_date="", shelves="", 
                 self_shelves="", original_title=""):
        """
        Initialize a Book object with the given attributes.
        
        Args:
            book_id (str): The ID of the book
            title (str): The Polish title of the book
            author (str): The author of the book
            isbn (str): The ISBN of the book
            cycle (str): The cycle/series the book belongs to
            avg_rating (str): The average rating of the book
            rating_count (str): The number of ratings for the book
            readers (str): The number of readers for the book
            opinions (str): The number of opinions for the book
            user_rating (str): The user's rating of the book
            book_link (str): The link to the book's page
            read_date (str): The date the book was read
            shelves (str): The shelves the book is on (main)
            self_shelves (str): The shelves the book is on (user-defined)
            original_title (str): The original title of the book
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.cycle = cycle
        self.avg_rating = avg_rating
        self.rating_count = rating_count
        self.readers = readers
        self.opinions = opinions
        self.user_rating = user_rating
        self.book_link = book_link
        self.read_date = read_date
        self.shelves = shelves
        self.self_shelves = self_shelves
        self.original_title = original_title
    
    @classmethod
    def from_list(cls, book_list):
        """
        Create a Book object from a list of attributes.
        
        Args:
            book_list (list): A list of book attributes in the order:
                [book_id, title, author, isbn, cycle, avg_rating, rating_count,
                 readers, opinions, user_rating, book_link, read_date,
                 shelves, self_shelves, original_title]
        
        Returns:
            Book: A Book object with the given attributes
        """
        if len(book_list) < 15:
            # Pad the list with empty strings if it's too short
            book_list.extend([""] * (15 - len(book_list)))
        
        return cls(
            book_id=book_list[0],
            title=book_list[1],
            author=book_list[2],
            isbn=book_list[3],
            cycle=book_list[4],
            avg_rating=book_list[5],
            rating_count=book_list[6],
            readers=book_list[7],
            opinions=book_list[8],
            user_rating=book_list[9],
            book_link=book_list[10],
            read_date=book_list[11],
            shelves=book_list[12],
            self_shelves=book_list[13],
            original_title=book_list[14]
        )
    
    def to_list(self):
        """
        Convert the Book object to a list of attributes.
        
        Returns:
            list: A list of book attributes in the order:
                [book_id, title, author, isbn, cycle, avg_rating, rating_count,
                 readers, opinions, user_rating, book_link, read_date,
                 shelves, self_shelves, original_title]
        """
        return [
            self.book_id,
            self.title,
            self.author,
            self.isbn,
            self.cycle,
            self.avg_rating,
            self.rating_count,
            self.readers,
            self.opinions,
            self.user_rating,
            self.book_link,
            self.read_date,
            self.shelves,
            self.self_shelves,
            self.original_title
        ]
    
    def to_dict(self):
        """
        Convert the Book object to a dictionary.
        
        Returns:
            dict: A dictionary with the book's attributes
        """
        return {
            'ID': self.book_id,
            'Polski Tytuł': self.title,
            'Autor': self.author,
            'ISBN': self.isbn,
            'Cykl': self.cycle,
            'Średnia ocena': self.avg_rating,
            'Liczba ocen': self.rating_count,
            'Czytelnicy': self.readers,
            'Opinie': self.opinions,
            'Ocena użytkownika': self.user_rating,
            'Link': self.book_link,
            'Data przeczytania': self.read_date,
            'Na półkach Głowne': self.shelves,
            'Na półkach Pozostałe': self.self_shelves,
            'Tytuł': self.original_title
        }
    
    @classmethod
    def from_dict(cls, book_dict):
        """
        Create a Book object from a dictionary.
        
        Args:
            book_dict (dict): A dictionary with the book's attributes
        
        Returns:
            Book: A Book object with the given attributes
        """
        return cls(
            book_id=book_dict.get('ID', ''),
            title=book_dict.get('Polski Tytuł', ''),
            author=book_dict.get('Autor', ''),
            isbn=book_dict.get('ISBN', ''),
            cycle=book_dict.get('Cykl', ''),
            avg_rating=book_dict.get('Średnia ocena', ''),
            rating_count=book_dict.get('Liczba ocen', ''),
            readers=book_dict.get('Czytelnicy', ''),
            opinions=book_dict.get('Opinie', ''),
            user_rating=book_dict.get('Ocena użytkownika', ''),
            book_link=book_dict.get('Link', ''),
            read_date=book_dict.get('Data przeczytania', ''),
            shelves=book_dict.get('Na półkach Głowne', ''),
            self_shelves=book_dict.get('Na półkach Pozostałe', ''),
            original_title=book_dict.get('Tytuł', '')
        )
    
    def to_goodreads_dict(self):
        """
        Convert the Book object to a dictionary in Goodreads format.
        
        Returns:
            dict: A dictionary with the book's attributes in Goodreads format
        """
        return {
            'Title': self.original_title or self.title,
            'Polish Title': self.title,
            'Author': self.author,
            'ISBN': self.isbn,
            'My Rating': self.user_rating,
            'Average Rating': self.avg_rating,
            'Publisher': '',  # No equivalent for Publisher
            'Binding': '',  # No equivalent for Binding
            'Year Published': '',  # No equivalent for Year Published
            'Original Publication Year': '',  # No equivalent
            'Date Read': self.read_date,
            'Date Added': '',  # No equivalent
            'Shelves': self.shelves,
            'Bookshelves': self.self_shelves,
            'My Review': ''  # No equivalent
        }
    
    def __str__(self):
        """
        Return a string representation of the Book object.
        
        Returns:
            str: A string representation of the Book object
        """
        return f"{self.title} by {self.author}"
    
    def __repr__(self):
        """
        Return a string representation of the Book object for debugging.
        
        Returns:
            str: A string representation of the Book object
        """
        return f"Book(id={self.book_id}, title='{self.title}', author='{self.author}')"