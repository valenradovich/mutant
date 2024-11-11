import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import Base, get_db

# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Mutant Detector API is running"}

def test_check_mutant(client):
    dna = {
        "dna": [
            "ATGCGA",
            "CAGTGC",
            "TTATGT",
            "AGAAGG",
            "CCCCTA",
            "TCACTG"
        ]
    }
    response = client.post("/mutant/", json=dna)
    assert response.status_code == 200
    assert response.json() == {"message": "Mutant detected"}

def test_check_human(client):
    dna = {
        "dna": [
            "ATGCGA",
            "CAGTGC",
            "TTATTT",
            "AGACGG",
            "GCGTCA",
            "TCACTG"
        ]
    }
    response = client.post("/mutant/", json=dna)
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden: Not a mutant"}

def test_duplicate_dna(client):
    dna = {
        "dna": [
            "ATGCGA",
            "CAGTGC",
            "TTATGT",
            "AGAAGG",
            "CCCCTA",
            "TCACTG"
        ]
    }
    # First request
    response = client.post("/mutant/", json=dna)
    assert response.status_code == 200
    
    # Duplicate request
    response = client.post("/mutant/", json=dna)
    assert response.status_code == 200
    assert response.json() == {"message": "Mutant detected"}

def test_stats_empty_db(client):
    response = client.get("/stats/")
    assert response.status_code == 200
    assert response.json() == {
        "count_mutant_dna": 0,
        "count_human_dna": 0,
        "ratio": 0
    }

def test_stats_with_data(client):
    # Add a mutant
    mutant_dna = {
        "dna": [
            "ATGCGA",
            "CAGTGC",
            "TTATGT",
            "AGAAGG",
            "CCCCTA",
            "TCACTG"
        ]
    }
    client.post("/mutant/", json=mutant_dna)
    
    # Add a human
    human_dna = {
        "dna": [
            "ATGCGA",
            "CAGTGC",
            "TTATTT",
            "AGACGG",
            "GCGTCA",
            "TCACTG"
        ]
    }
    client.post("/mutant/", json=human_dna)
    
    response = client.get("/stats/")
    assert response.status_code == 200
    stats = response.json()
    assert stats["count_mutant_dna"] == 1
    assert stats["count_human_dna"] == 1
    assert stats["ratio"] == 0.5 

def test_invalid_dna_length(client):
    """Test DNA sequence with invalid length"""
    dna = {
        "dna": [
            "ATGCGA",
            "CAGTGC",
            "TTATGT",
            "AGAAGG",
            "CCCCTA"  # Only 5 sequences instead of 6
        ]
    }
    response = client.post("/mutant/", json=dna)
    assert response.status_code == 400
    assert "Invalid DNA sequence" in response.json()["detail"]

def test_invalid_dna_characters(client):
    """Test DNA sequence with invalid characters"""
    dna = {
        "dna": [
            "ATGCGA",
            "CAGTGC",
            "TTATGT",
            "AGAAGG",
            "CCCCTA",
            "TCACT1"  # Contains a number
        ]
    }
    response = client.post("/mutant/", json=dna)
    assert response.status_code == 400
    assert "Invalid characters found" in response.json()["detail"]

def test_empty_dna(client):
    """Test empty DNA sequence"""
    dna = {"dna": []}
    response = client.post("/mutant/", json=dna)
    assert response.status_code == 400
    assert "Empty sequence" in response.json()["detail"]

def test_invalid_json_format(client):
    """Test invalid JSON format"""
    response = client.post("/mutant/", json={})
    assert response.status_code == 422

def test_non_square_matrix(client):
    """Test DNA sequence that's not a square matrix"""
    dna = {
        "dna": [
            "ATGCGA",
            "CAGTGC",
            "TTAT",  # Shorter sequence
            "AGAAGG",
            "CCCCTA",
            "TCACTG"
        ]
    }
    response = client.post("/mutant/", json=dna)
    assert response.status_code == 400
    assert "Not a square matrix" in response.json()["detail"]

def test_invalid_request_method(client):
    """Test invalid HTTP method"""
    response = client.put("/mutant/", json={"dna": []})
    assert response.status_code == 405

def test_stats_calculation(client):
    """Test stats calculation with multiple requests"""
    # Add multiple different mutants
    mutant_dnas = [
        {
            "dna": [
                "ATGCGA",
                "CAGTGC",
                "TTATGT",
                "AGAAGG",
                "CCCCTA",
                "TCACTG"
            ]
        },
        {
            "dna": [
                "ATGCGA",
                "ATGTGC",
                "ATATGT",
                "AGAAGG",
                "CCCCTA",
                "TCACTG"
            ]
        },
        {
            "dna": [
                "AAAAGA",
                "CAGTGC",
                "TTATGT",
                "AGAAGG",
                "CCCCTA",
                "TCACTG"
            ]
        }
    ]
    
    for dna in mutant_dnas:
        client.post("/mutant/", json=dna)
    
    # Add different humans
    human_dnas = [
        {
            "dna": [
                "ATGCGA",
                "CAGTGC",
                "TTATTT",
                "AGACGG",
                "GCGTCA",
                "TCACTG"
            ]
        },
        {
            "dna": [
                "GTGCGA",
                "CAGTGC",
                "TTATTT",
                "AGACGG",
                "GCGTCA",
                "TCACTG"
            ]
        }
    ]
    
    for dna in human_dnas:
        client.post("/mutant/", json=dna)
    
    response = client.get("/stats/")
    assert response.status_code == 200
    stats = response.json()
    assert stats["count_mutant_dna"] == 3
    assert stats["count_human_dna"] == 2
    assert stats["ratio"] == 0.6

def test_database_connection(client):
    """Test database connection and session management"""
    response = client.get("/")
    assert response.status_code == 200
    
def test_stats_calculation_with_duplicates(client):
    """Test stats calculation with duplicate DNA sequences"""
    mutant_dna = {
        "dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
    }
    
    # Submit same DNA multiple times
    for _ in range(3):
        client.post("/mutant/", json=mutant_dna)
    
    response = client.get("/stats/")
    stats = response.json()
    assert stats["count_mutant_dna"] == 1  # Should only count unique sequences
    assert stats["count_human_dna"] == 0
    assert stats["ratio"] == 1.0

def test_concurrent_requests(client):
    """Test handling of concurrent requests"""
    dna1 = {
        "dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
    }
    dna2 = {
        "dna": ["ATGCGA", "CAGTGC", "TTATTT", "AGACGG", "GCGTCA", "TCACTG"]
    }
    
    response1 = client.post("/mutant/", json=dna1)
    response2 = client.post("/mutant/", json=dna2)
    
    assert response1.status_code == 200
    assert response2.status_code == 403