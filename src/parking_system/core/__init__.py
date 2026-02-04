"""
parking_system package root

Exposes high-level submodules only.
Deep modules (security, analytics, etc.) are imported explicitly where needed.
"""

__all__ = [
    "core",
    "database",
    "analytics",
    "io_integration",
    "security",
    "notifications",
    "payment",
]
