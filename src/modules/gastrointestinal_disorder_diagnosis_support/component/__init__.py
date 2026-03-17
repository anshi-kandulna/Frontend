# components/__init__.py

from .gi_dashboard import gi_dashboard
from .forms.symptom_form import symptom_form
from .forms.stool_form import stool_form
from .forms.diet_form import diet_form
from .forms.alarm_form import alarm_form

__all__ = [
    "gi_dashboard",
    "symptom_form",
    "stool_form",
    "diet_form",
    "alarm_form",
]
