import string
import secrets
import re

def generate_password(length):
    """
    Generate a random password.

    This function generates a random strong password with the specified length.

    Args:
        length (int): The length of the password.

    Returns:
        str: The generated password.

    Raises:
        None

    Example:
        >>> generate_password(12)
        'A1b@3c$5d&'

    """
    while True:
        # Define the characters to use for the password
        chars = string.ascii_letters + string.digits + string.punctuation
        # Generate a random password
        password = ''.join(secrets.choice(chars) for _ in range(length))
        if re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            break
    return password


def calculate_strength(password):
    """
    Calculates the strength of a password based on various criteria.

    Parameters:
    password (str): The password to calculate the strength for.

    Returns:
    float: The strength of the password, ranging from 0 to 1.

    """
    strength = 0;
    length = len(password)
    special_characters = "!@#$%^&*"

    # If the length is lower than 6, returns strength 0
    if length < 6:
        return strength
    # If the length is between 6 and 8, add 0.4 to the strength
    elif length >=6 and length < 8:
        strength += 0.2
    else:
        strength += 0.4
    
    # Check if the password contains at least one digit
    if any(char.isdigit() for char in password):
        strength += 0.2

    # Check if the password contains at least one uppercase and one lowercase letter
    if any(char.islower() for char in password) and any(char.isupper() for char in password):
        strength += 0.2
    
    # Check if the password contains at least one special character
    if any(char in special_characters for char in password):
        strength += 0.2

    return strength
