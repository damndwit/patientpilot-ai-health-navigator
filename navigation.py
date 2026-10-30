"""Care navigation using external search links (no booking / no patient data transfer)."""
from __future__ import annotations
from urllib.parse import urlencode

MAPS = "https://www.google.com/maps/search/?"
DIRECTIONS = "https://www.google.com/maps/dir/?"
MAX_LOCATION = 100

def _safe_location(value: str) -> str:
    text = " ".join((value or "").strip().split())
    if not 2 <= len(text) <= MAX_LOCATION:
        raise ValueError("Enter a valid city, ZIP code, or destination (2–100 characters).")
    if any(x in text for x in ("\n", "\r", "<", ">", "\x00")):
        raise ValueError("Enter a normal city, ZIP code, or destination.")
    return text

def hospital_search_url(location: str) -> str:
    return MAPS + urlencode({"api": "1", "query": f"hospitals near {_safe_location(location)}"})

def directions_url(origin: str, destination: str) -> str:
    return DIRECTIONS + urlencode({
        "api": "1", "origin": _safe_location(origin),
        "destination": _safe_location(destination),
        "travelmode": "driving",
    })

def clinic_destination() -> str:
    # The fictional clinic has no actual address; never invent one.
    return "Cedar Grove Family Clinic is fictional and has no real-world address."
