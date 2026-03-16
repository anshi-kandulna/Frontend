from collections import defaultdict
import argparse
import json

from ..database import db


class GIAnalysisService:

    def __init__(self, db):
        self.db = db

    def diet_symptom_correlation(self, patient_id: str):

        diet_records = list(
            self.db['patient_diet'].find({"patient_id": patient_id})
        )
        # Debug prints
        print(f"DEBUG: Found {len(diet_records)} diet records for patient_id='{patient_id}'")
        if not diet_records:
             # Try other types just in case
             print(f"DEBUG: Checking alternative types for patient_id...")
             print(f"DEBUG: count for int(2): {self.db['patient_diet'].count_documents({'patient_id': 2})}")
             print(f"DEBUG: count for str('2'): {self.db['patient_diet'].count_documents({'patient_id': '2'})}")

        correlation = defaultdict(int)

        for record in diet_records:
            foods = record.get("food_category", [])
            symptoms = record.get("symptoms_after_eating", [])
            
            # Debug record content if empty
            if not foods or not symptoms:
                print(f"DEBUG: Skipping record - foods: {foods}, symptoms: {symptoms}")

            for food in foods:
                for symptom in symptoms:
                    key = f"{food} → {symptom}"
                    correlation[key] += 1

        return dict(correlation)


def run_diet_symptom_correlation(patient_id: str):
    service = GIAnalysisService(db)
    return service.diet_symptom_correlation(patient_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Diet ↔ Symptom correlation runner")
    parser.add_argument("patient_id", help="Patient identifier to analyze")
    args = parser.parse_args()

    result = run_diet_symptom_correlation(args.patient_id)
    print(json.dumps(result, indent=2))


# if __name__ == "__main__":

#     service = GIAnalysisService(db)
#     patient_id = "002"  # change as needed
#     result = service.diet_symptom_correlation(patient_id)
#     print(json.dumps(result, indent=2))