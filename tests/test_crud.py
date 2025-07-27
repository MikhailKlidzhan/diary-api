import pytest
from sqlalchemy.orm import Session
from src.diary_api import crud, schemas
from src.diary_api.test_config import engine, TestingSessionLocal, create_test_database

# Create tables before running tests
create_test_database()

@pytest.fixture
def db_session():
    """Create a new database session for each test"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

def test_create_diary_entry(db_session: Session):
    """Test creating a diary entry"""
    entry_create = schemas.DiaryEntryCreate(
        title="Test Entry",
        content="This is a test entry"
    )
    
    entry = crud.create_diary_entry(db_session, entry_create)
    
    assert entry.title == "Test Entry"
    assert entry.content == "This is a test entry"
    assert entry.is_done == False
    assert entry.id is not None

def test_get_diary_entry(db_session: Session):
    """Test getting a diary entry by ID"""
    # First create an entry
    entry_create = schemas.DiaryEntryCreate(
        title="Test Entry",
        content="This is a test entry"
    )
    created_entry = crud.create_diary_entry(db_session, entry_create)
    
    # Then retrieve it
    retrieved_entry = crud.get_diary_entry(db_session, created_entry.id)
    
    assert retrieved_entry is not None
    assert retrieved_entry.id == created_entry.id
    assert retrieved_entry.title == "Test Entry"

def test_get_diary_entries(db_session: Session):
    """Test getting multiple diary entries"""
    # Create multiple entries
    for i in range(3):
        entry_create = schemas.DiaryEntryCreate(
            title=f"Test Entry {i}",
            content=f"Content {i}"
        )
        crud.create_diary_entry(db_session, entry_create)
    
    # Get all entries
    entries = crud.get_diary_entries(db_session)
    
    assert len(entries) == 3

def test_update_diary_entry(db_session: Session):
    """Test updating a diary entry"""
    # Create an entry
    entry_create = schemas.DiaryEntryCreate(
        title="Original Title",
        content="Original Content"
    )
    created_entry = crud.create_diary_entry(db_session, entry_create)
    
    # Update it
    entry_update = schemas.DiaryEntryUpdate(
        title="Updated Title",
        is_done=True
    )
    updated_entry = crud.update_diary_entry(db_session, created_entry.id, entry_update)
    
    assert updated_entry is not None
    assert updated_entry.title == "Updated Title"
    assert updated_entry.content == "Original Content"  # Should remain unchanged
    assert updated_entry.is_done == True

def test_delete_diary_entry(db_session: Session):
    """Test deleting a diary entry"""
    # Create an entry
    entry_create = schemas.DiaryEntryCreate(
        title="Test Entry",
        content="Test Content"
    )
    created_entry = crud.create_diary_entry(db_session, entry_create)
    
    # Delete it
    success = crud.delete_diary_entry(db_session, created_entry.id)
    
    assert success == True
    
    # Verify it's deleted
    deleted_entry = crud.get_diary_entry(db_session, created_entry.id)
    assert deleted_entry is None

def test_mark_diary_entry_done(db_session: Session):
    """Test marking a diary entry as done"""
    # Create an entry
    entry_create = schemas.DiaryEntryCreate(
        title="Test Entry",
        content="Test Content"
    )
    created_entry = crud.create_diary_entry(db_session, entry_create)
    
    # Mark as done
    marked_entry = crud.mark_diary_entry_done(db_session, created_entry.id, True)
    
    assert marked_entry is not None
    assert marked_entry.is_done == True

def test_update_nonexistent_entry(db_session: Session):
    """Test updating a non-existent entry"""
    entry_update = schemas.DiaryEntryUpdate(title="New Title")
    result = crud.update_diary_entry(db_session, 99999, entry_update)
    
    assert result is None

def test_delete_nonexistent_entry(db_session: Session):
    """Test deleting a non-existent entry"""
    success = crud.delete_diary_entry(db_session, 99999)
    
    assert success == False