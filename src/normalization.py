import re
import unicodedata
import pandas as pd


# Common business/legal abbreviations.
# Keep this conservative for the first experiment.
ABBREVIATIONS = {
    "pvt": "private",
    "pvtltd": "private limited",
    "ltd": "limited",
    "inc": "incorporated",
    "corp": "corporation",
    "co": "company",
    "llc": "limited liability company",
    "plc": "public limited company",
}


def normalize_text(value):
    """
    General text normalization.

    Steps:
    1. Handle missing values
    2. Unicode normalization
    3. Lowercase
    4. Replace punctuation with spaces
    5. Normalize whitespace
    """

    if pd.isna(value):
        return ""

    text = str(value)

    # Unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # Lowercase
    text = text.lower()

    # Replace punctuation/symbols with spaces
    text = re.sub(r"[^\w\s]", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def normalize_business_name(value):
    """
    Normalize a business name.

    We intentionally keep this conservative in version 1.
    """

    text = normalize_text(value)

    if not text:
        return ""

    tokens = text.split()

    normalized_tokens = []

    for token in tokens:
        # Remove simple dots/spacing artifacts already handled
        # and normalize selected legal abbreviations.
        normalized_tokens.append(
            ABBREVIATIONS.get(token, token)
        )

    return " ".join(normalized_tokens)


def normalize_address(value):
    """
    Normalize a business address.

    Address normalization is deliberately conservative.
    """

    text = normalize_text(value)

    if not text:
        return ""

    # Common address abbreviations.
    address_replacements = {
        r"\brd\b": "road",
        r"\bst\b": "street",
        r"\bave\b": "avenue",
        r"\bav\b": "avenue",
        r"\bblvd\b": "boulevard",
        r"\bhwy\b": "highway",
        r"\bln\b": "lane",
        r"\bdr\b": "drive",
        r"\bct\b": "court",
        r"\bpkwy\b": "parkway",
    }

    for pattern, replacement in address_replacements.items():
        text = re.sub(pattern, replacement, text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


def normalize_country(value):
    """
    Normalize country values.
    """

    if pd.isna(value):
        return ""

    return normalize_text(value)


def add_normalized_columns(df):
    """
    Add normalized business name, address and country columns.

    Original columns are preserved.
    """

    result = df.copy()

    result["business_name_normalized"] = (
        result["business_name"]
        .apply(normalize_business_name)
    )

    result["business_address_normalized"] = (
        result["business_address"]
        .apply(normalize_address)
    )

    result["country_normalized"] = (
        result["country"]
        .apply(normalize_country)
    )

    return result