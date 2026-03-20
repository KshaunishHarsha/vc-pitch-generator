"""
API routes for pitch generation
Located in: routes/pitch.py
"""

import logging
import sys
from pathlib import Path
from fastapi import APIRouter, HTTPException

# Add parent directory to path to import models and services
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import PitchRequest, GeneratePitchResponse, ErrorResponse
from services.groq_service import groq_service
from utils.validators import validate_idea

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["pitch"])


# Example startup ideas
EXAMPLE_IDEAS = [
    "Food delivery app for college students",
    "Uber for dog walking",
    "LinkedIn for plants",
    "Blockchain-based note-taking app",
    "AI alarm clock that judges your sleep schedule",
    "Dating app for leftover pizza slices",
    "NFT-based email service",
    "Web3 social network for houseplants",
    "AI-powered sock matching service",
    "Metaverse gym for lazy people",
    "ChatGPT but for grocery lists",
    "Tinder but for finding roommates",
    "Duolingo but for learning to code",
    "Discord but for plants",
    "Airbnb but for pet sitting",
]


@router.post(
    "/generate-pitch",
    response_model=GeneratePitchResponse,
    responses={
        400: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def generate_pitch(request: PitchRequest) -> GeneratePitchResponse:
    """
    Generate a VC pitch from a startup idea
    
    Takes a simple startup idea and transforms it into a full buzzword-heavy VC pitch.
    Returns 11 sections including the brutal reality check.
    
    **Request Body:**
    - `idea`: str (10-200 characters) - Your startup idea
    
    **Response:**
    - `success`: bool - Whether generation was successful
    - `pitch`: dict - Generated pitch with sections
    - `error`: str - Error message if failed
    
    **Example Request:**
    ```json
    {
        "idea": "food delivery app for college students"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "success": true,
        "pitch": {
            "input_idea": "food delivery app for college students",
            "sections": [
                {
                    "id": 1,
                    "emoji": "🚀",
                    "title": "STARTUP NAME + TAGLINE",
                    "content": "QuickBite AI..."
                },
                ...
            ]
        },
        "error": null
    }
    ```
    """
    
    try:
        # Validate input
        is_valid, error_message = validate_idea(request.idea)
        if not is_valid:
            logger.warning(f"Invalid idea input: {error_message}")
            raise HTTPException(
                status_code=400,
                detail=error_message
            )
        
        # Generate pitch using Groq
        logger.info(f"Generating pitch for: {request.idea}")
        sections = await groq_service.generate_pitch(request.idea)
        
        if not sections or len(sections) == 0:
            logger.error("No sections returned from Groq")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate pitch sections"
            )
        
        # Return success response
        logger.info(f"Successfully generated pitch with {len(sections)} sections")
        return GeneratePitchResponse(
            success=True,
            pitch={
                "input_idea": request.idea,
                "sections": sections
            }
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error generating pitch: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate pitch. Please try again later."
        )


@router.get("/examples")
async def get_examples():
    """
    Get example startup ideas
    
    Returns a list of example startup ideas that users can click to try.
    
    **Response:**
    ```json
    {
        "success": true,
        "examples": [
            "Food delivery app for college students",
            "Uber for dog walking",
            ...
        ]
    }
    ```
    """
    logger.info("Fetching example ideas")
    return {
        "success": True,
        "examples": EXAMPLE_IDEAS
    }