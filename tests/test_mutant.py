import pytest
from src.mutant import is_mutant

def test_is_mutant_horizontal():
    dna = [
        "ATGCGA",
        "CAGTGC",
        "TTATGT",
        "AGAAGG",
        "CCCCTA",
        "TCACTG"
    ]
    assert is_mutant(dna) == True

def test_is_mutant_vertical():
    dna = [
        "ATGCGA",
        "ATGTGC",
        "ATATGT",
        "AGAAGG",
        "CCCCTA",
        "TCACTG"
    ]
    assert is_mutant(dna) == True

def test_is_not_mutant():
    dna = [
        "ATGCGA",
        "CAGTGC",
        "TTATTT",
        "AGACGG",
        "GCGTCA",
        "TCACTG"
    ]
    assert is_mutant(dna) == False

def test_is_mutant_diagonal_down():
    dna = [
        "ATGCGA",
        "CAGTGC",
        "TTATGT",
        "AGAAGT",
        "CCCCTG",
        "TCACTG"
    ]
    assert is_mutant(dna) == True

def test_is_mutant_diagonal_up():
    dna = [
        "ATGCGA",
        "CAGTGC",
        "TTATGT",
        "AGAAGT",
        "ACCCTG",
        "TCACTG"
    ]
    assert is_mutant(dna) == True

def test_single_sequence():
    """Test with only one sequence (should return False)"""
    dna = [
        "ATGCGA",
        "CAGTGC",
        "TTATGT",
        "AGAATG",
        "CCCATA",
        "TCACTG"
    ]
    assert is_mutant(dna) == False

def test_multiple_sequences_same_line():
    """Test with multiple sequences in the same line"""
    dna = [
        "ATGCGA",
        "CAGTGC",
        "TTATGT",
        "AAAATT",  # Two sequences in same line
        "CCCCTA",
        "TCACTG"
    ]
    assert is_mutant(dna) == True

def test_edge_case_sequence():
    """Test sequence at the edge of the matrix"""
    dna = [
        "ATGCGA",
        "CAGTGC",
        "TTATGT",
        "AGAAGG",
        "CCCCTA",
        "AAAATG"  # Sequence at the start
    ]
    assert is_mutant(dna) == True
