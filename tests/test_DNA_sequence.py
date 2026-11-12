import pathlib
import pytest
from backend.FASTA_comparison import compare_sequences

"""
DISCLAIMER: Currently written and tested by AI.
Will include more tests in the future.
"""

def test_identical():
    result = compare_sequences("ATGCCGTAA", "ATGCCGTAA")

    assert result["variant"] == []


def test_substitution():
    result = compare_sequences("ATGCCGTAA", "ATGTCGTAA")

    assert result["variant"] == [
        {
            "type": "Substitution",
            "wt_base": "C",
            "mut_base": "T"
        }
    ]

def test_deletion():
    result = compare_sequences("ATGCCGTAA", "ATGCGTAA")

    assert result["variant"] == [
        {
            "type": "Deletion",
            "deleted_seq": "C"
        }
    ]


def test_insertion():
    result = compare_sequences("ATGCCGTAA", "ATGCCAGTAA")

    assert result["variant"] == [
        {
            "type": "Insertion",
            "inserted_seq": "A"
        }
    ]

def test_fasta_header():
    result = compare_sequences(
        ">Wildtype\nATGCCGTAA",
        ">Edited\nATGCCGTAA"
    )

    assert result["variant"] == []
