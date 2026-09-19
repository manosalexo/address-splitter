"""Split addresses into street+number and city components."""

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

COMMA_PATTERN = re.compile(r"^(.+?),\s*(.+)$")
POSTAL_CODE_PATTERN = re.compile(r"^\d{3}\s?\d{2}\s+(.+)$")
STREET_NUMBER_PATTERN = re.compile(
    r"^(.*?\s\d+[A-Za-zΑ-Ωα-ω]?(?:\s[A-Za-zΑ-Ωα-ω])?)\s+(.+)$"
)
NO_NUMBER_PATTERN = re.compile(r"^(.+?)\s{2,}(.+)$")


def split_address(address: str) -> tuple[str, str]:
    """Split an address string into (street_with_number, city).

    Handles:
    - Comma-separated: "Ermou 15, 10563 Athens" -> ("Ermou 15", "Athens")
    - Space-separated: "Ermou 15 Athens" -> ("Ermou 15", "Athens")
    - With letter suffix: "Ermou 15A Athens" -> ("Ermou 15A", "Athens")
    - No number: "Ermou Athens" -> ("Ermou Athens", "")
    - Greek addresses: "Ερμού 15, Αθήνα" -> ("Ερμού 15", "Αθήνα")
    """
    if not isinstance(address, str) or not address.strip():
        return ("", "")

    address = address.strip()

    comma_match = COMMA_PATTERN.match(address)
    if comma_match:
        street = comma_match.group(1).strip()
        city_part = comma_match.group(2).strip()
        postal_match = POSTAL_CODE_PATTERN.match(city_part)
        if postal_match:
            city_part = postal_match.group(1).strip()
        return (street, city_part)

    number_match = STREET_NUMBER_PATTERN.match(address)
    if number_match:
        return (number_match.group(1).strip(), number_match.group(2).strip())

    return (address, "")


def process_file(input_path: str, output_path: str | None = None) -> pd.DataFrame:
    """Read addresses from a file and split them into components.

    Supports CSV and Excel files (xls/xlsx).
    """
    path = Path(input_path)
    if path.suffix in (".xls", ".xlsx"):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)

    address_col = df.columns[0]
    results = df[address_col].astype(str).apply(split_address)
    df["street"] = results.apply(lambda x: x[0])
    df["city"] = results.apply(lambda x: x[1])

    if output_path:
        out = Path(output_path)
        if out.suffix in (".xls", ".xlsx"):
            df.to_excel(out, index=False)
        else:
            df.to_csv(out, index=False)

    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Split addresses into street and city")
    parser.add_argument("input", help="Input CSV or Excel file")
    parser.add_argument("-o", "--output", help="Output file (CSV or Excel)")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Error: file '{args.input}' not found", file=sys.stderr)
        sys.exit(1)

    df = process_file(args.input, args.output)
    if not args.output:
        print(df.to_string(index=False))


if __name__ == "__main__":
    main()
