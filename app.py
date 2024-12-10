import streamlit as st

from engine import generate
from app_components import *

import logging
logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)


# Initialize session state for input values and analysis results
# def initialize_session_state():
default_state = {
    'page': "Home",
    'done': False,

    'jd_text': "",
    'resume_file': None,

    'tailored_resume_json': None,
    'tailored_resume_docx': None,
    'tailored_resume_pdf': None,
    
    'coverletter_json': None,
    'coverletter_docx': None,
    'coverletter_pdf': None,
}
for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

def home_page():
    # Header
    st.title("Resume Tailoring")
    # Introduction and Help
    cols = st.columns([4, 1])
    with cols[0]:
        st.write("This application helps you to tailor your resume for a specific job description.")
    with cols[1]:
        if st.button("Help", use_container_width=True):
            st.session_state.page = "Help"
            st.rerun()

    # Input fields
    # st.subheader("Input Resume and Job Description")
    cols = st.columns([1, 1], vertical_alignment="top")
    with cols[0]:
        upload_resume()
    with cols[1]:
        input_jd_text()
    
    # Run button
    cols = st.columns([1, 1])
    if st.session_state.jd_text and st.session_state.resume_file:
        if st.button("Generate Tailored Resume and Cover Letter", use_container_width=True):
            clear_generation_state()

            (st.session_state.tailored_resume_json, st.session_state.coverletter_json,
             st.session_state.tailored_resume_docx, st.session_state.coverletter_docx,
             st.session_state.tailored_resume_pdf,  st.session_state.coverletter_pdf) = generate(st.session_state.jd_text,
                                                                                                 st.session_state.resume_file)

    # Results Section
    if st.session_state.tailored_resume_json or st.session_state.coverletter_json:
        st.subheader("Generation Results:")
        result_view_buttons()


def help_page():
    # Navigation buttons
    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button("Go to Home", key="Top Home button", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
    # display_logs()

    st.markdown("# Help")
    st.write("""
        This application helps you to tailor your resume for specific job descriptions. 
        Follow these steps:
        1. Input job description and your resume on the Home page. The input state is reflected in the Home page and sidebar.
        2. You can tailor your resume by clicking the buttons appeared according to the input state.
        3. Navigate through the pages to view the tailored resume and cover letter.
    """)

    st.markdown("## Frequently Asked Questions (FAQs)")
    st.write("""
        **1. What file formats are supported for resume upload?**
        - The application supports PDF, DOCX, JSON, and TXT formats.

        **2. How do I input the job description?**
        - Copy from the job site page and then input the job description into the text area in the Home page.
    """)

    # Navigation buttons
    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button("Go to Home", key="Bottom Home button", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()


def main():
    # Set page config
    st.set_page_config(
        page_title="Resume Tailoring",
        page_icon=":clipboard:",  # You can use emoji shortcodes for icons
        layout="wide"
    )

    st.sidebar.title("Resume Tailoring")

    pages = {
        "Home": home_page,
        "Tailored Resume": tailored_resume_page(
            page_title="Tailored Resume",
            result_json=st.session_state.tailored_resume_json,
            warning_text="Please input both resume and job description on Home page."
        ) if st.session_state.tailored_resume_json else None,
        
        "Cover Letter": coverletter_page(
            page_title="Cover Letter",
            result_json=st.session_state.coverletter_json,
            warning_text="Please input both resume and job description on Home page."
        ) if st.session_state.coverletter_json else None,
        
        "Help": help_page
    }

    # Sidebar for page navigation at the top
    available_pages = {name: page for name, page in pages.items() if page is not None}
    page = st.sidebar.radio("Navigate pages", 
                            options=list(available_pages.keys()), 
                            index=list(available_pages.keys()).index(st.session_state.page))
    st.session_state.page = page

    # Render the selected page
    if st.session_state.page in available_pages:
        available_pages[st.session_state.page]()

    st.sidebar.markdown("---")
    
    # Display inputs in the sidebar
    st.sidebar.subheader("Your Inputs")
    if st.session_state.resume_file:
        st.sidebar.text(f"Resume file: {st.session_state.resume_file.name}")
    else:
        st.sidebar.text(f"Resume file: None")
    st.sidebar.text_area("Job Description text:", 
                        st.session_state.jd_text, 
                        height=150, 
                        key="sidebar_job_desc_view", 
                        disabled=True)


if __name__ == "__main__":
    main()
