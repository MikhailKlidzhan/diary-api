import pytest
from fastapi.testclient import TestClient

from src.diary_api.main import app
from src.diary_api.database import Base, get_db
from src.diary_api.test_config import engine as test_engine, TestingSessionLocal, create_test_database

# Create tables before running tests
create_test_database()

@pytest.fixture
def test_db():
    """Create a new database session for each test"""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    Base.metadata.create_all(bind=test_engine)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(test_db):
    """Create a test client that uses the test database"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_create_entry(client):
    """Test creating an entry through the API"""
    response = client.post(
        "/entries/",
        json={"title": "Test Entry", "content": "Test Content"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Entry"
    assert data["content"] == "Test Content"
    assert data["is_done"] is False
    assert "id" in data

def test_read_entry(client, test_db):
    """Test reading an entry through the API"""
    # First create an entry directly in the database
    from src.diary_api import crud, schemas
    entry_create = schemas.DiaryEntryCreate(title="Test Entry", content="Test Content")
    entry = crud.create_diary_entry(test_db, entry_create)
    
    # Now read it through the API
    response = client.get(f"/entries/{entry.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Entry"
    assert data["id"] == entry.id

def test_read_entries(client, test_db):
    """Test reading multiple entries through the API"""
    # Create some entries directly
    from src.diary_api import crud, schemas
    for i in range(3):
        entry_create = schemas.DiaryEntryCreate(
            title=f"Test Entry {i}", 
            content=f"Content {i}"
        )
        crud.create_diary_entry(test_db, entry_create)
    
    # Get all entries
    response = client.get("/entries/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["title"] == "Test Entry 0"
    assert data[1]["title"] == "Test Entry 1"

def test_update_entry(client, test_db):
    """Test updating an entry through the API"""
    # First create an entry
    from src.diary_api import crud, schemas
    entry_create = schemas.DiaryEntryCreate(title="Original", content="Original")
    entry = crud.create_diary_entry(test_db, entry_create)
    
    # Update it
    response = client.patch(
        f"/entries/{entry.id}",
        json={"title": "Updated", "is_done": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["is_done"] is True
    assert data["content"] == "Original"  # Should remain unchanged

def test_delete_entry(client, test_db):
    """Test deleting an entry through the API"""
    # First create an entry
    from src.diary_api import crud, schemas
    entry_create = schemas.DiaryEntryCreate(title="To Delete", content="Content")
    entry = crud.create_diary_entry(test_db, entry_create)
    
    # Delete it
    response = client.delete(f"/entries/{entry.id}")
    assert response.status_code == 204
    
    # Verify it's really deleted
    response = client.get(f"/entries/{entry.id}")
    assert response.status_code == 404

def test_read_nonexistent_entry(client):
    """Test reading a non-existent entry"""
    response = client.get("/entries/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Diary entry not found"}

def test_update_nonexistent_entry(client):
    """Test updating a non-existent entry"""
    response = client.patch(
        "/entries/99999",
        json={"title": "New Title"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Diary entry not found"}

def test_delete_nonexistent_entry(client):
    """Test deleting a non-existent entry"""
    response = client.delete("/entries/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Diary entry not found"}