import json
from pathlib import Path
from typing import Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_FILE = BASE_DIR / "app" / "knowledge" / "portfolio.json"

_cached_knowledge: Dict[str, Any] = {}
_cached_system_prompt: str = ""


def load_portfolio_knowledge() -> Dict[str, Any]:
    """Load and return the raw portfolio JSON data."""
    global _cached_knowledge
    if not _cached_knowledge:
        if KNOWLEDGE_FILE.exists():
            with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                _cached_knowledge = json.load(f)
    return _cached_knowledge


def build_system_prompt() -> str:
    """Build a system prompt incorporating portfolio knowledge context and rules."""
    global _cached_system_prompt
    if _cached_system_prompt:
        return _cached_system_prompt

    data = load_portfolio_knowledge()
    if not data:
        return "You are an AI assistant for Olugbenga Ojeniyi (ARLTECH)."

    profile = data.get("profile", {})
    services = data.get("services", [])
    skills = data.get("skills", {})
    education = data.get("education", [])
    certifications = data.get("certifications", [])
    projects = data.get("projects", [])
    experience = data.get("experience", [])
    testimonials = data.get("testimonials", [])
    contact = data.get("contact", {})
    social_links = data.get("social_links", {})
    availability = data.get("availability", {})
    cta = data.get("call_to_action", {})
    bot = data.get("chatbot", {})

    prompt_lines = [
        f"You are {bot.get('name', 'ARLTECH AI Assistant')}.",
        f"Purpose: {bot.get('purpose', 'Help visitors understand Olugbenga Ojeniyi portfolio.')}",
        f"Tone: {', '.join(bot.get('tone', ['professional', 'friendly']))}.",
        "",
        "RULES:",
    ]

    for rule in bot.get("rules", []):
        prompt_lines.append(f"- {rule}")

    prompt_lines.extend([
        "",
        "PORTFOLIO KNOWLEDGE BASE:",
        f"Name: {profile.get('name')}",
        f"Brand: {profile.get('brand')}",
        f"Title: {profile.get('title')}",
        f"Tagline: {profile.get('tagline')}",
        f"About: {profile.get('description')}",
        f"Stats: {profile.get('projects_delivered')} projects delivered, {profile.get('happy_clients')} happy clients, {profile.get('years_of_experience')} years experience.",
        "",
        "SERVICES:",
    ])

    for s in services:
        prompt_lines.append(f"- {s.get('title')}: {s.get('description')}")

    prompt_lines.extend([
        "",
        "SKILLS & TECHNOLOGIES:",
        f"- Frontend: {', '.join(skills.get('frontend', []))}",
        f"- Backend: {', '.join(skills.get('backend', []))}",
        f"- Tools: {', '.join(skills.get('tools', []))}",
        f"- CMS: {', '.join(skills.get('cms', []))}",
        "",
        "EDUCATION:",
    ])

    for ed in education:
        degree = ed.get("degree") or ed.get("program")
        prompt_lines.append(f"- {degree} in {ed.get('field')} at {ed.get('institution')} ({ed.get('year')})")

    prompt_lines.extend([
        "",
        "CERTIFICATIONS:",
        f"- {', '.join(certifications)}",
        "",
        "PROJECTS:",
        "No specific project details are currently available." if not projects else str(projects),
        "",
        "EXPERIENCE:",
        "No specific employment history records are currently available." if not experience else str(experience),
        "",
        "TESTIMONIALS:",
        "No client testimonials are currently available." if not testimonials else str(testimonials),
        "",
        "CONTACT & AVAILABILITY:",
        f"- Email: {contact.get('email')}",
        f"- WhatsApp: {contact.get('whatsapp')} ({social_links.get('whatsapp')})",
        f"- Location: {contact.get('location')}",
        f"- Availability: {availability.get('status')}",
        f"- Response Time: {contact.get('response_time')}",
        f"- Call to Action: {cta.get('message')}",
    ])

    _cached_system_prompt = "\n".join(prompt_lines)
    return _cached_system_prompt
