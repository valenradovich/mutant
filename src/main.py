from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.mutant import is_mutant
from src.database import get_db, DNA

app = FastAPI(title="Mutant Detector API")

@app.get("/")
async def root():
    return {"message": "Mutant Detector API is running"}

class DNARequest(BaseModel):
    dna: List[str]

class Stats(BaseModel):
    count_mutant_dna: int
    count_human_dna: int
    ratio: float

def get_dna_string(dna_list: List[str]) -> str:
    return ",".join(dna_list)

def validate_dna_sequence(dna_list: List[str]) -> None:
    if not dna_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid DNA sequence: Empty sequence"
        )
    
    n = len(dna_list)
    valid_chars = set('ATCG')
    
    if any(len(row) != n for row in dna_list):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid DNA sequence: Not a square matrix"
        )
    
    for row in dna_list:
        if not all(c in valid_chars for c in row):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid DNA sequence: Invalid characters found"
            )

@app.post("/mutant/")
async def check_mutant(dna_request: DNARequest, db: Session = Depends(get_db)):
    validate_dna_sequence(dna_request.dna)
    
    # converting DNA list to string for storage
    dna_string = get_dna_string(dna_request.dna)
    
    existing_dna = db.query(DNA).filter(DNA.sequence == dna_string).first()
    if existing_dna:
        if existing_dna.is_mutant:
            return {"message": "Mutant detected"}
        else:
            raise HTTPException(status_code=403, detail="Forbidden: Not a mutant")
    
    # processing new DNA
    mutant_result = is_mutant(dna_request.dna)
    
    # storing result
    new_dna = DNA(sequence=dna_string, is_mutant=mutant_result)
    db.add(new_dna)
    db.commit()
    
    if mutant_result:
        return {"message": "Mutant detected"}
    else:
        raise HTTPException(status_code=403, detail="Forbidden: Not a mutant")

@app.get("/stats/", response_model=Stats)
async def get_stats(db: Session = Depends(get_db)):
    # counting distinct sequences
    mutant_count = db.query(DNA).filter(DNA.is_mutant == True).count()
    human_count = db.query(DNA).filter(DNA.is_mutant == False).count()
    
    ratio = mutant_count / (human_count + mutant_count) if (human_count + mutant_count) > 0 else 0
    
    return Stats(
        count_mutant_dna=mutant_count,
        count_human_dna=human_count,
        ratio=round(ratio, 2)
    )