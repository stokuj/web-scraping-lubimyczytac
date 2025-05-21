"""
Test runner script for the Lubimyczytac.pl web scraper.

This script runs all the tests in the project using pytest.
"""

import pytest
import sys

if __name__ == "__main__":
    print("Running tests for Lubimyczytac.pl web scraper...")
    
    # Run all tests
    result = pytest.main(["-v", "tests"])
    
    # Exit with the pytest result code
    sys.exit(result)