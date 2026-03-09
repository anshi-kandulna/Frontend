# # models/forms.py
# from dataclasses import dataclass
# from typing import List, Optional

# @dataclass
# class SymptomData:
#     symptom_name: str
#     severity: int  # 1-10
#     duration_days: int

# @dataclass
# class DietData:
#     food_type: str
#     frequency: str
#     digestive_issues: str

# @dataclass
# class StoolData:
#     color: str
#     consistency: str
#     frequency: int

# @dataclass
# class AlarmData:
#     alarm_type: str
#     severity: str
#     description: str

# @dataclass
# class DiagnosisResponse:
#     diagnosis: str
#     recommendations: List[str]
#     severity: str