from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from .models import DiaryEntry
from .schemas import DiaryEntryCreate, DiaryEntryUpdate


def get_diary_entry(db: Session, entry_id: int) -> DiaryEntry | None:
    """Get a single diary entry by ID"""
    stmt = select(DiaryEntry).where(DiaryEntry.id == entry_id)

    return db.execute(stmt).scalars().one_or_none()


def get_diary_entries(db: Session, skip: int = 0, limit: int = 100) -> list[DiaryEntry]:
    """Get multiple diary entries with pagination"""
    stmt = select(DiaryEntry).offset(skip).limit(limit)

    return list(db.execute(stmt).scalars().all())


def create_diary_entry(db: Session, entry: DiaryEntryCreate) -> DiaryEntry:
    """Create a new diary entry"""
    db_entry = DiaryEntry(
        title=entry.title,
        content=entry.content
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    return db_entry


def update_diary_entry(db: Session, entry_id: int, entry: DiaryEntryUpdate) -> DiaryEntry | None:
    """Update and existing diary entry"""
    db_entry = get_diary_entry(db, entry_id)
    if db_entry is None:
        return None

    update_data = entry.model_dump(exclude_unset=True)
    if update_data:
        for key, value in update_data.items():
            setattr(db_entry, key, value)
            db.commit()
            db.refresh(db_entry)

    return db_entry


def delete_diary_entry(db: Session, entry_id: int) -> bool:
    """Delete a diary entry"""
    stmt = delete(DiaryEntry).where(DiaryEntry.id == entry_id)
    result = db.execute(stmt)
    db.commit()

    return result.rowcount > 0


def mark_diary_entry_done(db: Session, entry_id: int, is_done: bool = True) -> DiaryEntry | None:
    """Mark a diary entry as done/not done"""
    stmt = update(DiaryEntry).where(DiaryEntry.id == entry_id).values(is_done=is_done)
    result = db.execute(stmt)
    db.commit()

    if result.rowcount > 0:
        return get_diary_entry(db, entry_id)
    
    return None