# # services/api_service.py
# import requests
# from typing import Dict

# class APIService:
#     BASE_URL = "http://localhost:5000/api"
    
#     @staticmethod
#     def submit_symptom(patient_id: str, data: Dict) -> Dict:
#         """Send symptom data to backend"""
#         response = requests.post(
#             f"{APIService.BASE_URL}/symptoms",
#             json={"patient_id": patient_id, **data}
#         )
#         return response.json()
    
#     @staticmethod
#     def submit_diet(patient_id: str, data: Dict) -> Dict:
#         """Send diet data to backend"""
#         response = requests.post(
#             f"{APIService.BASE_URL}/diet",
#             json={"patient_id": patient_id, **data}
#         )
#         return response.json()
    
#     @staticmethod
#     def get_diagnosis(patient_id: str) -> Dict:
#         """Get diagnosis from backend"""
#         response = requests.get(
#             f"{APIService.BASE_URL}/diagnosis/{patient_id}"
#         )
#         return response.json()