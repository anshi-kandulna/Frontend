import sys
import os

# Add parent directory to path for imports
# parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, parent_dir)

from database.mongo import db

symptom_collection = db['patient_symptoms']
diet_collection = db['patient_diet']
stool_collection = db['patient_stool']
alarm_collection = db['patient_alarms']


def get_patient_symptoms(patient_id):
    try:
        symptoms = symptom_collection.find({"patient_id": patient_id})
        return list(symptoms)
    except Exception as e:
        print(f"Error fetching symptoms: {e}")
        return []


def get_patient_diet(patient_id):
    try:
        diets = diet_collection.find({"patient_id": patient_id})
        return list(diets)
    except Exception as e:
        print(f"Error fetching diet: {e}")
        return []


def get_patient_stool(patient_id):
    try:
        stools = stool_collection.find({"patient_id": patient_id})
        return list(stools)
    except Exception as e:
        print(f"Error fetching stool: {e}")
        return []


def get_patient_alarms(patient_id):
    try:
        alarms = alarm_collection.find({"patient_id": patient_id})
        return list(alarms)
    except Exception as e:
        print(f"Error fetching alarms: {e}")
        return []


def get_full_patient_data(patient_id):

    symptoms = get_patient_symptoms(patient_id)
    diet = get_patient_diet(patient_id)
    stool = get_patient_stool(patient_id)
    alarms = get_patient_alarms(patient_id)

    return {
        "symptoms": symptoms,
        "diet": diet,
        "stool": stool,
        "alarms": alarms
    }

def get_all_symptoms():
    try:
        return list(symptom_collection.find())
    except Exception as e:
        print(f"Error fetching all symptoms: {e}")
        return []


def get_all_diets():
    try:
        return list(diet_collection.find())
    except Exception as e:
        print(f"Error fetching all diets: {e}")
        return []


# For testing - call this function when needed, not at module import
def test_connection(patient_id="002"):
    print(f"Testing GI Data Service with patient_id: {patient_id}")
    
    data = get_full_patient_data(patient_id)
    print(f"\nRetrieved data: {data}")
    return data

# if __name__ == "__main__":
   
   