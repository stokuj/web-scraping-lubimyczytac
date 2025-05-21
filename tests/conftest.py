"""
Pytest configuration file for the Lubimyczytac.pl web scraper tests.

This file contains fixtures that can be used by all tests in the project.
"""

import pytest
import os
import csv
from unittest.mock import MagicMock

@pytest.fixture
def sample_books():
    """Fixture providing sample book data for testing."""
    return [
        ['1', 'Tytuł Polski 1', 'Autor 1', 'ISBN1', 'Cykl 1', '4.5', '100', 
         '200', '50', '5', 'http://example.com/book1', '2023-01-01', 
         'Przeczytane', 'Fantasy, Sci-Fi', 'Original Title 1'],
        ['2', 'Tytuł Polski 2', 'Autor 2', 'ISBN2', 'Cykl 2', '4.0', '200', 
         '300', '75', '4', 'http://example.com/book2', '2023-02-01', 
         'Chcę przeczytać', 'Horror, Mystery', 'Original Title 2']
    ]

@pytest.fixture
def temp_csv_file(tmp_path):
    """Fixture providing a temporary CSV file path."""
    return os.path.join(tmp_path, "test_books.csv")

@pytest.fixture
def mock_driver():
    """Fixture providing a mock Selenium WebDriver."""
    driver = MagicMock()
    
    # Mock find_element for ISBN
    isbn_meta = MagicMock()
    isbn_meta.get_attribute.return_value = "9781234567890"
    driver.find_element.return_value = isbn_meta
    
    # Mock WebDriverWait and until
    wait_mock = MagicMock()
    driver.find_element.return_value = isbn_meta
    
    return driver