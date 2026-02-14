from app.models import Candidate, InterviewSession, CandidateScore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

print("Testing database models...")

# Create in-memory SQLite database for testing
engine = create_engine('sqlite:///:memory:')

# Create all tables
from app.models import Base
Base.metadata.create_all(bind=engine)

print("✓ Models loaded successfully!")
print("✓ Tables created successfully!")

Session = sessionmaker(bind=engine)
db = Session()

# Test creating a candidate
test_candidate = Candidate(
    first_name="Test",
    last_name="User",
    email="test@example.com",
    chat_session_id="test123"
)

db.add(test_candidate)
db.commit()

print("✓ Candidate created successfully!")
print(f"✓ Candidate ID: {test_candidate.id}")

db.close()
print("\nAll tests passed! ✅")
