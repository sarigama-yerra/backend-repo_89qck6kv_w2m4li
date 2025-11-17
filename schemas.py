"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

# Core HR models

class Employee(BaseModel):
    """Employees collection schema"""
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    email: str = Field(..., description="Work email address")
    phone: Optional[str] = Field(None, description="Phone number")
    position: Optional[str] = Field(None, description="Job title/position")
    department: Optional[str] = Field(None, description="Department name")
    start_date: Optional[date] = Field(None, description="Start date")
    employment_type: Optional[str] = Field(
        "full-time", description="Employment type: full-time, part-time, contract"
    )
    manager_id: Optional[str] = Field(None, description="Manager employee ID (string)")
    location: Optional[str] = Field(None, description="Office or remote location")
    is_active: bool = Field(True, description="Active employment status")

class Job(BaseModel):
    """Jobs collection schema"""
    title: str = Field(..., description="Job title")
    department: Optional[str] = Field(None, description="Department")
    description: Optional[str] = Field(None, description="Job description")
    location: Optional[str] = Field(None, description="Location")
    employment_type: Optional[str] = Field("full-time", description="Employment type")
    salary_min: Optional[float] = Field(None, ge=0, description="Minimum salary")
    salary_max: Optional[float] = Field(None, ge=0, description="Maximum salary")
    skills: Optional[List[str]] = Field(default_factory=list, description="Key skills")
    is_open: bool = Field(True, description="Whether the job is open")

class Applicant(BaseModel):
    """Applicants collection schema"""
    name: str = Field(..., description="Applicant name")
    email: str = Field(..., description="Applicant email")
    phone: Optional[str] = Field(None, description="Applicant phone")
    job_id: Optional[str] = Field(None, description="Applied job ID (string)")
    resume_url: Optional[str] = Field(None, description="Link to resume/CV")
    cover_letter: Optional[str] = Field(None, description="Cover letter text")
    status: str = Field("applied", description="Application status")

class LeaveRequest(BaseModel):
    """Leave requests collection schema"""
    employee_id: str = Field(..., description="Employee ID (string)")
    leave_type: str = Field(..., description="Type of leave: vacation, sick, etc.")
    start_date: date = Field(..., description="Start date")
    end_date: date = Field(..., description="End date")
    reason: Optional[str] = Field(None, description="Reason for leave")
    status: str = Field("pending", description="Approval status")

class Attendance(BaseModel):
    """Attendance collection schema"""
    employee_id: str = Field(..., description="Employee ID (string)")
    date: date = Field(..., description="Attendance date")
    check_in: Optional[str] = Field(None, description="Check-in time (HH:MM)")
    check_out: Optional[str] = Field(None, description="Check-out time (HH:MM)")
    notes: Optional[str] = Field(None, description="Notes")

class Payroll(BaseModel):
    """Payroll collection schema"""
    employee_id: str = Field(..., description="Employee ID (string)")
    period_start: date = Field(..., description="Payroll period start date")
    period_end: date = Field(..., description="Payroll period end date")
    base_pay: float = Field(..., ge=0, description="Base pay amount")
    bonus: float = Field(0, ge=0, description="Bonus amount")
    deductions: float = Field(0, ge=0, description="Deductions amount")
    net_pay: Optional[float] = Field(None, ge=0, description="Net pay (calculated if not provided)")

class PerformanceReview(BaseModel):
    """Performance reviews collection schema"""
    employee_id: str = Field(..., description="Employee ID (string)")
    reviewer_id: Optional[str] = Field(None, description="Reviewer employee ID")
    review_date: date = Field(..., description="Date of review")
    rating: int = Field(..., ge=1, le=5, description="Overall rating 1-5")
    strengths: Optional[List[str]] = Field(default_factory=list, description="Strengths")
    improvements: Optional[List[str]] = Field(default_factory=list, description="Areas for improvement")
    comments: Optional[str] = Field(None, description="Additional comments")

class Announcement(BaseModel):
    """Announcements collection schema"""
    title: str = Field(..., description="Announcement title")
    body: str = Field(..., description="Announcement content")
    audience: Optional[str] = Field("all", description="Target audience")
    priority: Optional[str] = Field("normal", description="Priority: low, normal, high")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
