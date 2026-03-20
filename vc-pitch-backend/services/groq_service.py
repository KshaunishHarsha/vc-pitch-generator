"""
Groq API Service for generating VC pitches
Located in: services/groq_service.py
"""

import logging
import sys
from pathlib import Path
from typing import List, Dict
from groq import Groq

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import settings

logger = logging.getLogger(__name__)


class GroqPitchGenerator:
    """Service for generating pitches using Groq API"""
    
    def __init__(self):
        """Initialize Groq client"""
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        logger.info(f"Groq service initialized with model: {self.model}")
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for Groq"""
        return """You are a startup founder pitching to top-tier VCs.

Your job is to take ANY simple/stupid idea and transform it into a highly overhyped, 
buzzword-heavy startup pitch that sounds impressive, exaggerated, and full of tech jargon.

Tone: Confident, persuasive, slightly over-the-top, using Silicon Valley buzzwords liberally.

You MUST output EXACTLY 11 sections in the specified format.
Each section MUST start with ---SECTION [NUMBER]---"""
    
    def _build_user_prompt(self, idea: str) -> str:
        """Build the user prompt for Groq"""
        return f"""Transform this startup idea into a VC pitch with exactly 11 sections:

IDEA: "{idea}"

Output each section with this EXACT format:
---SECTION 1---
[Content]
---SECTION 2---
[Content]
... continue for all 11 sections (---SECTION 3---, ---SECTION 4---, etc.)

SECTION STRUCTURE (generate all 11 sections in order):

1. 🚀 STARTUP NAME + TAGLINE
   - Generate a cool, slightly pretentious name
   - Add a 1-line tagline that sounds innovative
   - Example: QuickBite AI - "Redefining hyperlocal food logistics for Gen Z"

2. 🎯 PROBLEM STATEMENT
   - Make it sound dramatic and global
   - Start with "In today's fast-paced world..."
   - Highlight inefficiency, pain points, massive market scale
   - Make it sound like a billion-dollar problem

3. 💡 SOLUTION
   - Turn the simple idea into: "AI-powered, scalable, intelligent platform"
   - Include: automation, personalization, optimization
   - Make mundane sound revolutionary

4. 🧠 THE TECH (BE MAXIMALLY ABSURD BUT SOUND IMPRESSIVE)
   - Include: AI, multi-agent systems, real-time processing
   - Optional: blockchain, quantum computing, neural networks
   - Make it unhinged but sound like genius
   - Buzzwords: "synergize", "leverage", "paradigm shift", "decentralized"
   - This section should be the funniest

5. 📈 MARKET OPPORTUNITY
   - Cite "$XX billion TAM" with specific but vague numbers
   - Example: "$47.3B market" or "$12.8B TAM"
   - "Rapidly growing sector"
   - "Severely underserved audience"
   - "Expanding at 45% YoY"

6. 💰 BUSINESS MODEL
   - Subscriptions, commissions, SaaS, freemium conversion
   - Multiple revenue streams
   - "Marketplace dynamics", "network effects", "unit economics"

7. 🧲 TRACTION
   - "Early user interest and validation"
   - "Pilot testing underway"
   - "Strong engagement signals"
   - Mention: waitlists, viral metrics, beta users, influencer partnerships
   - "1.2M waitlist", "2.3x retention rate"

8. 🆚 COMPETITIVE ADVANTAGE
   - "First-mover advantage"
   - "Proprietary technology / algorithms"
   - "Network effects"
   - "Switching costs"
   - Vague but impressive language

9. 🛣️ ROADMAP
   - Phase 1: MVP launch (3 months)
   - Phase 2: Scale to new markets (6 months)
   - Phase 3: "Global domination" or "IPO trajectory" energy
   - Include "strategic partnerships" and "international expansion"

10. 💸 THE ASK
    - "We're raising $X million to..."
    - Mention: hiring world-class talent, aggressive growth, market expansion
    - "To scale from 10K to 10M users"
    - Use numbers like "$5M seed", "$15M Series A"

11. 💀 REALITY CHECK (THE VIRAL HOOK - COMPLETELY DIFFERENT TONE)
    - Write a SINGLE brutally honest line
    - Complete tonal break from previous sections
    - Drop the startup speak entirely
    - Format: "What it actually is: [the real, mundane thing]"
    - Examples: 
      - "What it actually is: just a group chat with Uber Eats links"
      - "What it actually is: a spreadsheet that texts you"
      - "What it actually is: your friend with a good contact list"
      - "What it actually is: literally a reminder app"
    - THIS IS THE VIRAL MOMENT - make it funny and unexpected

IMPORTANT INSTRUCTIONS:
- Keep each section concise but impressive (2-4 sentences for sections 1-3, 3-5 for others)
- Use Silicon Valley buzzwords liberally and unironically
- Make the Reality Check SHOCKING compared to the hype - that's the humor
- Don't repeat the emoji in the content itself
- Section 4 (THE TECH) should be maximum absurdity
- Sections 1-10 should sound like a real pitch deck
- Section 11 should be the mic drop moment
- All 11 sections are required"""
    
    async def generate_pitch(self, idea: str) -> List[Dict]:
        """Generate a pitch for the given idea using Groq API"""
        try:
            logger.info(f"Generating pitch for idea: {idea[:50]}...")
            
            user_prompt = self._build_user_prompt(idea)
            
            # Call Groq API (use chat.completions, not messages)
            message = self.client.chat.completions.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
            )
            
            # Extract response text (use choices[0].message.content, not content[0].text)
            response_text = message.choices[0].message.content
            logger.debug(f"Groq response received (length: {len(response_text)})")
            
            # Parse the response
            sections = self._parse_response(response_text)
            logger.info(f"Successfully parsed {len(sections)} sections")
            
            if len(sections) != 11:
                logger.warning(f"Expected 11 sections, got {len(sections)}")
            
            return sections
            
        except Exception as e:
            logger.error(f"Error generating pitch: {str(e)}", exc_info=True)
            raise
    
    def _parse_response(self, response_text: str) -> List[Dict]:
        """Parse Groq response into structured sections"""
        try:
            # Split by section markers
            sections = response_text.split("---SECTION")
            
            # Expected titles for each section (fallback if parsing fails)
            expected_titles = [
                "STARTUP NAME + TAGLINE",
                "PROBLEM STATEMENT",
                "SOLUTION",
                "THE TECH",
                "MARKET OPPORTUNITY",
                "BUSINESS MODEL",
                "TRACTION",
                "COMPETITIVE ADVANTAGE",
                "ROADMAP",
                "THE ASK",
                "REALITY CHECK"
            ]
            
            # Emoji mapping for each section
            emojis = ["🚀", "🎯", "💡", "🧠", "📈", "💰", "🧲", "🆚", "🛣️", "💸", "💀"]
            
            parsed_sections = []
            
            # Skip first element (before first ---SECTION) and process remaining
            for idx, section in enumerate(sections[1:12], start=1):
                if idx > 11:  # Only parse 11 sections
                    break
                
                lines = section.split("\n")
                
                # Extract header (contains number and any title)
                header = lines[0] if lines else ""
                
                # Extract content (everything after header)
                content_lines = lines[1:]
                content = "\n".join(content_lines).strip()
                
                if not content:  # Skip empty sections
                    logger.warning(f"Empty content for section {idx}")
                    continue
                
                section_dict = {
                    "id": idx,
                    "emoji": emojis[idx - 1] if idx <= len(emojis) else "📌",
                    "title": expected_titles[idx - 1] if idx <= len(expected_titles) else f"SECTION {idx}",
                    "content": content
                }
                
                parsed_sections.append(section_dict)
            
            # Ensure we have all 11 sections
            if len(parsed_sections) < 11:
                logger.warning(f"Only got {len(parsed_sections)} sections, expected 11")
                # Pad with placeholder sections if needed
                while len(parsed_sections) < 11:
                    idx = len(parsed_sections) + 1
                    parsed_sections.append({
                        "id": idx,
                        "emoji": emojis[idx - 1] if idx <= len(emojis) else "📌",
                        "title": expected_titles[idx - 1] if idx <= len(expected_titles) else f"SECTION {idx}",
                        "content": "[Content not generated]"
                    })
            
            return parsed_sections[:11]  # Return only first 11
            
        except Exception as e:
            logger.error(f"Error parsing response: {str(e)}")
            raise ValueError(f"Failed to parse pitch response: {str(e)}")


# Initialize the service
groq_service = GroqPitchGenerator()