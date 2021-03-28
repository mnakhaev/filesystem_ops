import random
import string


def generate_random_string(n: int = random.randint(1, 255)) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


def create_file(filename: str) -> None:
    """Helper function to create an empty file"""
    with open(filename, "w"):
        pass
