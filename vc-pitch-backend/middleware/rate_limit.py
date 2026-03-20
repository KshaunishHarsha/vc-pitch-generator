"""
Rate limiting middleware
Located in: middleware/rate_limit.py
"""

import logging
import sys
from pathlib import Path
from fastapi import Request, HTTPException
from collections import defaultdict
from datetime import datetime, timedelta

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import settings

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = defaultdict(list)  # IP -> list of timestamps
    
    def is_allowed(self, client_ip: str) -> bool:
        """Check if client is within rate limits"""
        if not settings.RATE_LIMIT_ENABLED:
            return True
        
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        one_hour_ago = now - timedelta(hours=1)
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > one_hour_ago
        ]
        
        # Check per-minute limit
        recent_requests = [
            req_time for req_time in self.requests[client_ip]
            if req_time > one_minute_ago
        ]
        
        if len(recent_requests) >= settings.REQUESTS_PER_MINUTE:
            logger.warning(f"Rate limit (per minute) exceeded for IP: {client_ip}")
            return False
        
        # Check per-hour limit
        if len(self.requests[client_ip]) >= settings.REQUESTS_PER_HOUR:
            logger.warning(f"Rate limit (per hour) exceeded for IP: {client_ip}")
            return False
        
        # Add current request
        self.requests[client_ip].append(now)
        return True
    
    def get_reset_time(self, client_ip: str) -> int:
        """Get seconds until rate limit resets"""
        if not self.requests[client_ip]:
            return 0
        
        oldest_request = min(self.requests[client_ip])
        reset_time = oldest_request + timedelta(minutes=1)
        seconds_until_reset = max(0, (reset_time - datetime.now()).total_seconds())
        
        return int(seconds_until_reset)


# Global rate limiter instance
rate_limiter = RateLimiter()


async def rate_limit_middleware(request: Request, call_next):
    """Middleware to apply rate limiting"""
    
    # Get client IP
    client_ip = request.client.host if request.client else "unknown"
    
    # Check rate limit for POST requests to /api/generate-pitch
    if request.method == "POST" and "/api/generate-pitch" in request.url.path:
        if not rate_limiter.is_allowed(client_ip):
            reset_time = rate_limiter.get_reset_time(client_ip)
            logger.warning(f"Rate limit exceeded for {client_ip}. Reset in {reset_time}s")
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Try again in {reset_time} seconds.",
                headers={"Retry-After": str(reset_time)}
            )
    
    response = await call_next(request)
    return response