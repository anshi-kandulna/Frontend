# components/gi_dashboard.py

import streamlit as st
from datetime import datetime

from .symptom_form import symptom_form
from .stool_form import stool_form
from .diet_form import diet_form
from .alarm_form import alarm_form
from utils import FormValidationHandler
from services import FormSubmissionHandler

def gi_dashboard():
    """
    Main dashboard page for GI Assessment module
    Single long-form with all fields and submit button at the end
    """
    
    # Initialize session state for form data
    if "symptom_data" not in st.session_state:
        st.session_state.symptom_data = {}
    if "stool_data" not in st.session_state:
        st.session_state.stool_data = {}
    if "diet_data" not in st.session_state:
        st.session_state.diet_data = {}
    if "alarm_data" not in st.session_state:
        st.session_state.alarm_data = {}
    
    # Page title and header
    st.title("🏥 GI Assessment Platform")
    st.markdown("---")
    
    # Welcome section
    st.header("Welcome to GI Assessment")
    st.subheader("Gastrointestinal Disorder Diagnosis Support")
    st.markdown("Please complete all sections below and submit your assessment")
    
    # Patient ID (persistent)
    st.markdown("### Patient Information")
    patient_id = st.text_input("Patient ID *", key="patient_id_input", placeholder="Enter your patient ID")
    
    st.markdown("---")
    
    # Form Section 1: Symptoms
    st.session_state.symptom_data = symptom_form()
    st.markdown("---")
    
    # Form Section 2: Stool Analysis
    st.session_state.stool_data = stool_form()
    st.markdown("---")
    
    # Form Section 3: Dietary Tracking
    st.session_state.diet_data = diet_form()
    st.markdown("---")
    
    # Form Section 4: Red Flag Symptoms
    st.session_state.alarm_data = alarm_form()
    
    st.markdown("---")
    
    # SUBMIT BUTTON AT THE END
    if st.button("📤 Submit Complete Assessment", type="primary", use_container_width=True, key="submit_btn"):
        # Validate all forms
        is_valid, errors = FormValidationHandler.validate_forms(
            patient_id,
            st.session_state.symptom_data,
            st.session_state.diet_data,
        )
        
        # Display validation errors if any
        if not is_valid:
            for error in errors:
                st.error(error)
            st.stop()
        else:
            # Submit to backend
            with st.spinner("Submitting your assessment..."):
                responses = FormSubmissionHandler.submit_all_forms(
                    patient_id,
                    st.session_state.symptom_data,
                    st.session_state.stool_data,
                    st.session_state.diet_data,
                    st.session_state.alarm_data
                )
            
            # Check if all services returned success
            all_success = all(
                resp.get("success", False) 
                for resp in responses.values()
            )
            
            if all_success:
                st.success(f"✅ **Assessment submitted successfully!**")
                
                # Show submission IDs from each service
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.info(f"**Symptoms**\n{responses['symptoms'].get('id', 'N/A')}")
                with col2:
                    st.info(f"**Stool**\n{responses['stool'].get('id', 'N/A')}")
                with col3:
                    st.info(f"**Diet**\n{responses['diet'].get('id', 'N/A')}")
                with col4:
                    st.info(f"**Alarm**\n{responses['alarm'].get('id', 'N/A')}")
                
                #st.markdown("Your doctor will review this assessment and provide recommendations.")
                
                # Reset form after successful submission
                st.session_state.symptom_data = {}
                st.session_state.stool_data = {}
                st.session_state.diet_data = {}
                st.session_state.alarm_data = {}
            else:
                st.error(f"❌ **Submission failed for some forms:**")
                
                # Show errors for each service
                for service_name, response in responses.items():
                    if not response.get("success"):
                        st.error(f"**{service_name.upper()}**: {response.get('error', 'Unknown error')}")