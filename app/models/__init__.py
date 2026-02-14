from sqlalchemy import Column, Integer, String, JSON, DateTime, Float, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_session_id = Column(String, unique=True, index=True)
    
    # Personal Info
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    date_of_birth = Column(DateTime, nullable=True)
    location = Column(String)
    
    # Professional Info
    education = Column(JSON, default=list)  # List of education entries
    work_experience = Column(JSON, default=list)  # List of work experiences
    total_experience = Column(Float, default=0)  # Total years of experience
    
    # Compensation
    current_ctc = Column(Float, nullable=True)
    in_hand_salary = Column(Float, nullable=True)
    expected_ctc = Column(Float, nullable=True)
    notice_period = Column(Integer, nullable=True)  # in days
    
    # Career Stability
    reason_for_leaving = Column(Text, nullable=True)
    job_switches = Column(Integer, default=0)
    career_gap = Column(Boolean, default=False)
    career_gap_details = Column(Text, nullable=True)
    
    # Skills
    skills = Column(JSON, default=list)  # List of skills
    
    # Assessment
    typing_speed = Column(Integer, default=0)  # WPM
    typing_accuracy = Column(Float, default=0)  # Percentage
    resume_path = Column(String, nullable=True)
    
    # AI Analysis
    communication_score = Column(Float, default=0)
    ai_observations = Column(Text, nullable=True)
    
    # Status
    status = Column(String, default="new")  # new, in_progress, completed, shortlisted, rejected, hired
    current_role_applied = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    interview_sessions = relationship("InterviewSession", back_populates="candidate")
    scores = relationship("CandidateScore", back_populates="candidate")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    role_id = Column(String, index=True)
    current_step = Column(String, default="greeting")
    conversation_history = Column(JSON, default=list)
    responses = Column(JSON, default=dict)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="interview_sessions")


class CandidateScore(Base):
    __tablename__ = "candidate_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    role_id = Column(String, index=True)
    
    # Score components (out of 100)
    experience_score = Column(Float, default=0)  # 25% weight
    skills_score = Column(Float, default=0)      # 25% weight
    stability_score = Column(Float, default=0)   # 15% weight
    communication_score = Column(Float, default=0) # 15% weight
    typing_score = Column(Float, default=0)      # 10% weight
    role_fit_score = Column(Float, default=0)    # 10% weight
    
    total_score = Column(Float, default=0)       # Weighted sum
    rank = Column(Integer, nullable=True)
    is_shortlisted = Column(Boolean, default=False)
    manual_override = Column(JSON, nullable=True)  # Store manual overrides
    override_reason = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="scores")


class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(String, unique=True, index=True)  # e.g., "software_engineer"
    role_name = Column(String)  # e.g., "Software Engineer"
    description = Column(Text)
    required_skills = Column(JSON, default=list)
    preferred_skills = Column(JSON, default=list)
    min_experience = Column(Integer, default=0)
    max_experience = Column(Integer, default=20)
    education_requirements = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class InterviewSchedule(Base):
    __tablename__ = "interview_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    role_id = Column(String)
    scheduled_date = Column(DateTime)
    interview_type = Column(String)  # technical, hr, managerial
    interviewer_email = Column(String)
    meeting_link = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, confirmed, completed, cancelled, rescheduled
    calendar_event_id = Column(String, nullable=True)
    reschedule_count = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

