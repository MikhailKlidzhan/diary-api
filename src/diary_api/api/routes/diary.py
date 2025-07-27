from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...database import get_db
from ... import crud, schemas


router = APIRouter(
    prefix='/entries',
    tags=['diary entries']
)


@router.post('/', response_model=schemas.DiaryEntry, status_code=status.HTTP_201_CREATED)
def create_diary_entry(entry: schemas.DiaryEntryCreate, db: Session = Depends(get_db)):
    """Create  new diary entry"""
    return crud.create_diary_entry(db=db, entry=entry)


@router.get('/', response_model=List[schemas.DiaryEntry])
def read_diary_entries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all diary entries with pagination"""
    entries = crud.get_diary_entries(db=db, skip=skip, limit=limit)

    return entries
    

@router.get('/{entry_id}', response_model=schemas.DiaryEntry)
def read_diary_entry(entry_id: int, db: Session = Depends(get_db)):
    """Get a specific diary entry by ID"""
    db_entry = crud.get_diary_entry(db=db, entry_id=entry_id)
    if db_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Diary entry not found'
        )
    
    return db_entry


@router.patch('/{entry_id}', response_model=schemas.DiaryEntry)
def patch_diary_entry(entry_id: int, entry: schemas.DiaryEntryUpdate, db: Session = Depends(get_db)):
    """Partially update a diary entry"""
    db_entry = crud.update_diary_entry(db=db, entry_id=entry_id, entry=entry)
    if db_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Diary entry not found'
        )
    
    return db_entry


@router.delete('/{entry_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_diary_entry(entry_id: int, db: Session = Depends(get_db)):
    """Delete a diary entry"""
    success = crud.delete_diary_entry(db=db, entry_id=entry_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Diary entry not found'
        )
    

@router.patch('/{entry_id}/done', response_model=schemas.DiaryEntry)
def mark_entry_done(entry_id: int, is_done: bool = True, db: Session = Depends(get_db)):
    """Mark a diary entry as done/not done"""
    db_entry = crud.mark_diary_entry_done(db=db, entry_id=entry_id, is_done=is_done)
    if db_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Diary entry not found'
        )
    
    return db_entry