# Address Splitter

Split addresses into street+number and city components.

Supports Greek and international address formats, with or without postal codes.

## Formats handled

| Input | Street | City |
|---|---|---|
| `Ermou 15, 10563 Athens` | `Ermou 15` | `Athens` |
| `Ερμού 15, Αθήνα` | `Ερμού 15` | `Αθήνα` |
| `Stadiou 3 Thessaloniki` | `Stadiou 3` | `Thessaloniki` |
| `Ermou 15A Athens` | `Ermou 15A` | `Athens` |

## Python usage

```bash
pip install -r requirements.txt

# Process a CSV file
python address_splitter.py addresses.csv

# Save output to a file
python address_splitter.py addresses.csv -o output.csv

# Works with Excel files too
python address_splitter.py addresses.xlsx -o output.xlsx
```

As a library:

```python
from address_splitter import split_address, process_file

street, city = split_address("Ermou 15, Athens")
df = process_file("addresses.csv", "output.csv")
```

## Tests

```bash
pytest test_address_splitter.py -v
```

## VBA version

The original VBA macro is in `addresses_split.txt`. Import it into an Excel workbook with a sheet named "addresses_split" and addresses in column A starting from A2.
