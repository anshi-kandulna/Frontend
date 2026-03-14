# routes/__init__.py
from .symptom_routes import symptom_router
from .stool_routes import stool_router
from .diet_routes import diet_router
from .alarm_routes import alarm_router

__all__ = ['symptom_router', 'stool_router', 'diet_router', 'alarm_router']
