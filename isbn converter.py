import unittest
# Set of testcases
tests=[['0306406152', '9780306406157'],
   ['0679406417', '9780679406419'],
   ['048665088X', '9780486650883'],
   ['0140449132', '9780140449136'],
   ['0198526636', '9780198526636'],
   ['080442957X', '9780804429573'],
   ['0812979656', '9780812979657'],
   ['067978327X', '9780679783275'],
   ['0385472579', '9780385472579']]

class TestISBNConversion(unittest.TestCase):

    def test_isbn10_to_isbn13(self):
        # Valid cases
        for u,v in tests:
            self.assertEqual(convert_isbn10_to_isbn13(u), v)
        # Invalid Case
        self.assertEqual(convert_isbn10_to_isbn13('030640615X'), '9'*13)
        

    def test_isbn13_to_isbn10(self):
        # Valid cases
        for u,v in tests:
            self.assertEqual(convert_isbn13_to_isbn10(v), u)
        # Invalid Case
        self.assertEqual(convert_isbn13_to_isbn10('9780306406151'), '9'*10)

def get_check_sum13(s):
    """
    Calculates the checksum for a 13-digit ISBN 
    Args:
        s (str): A string of the first 12 digits of a 13-digit ISBN.
    Returns:
        str: The calculated checksum as a single character
    """
    check_sum=0
    # Each digit is multiplied by 1 or 3 based on its position (odd/even index)
    for ind,c in enumerate(s):
        check_sum+= int(c) * (1 if ind%2==0 else 3)
    # Subtract the last digit of the sum from 10 to get the checksum
    check_sum= 10-check_sum%10
    # If the check_sum is 10, set checksum to 0
    if check_sum==10:
        check_sum= 0
    return str(check_sum)
    
def get_check_sum10(s):
    """
    Calculates the checksum for a 10-digit ISBN .
    Args:
        s (str): A string of the first 9 digits of a 10-digit ISBN.
    Returns:
        str: The calculated checksum as a single character
    """
    check_sum=0
    d={10:'X',11:0}
    # For each digit, multiply by (10 - index) and add to checksum
    for ind,c in enumerate(s):
        check_sum+= (10-ind)* int(c)
    # Calculate checksum as 11 minus the remainder of checksum divided by 11
    check_sum= 11 - (check_sum%11)
    # Replace checksum with 'X' if 10, or 0 if 11
    if check_sum in d:
        check_sum=d[check_sum]
    return str(check_sum)
    
def check_isbn10(s):
    """
    Checks if a given string is a valid 10-digit ISBN.
    The function validates the following conditions:
        - The length of the string is 10.
        - The last character is either 'X' or a digit, and all other characters are digits.
        - The checksum matches the last character.
    Args:
        s (str): A string representing a 10-digit ISBN.
    Returns:
        bool: True if the string is a valid ISBN-10, False otherwise.
    """
    if (len(s)!=10 or s[-1]!='X' and not s[-1].isdigit()) or not s[:-1].isdigit() or get_check_sum10(s[:-1])!=s[-1]:
        return False
    return True

def check_isbn13(s):
    """
    Checks if a given string is a valid 13-digit ISBN.
    The function validates the following conditions:
        - The length of the string is 13.
        - The string starts with '978'.
        - All characters are digits.
        - The checksum matches the last character.
    Args:
        s (str): A string representing a 13-digit ISBN.
    Returns:
        bool: True if the string is a valid ISBN-13, False otherwise.
    """
    if len(s)!=13 or not s.startswith('978') or not s.isdigit() or get_check_sum13(s[:-1])!=s[-1]:
        return False
    return True


def convert_isbn10_to_isbn13(isbn10):
    """
    Converts a 10-digit ISBN to its 13-digit equivalent.
    Args:
        isbn10 (str): A valid 10-digit ISBN.
    Returns:
        str: The corresponding 13-digit ISBN.
    """

    # If the give input is invalid ISBN10, We will return 9999999999999 as a invalid ISBN13
    # We can also return False or raise an exception insted, by changing the return statement
    if not check_isbn10(isbn10):
        return '9'*13
    # Discard the check digit and add 978 to the beginning
    s='978'+isbn10[:-1]
    # Calculate ISBN10 check sum and append it to s
    return s+get_check_sum13(s)

def convert_isbn13_to_isbn10(isbn13):
    """
    Converts a valid 13-digit ISBN to its 10-digit equivalent.
    Args:
        isbn13 (str): A valid 13-digit ISBN.
    Returns:
        str: The corresponding 10-digit ISBN.
    """

    # If the give input is bad ISBN13, We will return 999999999 as a invalid ISBN10
    # We can also return False or raise an exception insted, by changing the return statement
    if not check_isbn13(isbn13):
        return '9'*10
    # Discard the first three digits(978) and the last check digit
    s=isbn13[3:-1]
    # Calculate ISBN13 check sum and append it to s
    return s+get_check_sum10(s)

# In the code, we are returning 999999999 to represent that an invalid ISBN13 was given as input. (we can also return False or raise Error. I chose to do it this way)
# In the code, we are returning 9999999999999 to represent that an invalid ISBN10 was given as input. (we can also return False or raise Error. I chose to do it this way)

# Basic calls 
print(convert_isbn10_to_isbn13('0306406152'))
print(convert_isbn13_to_isbn10('9780306406157'))

# Testing with testcases
unittest.main()
