import re
import math


def extract_features(password):
    """
    Convert a password into numerical features for the ML model.
    """

    length = len(password)

    uppercase_count = sum(1 for c in password if c.isupper())
    lowercase_count = sum(1 for c in password if c.islower())
    digit_count = sum(1 for c in password if c.isdigit())
    special_count = sum(
        1 for c in password
        if not c.isalnum()
    )

    unique_characters = len(set(password))

    has_uppercase = int(bool(re.search(r"[A-Z]", password)))
    has_lowercase = int(bool(re.search(r"[a-z]", password)))
    has_digit = int(bool(re.search(r"\d", password)))
    has_special = int(bool(re.search(r"[^A-Za-z0-9]", password)))

    # Detect simple predictable sequences
    lower = password.lower()

    sequences = [
        "123", "234", "345", "456",
        "567", "678", "789",
        "abc", "bcd", "cde",
        "qwerty", "asdf"
    ]

    has_sequence = int(
        any(sequence in lower for sequence in sequences)
    )

    # Detect repeated characters such as aaa or 111
    has_repeated_characters = int(
        bool(re.search(r"(.)\1\1", password))
    )

    # Detect common password patterns
    common_passwords = {
        "password",
        "password123",
        "123456",
        "12345678",
        "qwerty",
        "admin",
        "admin123",
        "welcome",
        "letmein",
        "abc123"
    }

    is_common_password = int(
        lower in common_passwords
    )

    # Approximate character-space entropy
    character_pool = 0

    if has_lowercase:
        character_pool += 26

    if has_uppercase:
        character_pool += 26

    if has_digit:
        character_pool += 10

    if has_special:
        character_pool += 32

    entropy = (
        length * math.log2(character_pool)
        if character_pool > 0
        else 0
    )

    return [
        length,
        uppercase_count,
        lowercase_count,
        digit_count,
        special_count,
        unique_characters,
        has_uppercase,
        has_lowercase,
        has_digit,
        has_special,
        has_sequence,
        has_repeated_characters,
        is_common_password,
        round(entropy, 2)
    ]


FEATURE_NAMES = [
    "length",
    "uppercase_count",
    "lowercase_count",
    "digit_count",
    "special_count",
    "unique_characters",
    "has_uppercase",
    "has_lowercase",
    "has_digit",
    "has_special",
    "has_sequence",
    "has_repeated_characters",
    "is_common_password",
    "entropy"
]