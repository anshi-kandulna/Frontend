# utils/form_validators.py

import streamlit as st
from typing import Dict, Tuple, List

class FormValidationHandler:
    """
    Handles form validation and submission across multiple forms
    """
    
    @staticmethod
    def validate_symptom_data(symptom_data: Dict) -> Tuple[bool, List[str]]:
        """Validate symptom form data"""
        errors = []
        
        if not symptom_data.get('symptoms'):
            errors.append("❌ Symptom Assessment: Please select at least one symptom")
        
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_diet_data(diet_data: Dict) -> Tuple[bool, List[str]]:
        """Validate diet form data"""
        errors = []
        
        if not diet_data.get('food_category'):
            errors.append("❌ Dietary Tracking: Please select at least one food category")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_forms(patient_id: str, symptom_data: Dict, 
                       diet_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate all forms together
        Returns (is_valid, error_list)
        """
        all_errors = []
        
        # Validate patient ID
        if not patient_id or patient_id.strip() == "":
            all_errors.append("❌ Please enter your Patient ID")
        
        # Validate each form
        symptom_valid, symptom_errors = FormValidationHandler.validate_symptom_data(symptom_data)
        all_errors.extend(symptom_errors)
        
        diet_valid, diet_errors = FormValidationHandler.validate_diet_data(diet_data)
        all_errors.extend(diet_errors)
        
        is_valid = len(all_errors) == 0
        
        return is_valid, all_errors
    
    