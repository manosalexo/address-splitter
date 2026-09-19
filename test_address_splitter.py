"""Tests for address_splitter module."""

import tempfile
from pathlib import Path

import pytest

from address_splitter import process_file, split_address


class TestSplitAddress:
    def test_empty_string(self):
        assert split_address("") == ("", "")

    def test_whitespace_only(self):
        assert split_address("   ") == ("", "")

    def test_simple_with_number(self):
        assert split_address("Ermou 15 Athens") == ("Ermou 15", "Athens")

    def test_multi_word_street(self):
        assert split_address("Leoforos Alexandras 50 Athens") == (
            "Leoforos Alexandras 50",
            "Athens",
        )

    def test_number_with_letter_suffix(self):
        assert split_address("Ermou 15A Athens") == ("Ermou 15A", "Athens")

    def test_comma_separated(self):
        assert split_address("Ermou 15, Athens") == ("Ermou 15", "Athens")

    def test_comma_with_postal_code(self):
        assert split_address("Ermou 15, 10563 Athens") == ("Ermou 15", "Athens")

    def test_comma_with_spaced_postal_code(self):
        assert split_address("Ermou 15, 105 63 Athens") == ("Ermou 15", "Athens")

    def test_greek_address(self):
        assert split_address("Ερμού 15, Αθήνα") == ("Ερμού 15", "Αθήνα")

    def test_greek_address_with_postal(self):
        assert split_address("Ερμού 15, 10563 Αθήνα") == ("Ερμού 15", "Αθήνα")

    def test_no_number(self):
        street, city = split_address("Ermou Athens")
        assert street == "Ermou Athens"
        assert city == ""

    def test_multi_word_city(self):
        assert split_address("Ermou 15, Nea Smyrni") == ("Ermou 15", "Nea Smyrni")

    def test_number_with_single_letter_after(self):
        assert split_address("Stadiou 5 B Athens") == ("Stadiou 5 B", "Athens")

    def test_only_street_and_number(self):
        assert split_address("Ermou 15") == ("Ermou 15", "")


class TestProcessFile:
    def test_csv_processing(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as f:
            f.write("address\n")
            f.write('"Ermou 15, Athens"\n')
            f.write("Stadiou 3 Thessaloniki\n")
            f.name

        df = process_file(f.name)
        assert list(df["street"]) == ["Ermou 15", "Stadiou 3"]
        assert list(df["city"]) == ["Athens", "Thessaloniki"]
        Path(f.name).unlink()

    def test_csv_output(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as infile:
            infile.write("address\n")
            infile.write('"Ermou 15, Athens"\n')

        outpath = Path(tempfile.mktemp(suffix=".csv"))
        process_file(infile.name, str(outpath))
        assert outpath.exists()
        content = outpath.read_text()
        assert "Ermou 15" in content
        assert "Athens" in content
        Path(infile.name).unlink()
        outpath.unlink()
