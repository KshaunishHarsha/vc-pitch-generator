"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from config import settings


class PitchRequest(BaseModel):
    """Request model for generating a pitch"""
    idea: str = Field(
        ...,
        min_length=settings.MIN_IDEA_LENGTH,
        max_length=settings.MAX_IDEA_LENGTH,
        description="The startup idea to pitch"
    )

    @validator("idea")
    def validate_idea(cls, v):
        """Validate idea input"""
        if not v or not v.strip():
            raise ValueError("Idea cannot be empty or whitespace")
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "idea": "food delivery app for college students"
            }
        }


class PitchSection(BaseModel):
    """Individual pitch section"""
    id: int = Field(..., description="Section number (1-11)")
    emoji: str = Field(..., description="Emoji for the section")
    title: str = Field(..., description="Section title")
    content: str = Field(..., description="Section content")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "emoji": "🚀",
                "title": "STARTUP NAME + TAGLINE",
                "content": "QuickBite AI\n\"Redefining hyperlocal food logistics for Gen Z\""
            }
        }


class GeneratePitchResponse(BaseModel):
    """Response model for pitch generation"""
    success: bool
    pitch: Optional[dict] = None
    error: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "pitch": {
                    "input_idea": "food delivery app for college students",
                    "sections": [
                        {
                            "id": 1,
                            "emoji": "🚀",
                            "title": "STARTUP NAME + TAGLINE",
                            "content": "QuickBite AI\n\"Redefining hyperlocal food logistics for Gen Z\""
                        },
                        {
                            "id": 2,
                            "emoji": "🎯",
                            "title": "PROBLEM STATEMENT",
                            "content": "In today's fast-paced world, college students face an acute pain point..."
                        }
                    ]
                },
                "error": None
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
    details: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Idea must be between 10 and 200 characters",
                "details": "Provided idea: 'hi' (length: 2)"
            }
        }