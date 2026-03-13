# routes/__init__.py
from .symptom_routes import symptom_router
from .stool_routes import stool_router

__all__ = ['symptom_router', 'stool_router']
