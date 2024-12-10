import streamlit as st
import json
import fitz  # PyMuPDF

from app_utils import *

##########################################################################################
######## Components for Home page ########################################################
# Resume input on Home page
def upload_resume():
    # File uploader
    uploaded_file = st.file_uploader("Input Resume", 
                                     type=["pdf", "docx", "json", "txt"], 
                                     key="resume_uploader")

    # Check if a new file is uploaded
    if uploaded_file is not None and uploaded_file != st.session_state.resume_file:
        st.session_state.resume_file = uploaded_file
        clear_generation_state()
        uploaded_file = None
        # if st.button("Confirm Resume Upload"):
        #     st.success("Resume uploaded successfully.")

    # Display current resume status
    if st.session_state.resume_file:
        st.text(f"Resume: {st.session_state.resume_file.name}")
    else:
        st.text("Resume: None")
    

# Job description input on Home page
def input_jd_text():
    job_desc = st.text_area("Input Job Description", 
                            value=st.session_state.jd_text, 
                            height=300, key="job_desc_area")
    if job_desc != st.session_state.jd_text:
        st.session_state.jd_text = job_desc
        clear_generation_state()
        # if st.button("Confirm Job Description"):
        #     st.success("Job description input successfully.")


# Result view bottons on Home page
def result_view_buttons():
    results_data = {
        "Tailored Resume": st.session_state.tailored_resume_json,
        "Cover Letter": st.session_state.coverletter_json,
    }

    for i in range(0, len(results_data), 2):
        cols = st.columns([1, 1])
        for j in range(2):
            if i + j < len(results_data):
                with cols[j]:
                    label = list(results_data.keys())[i + j]
                    state_key = list(results_data.values())[i + j]
                    if state_key:
                        if st.button(label, use_container_width=True):
                            st.session_state.page = label
                            st.rerun()
                    else:
                        st.empty()

##########################################################################################
######## Components for Help page ########################################################
# Display logs
def display_logs():
    if st.button("Refresh Logs", use_container_width=True):
        log_content_reversed = read_log_file_reversed("app.log")
        st.text_area("Log Output (Newest First)", 
                     log_content_reversed, 
                     height=300,
                     disabled=True)

##################################################################################################
######## Components for result view pages ########################################################
def top_home_help_buttons(page_title):
    # Navigation buttons
    cols = st.columns([1, 2, 1], vertical_alignment='center')
    with cols[0]:
        if st.button("Go to Home", key=f"Top Home button on {page_title}", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
    with cols[2]:
        if st.button("Help", key=f"Top Help button on {page_title}", use_container_width=True):
            st.session_state.page = "Help"
            st.rerun()    

def bottom_home_help_buttons(page_title):
    # Navigation buttons
    cols = st.columns([1, 2, 1], vertical_alignment='center')
    with cols[0]:
        if st.button("Go to Home", key=f"Bottom Home button on {page_title}", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
    with cols[2]:
        if st.button("Help", key=f"Bottom Help button on {page_title}", use_container_width=True):
            st.session_state.page = "Help"
            st.rerun()    


########################################################################################################
######## Tailored Resume and Cover Letter pages ########################################################
def display_and_edit_json(json_data, level=0, parent_key=""):
    indent = " " * (4 * level)
    
    for key, value in json_data.items():
        # Create a unique key by combining the parent key and the current key
        unique_key = f"{parent_key}.{key}" if parent_key else key
        
        if isinstance(value, dict):
            st.markdown(f"{indent}**{key}:**")
            display_and_edit_json(value, level + 1, unique_key)
        elif isinstance(value, list):
            st.markdown(f"{indent}**{key}:**")
            for i, item in enumerate(value):
                item_key = f"{unique_key}[{i}]"
                if isinstance(item, dict):
                    st.markdown(f"{indent}{i+1}.")
                    display_and_edit_json(item, level + 1, item_key)
                else:
                    json_data[key][i] = st.text_input(f"{indent}{i+1}.", item, key=item_key)
        else:
            json_data[key] = st.text_input(f"{indent}{key}", value, key=unique_key)

    return json_data


def display_pdf(pdf_file):
    # Load the PDF file using PyMuPDF
    doc = fitz.open(stream=pdf_file, filetype="pdf")
    num_pages = doc.page_count
    
    st.write(f"**Total Pages:** {num_pages}")

    # Loop through each page and render as an image
    for page_num in range(num_pages):
        page = doc.load_page(page_num)  # Load each page
        pix = page.get_pixmap()  # Render page to a Pixmap image
        
        # Get the original dimensions of the image
        width, height = pix.width, pix.height
        img_data = pix.tobytes("png")  # Convert to PNG format for better compatibility
        
        # Display each page as an image in Streamlit at original size
        st.image(img_data, caption=f"Page {page_num + 1}", width=width)
    
    # Close the PDF document
    doc.close()


def download_files_btns(docx_file, pdf_file, json_data, 
                        resume_cl: str, top_or_bottom: str):
    cols = st.columns([1, 1, 1], vertical_alignment='bottom')
    with cols[0]:
        if st.session_state.tailored_resume_json is not None:
            st.download_button(label="Download JSON",
                               data=json.dumps(json_data, indent=4),
                               file_name=f"{st.session_state.tailored_resume_json['basics'].get('name', '')} {resume_cl}.json",
                               mime="application/json",
                               use_container_width=True,
                               key=resume_cl + 'json_btn' + top_or_bottom)

    with cols[1]:
        if st.session_state.tailored_resume_docx is not None:
            st.download_button(label="Download DOCX",
                               data=docx_file,
                               file_name=f"{st.session_state.tailored_resume_json['basics'].get('name', '')} {resume_cl}.docx",
                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                               use_container_width=True,
                               key=resume_cl + '-docx_btn-' + top_or_bottom)

    with cols[2]:
        if st.session_state.tailored_resume_pdf is not None:
            st.download_button(label="Download PDF",
                               data=pdf_file,
                               file_name=f"{st.session_state.tailored_resume_json['basics'].get('name', '')} {resume_cl}.pdf",
                               mime="application/pdf",
                               use_container_width=True,
                               key=resume_cl + '-pdf_btn-' + top_or_bottom)

##################################################################################
def tailored_resume_page(page_title, result_json, warning_text):
    def page():
        top_home_help_buttons(page_title)
        st.header(page_title)
        if result_json:
            download_files_btns(docx_file=st.session_state.tailored_resume_docx,
                                pdf_file=st.session_state.tailored_resume_pdf,
                                json_data=st.session_state.tailored_resume_json,
                                resume_cl='resume',
                                top_or_bottom='top')
            display_pdf(pdf_file=st.session_state.tailored_resume_pdf)

            download_files_btns(docx_file=st.session_state.tailored_resume_docx,
                                pdf_file=st.session_state.tailored_resume_pdf,
                                json_data=st.session_state.tailored_resume_json,
                                resume_cl='resume',
                                top_or_bottom='bottom')
            bottom_home_help_buttons(page_title)
        else:
            st.warning(warning_text)

    return page


def coverletter_page(page_title, result_json, warning_text):
    def page():
        top_home_help_buttons(page_title)
        st.header(page_title)
        if result_json:
            download_files_btns(docx_file=st.session_state.coverletter_docx,
                                pdf_file=st.session_state.coverletter_pdf,
                                json_data=st.session_state.coverletter_json,
                                resume_cl='cover letter',
                                top_or_bottom='top')
            # display_pdf(pdf_file=st.session_state.coverletter_pdf)
            st.text_area(label='Cover Letter', 
                         label_visibility="hidden",
                         value=result_json["coverletter"],
                         height=500
            )

            download_files_btns(docx_file=st.session_state.coverletter_docx,
                                pdf_file=st.session_state.coverletter_pdf,
                                json_data=st.session_state.coverletter_json,
                                resume_cl='cover letter',
                                top_or_bottom='bottom')
            bottom_home_help_buttons(page_title)
        else:
            st.warning(warning_text)

    return page

