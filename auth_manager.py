"""
=============================================================================
AI NEWS DETECTIVE - AUTHENTICATION & USER MANAGEMENT ENGINE
=============================================================================
Provides secure authentication, session management, and role-based access
for forensic investigators, intelligence analysts, and guest researchers.
"""

import hashlib
import json
import os
import time
from typing import Dict, Any, Optional

AUTH_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users_db.json")


class AuthManager:
    """Handles user registration, authentication, password hashing, and profiles."""

    def __init__(self):
        self._ensure_db()

    def _hash_password(self, password: str) -> str:
        """Hash passwords with SHA-256 for secure local storage."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def _ensure_db(self):
        """Initialize database with pre-configured demo analyst accounts if not present."""
        if not os.path.exists(AUTH_FILE):
            default_users = {
                "analyst@detective.ai": {
                    "email": "analyst@detective.ai",
                    "name": "Dr. Sarah Chen",
                    "role": "Senior Forensic Investigator",
                    "password_hash": self._hash_password("detective2026"),
                    "created_at": "2026-08-20",
                    "avatar": "🛡️",
                    "investigations_count": 42,
                    "clearance_level": "Tier-3 Intelligence Clearance"
                },
                "journalist@truth.org": {
                    "email": "journalist@truth.org",
                    "name": "Marcus Vance",
                    "role": "Investigative Journalist",
                    "password_hash": self._hash_password("press123"),
                    "created_at": "2026-08-21",
                    "avatar": "📰",
                    "investigations_count": 19,
                    "clearance_level": "Press Accreditation"
                }
            }
            with open(AUTH_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_users, f, indent=2)

    def _load_users(self) -> Dict[str, Any]:
        try:
            with open(AUTH_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_users(self, users: Dict[str, Any]):
        with open(AUTH_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2)

    def authenticate(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Verify user credentials."""
        users = self._load_users()
        email_clean = email.strip().lower()
        if email_clean in users:
            user = users[email_clean]
            if user.get("password_hash") == self._hash_password(password):
                # Return profile without sensitive hash
                profile = user.copy()
                profile.pop("password_hash", None)
                return profile
        return None

    def register(self, email: str, name: str, password: str, role: str = "Forensic Analyst") -> Dict[str, Any]:
        """Register a new user account."""
        users = self._load_users()
        email_clean = email.strip().lower()

        if not email_clean or "@" not in email_clean:
            return {"success": False, "message": "Please provide a valid email address."}
        if len(password) < 4:
            return {"success": False, "message": "Password must be at least 4 characters long."}
        if email_clean in users:
            return {"success": False, "message": "An account with this email already exists."}

        new_user = {
            "email": email_clean,
            "name": name.strip() if name.strip() else "Investigator",
            "role": role,
            "password_hash": self._hash_password(password),
            "created_at": time.strftime("%Y-%m-%d"),
            "avatar": "🔍",
            "investigations_count": 1,
            "clearance_level": "Standard Investigator Access"
        }
        users[email_clean] = new_user
        self._save_users(users)

        profile = new_user.copy()
        profile.pop("password_hash", None)
        return {"success": True, "user": profile, "message": "Account created successfully!"}

    def increment_investigations(self, email: str):
        """Update investigations counter for active user."""
        users = self._load_users()
        email_clean = email.strip().lower()
        if email_clean in users:
            users[email_clean]["investigations_count"] = users[email_clean].get("investigations_count", 0) + 1
            self._save_users(users)


_auth_manager = AuthManager()

def authenticate_user(email: str, password: str):
    return _auth_manager.authenticate(email, password)

def register_user(email: str, name: str, password: str, role: str = "Forensic Analyst"):
    return _auth_manager.register(email, name, password, role)
