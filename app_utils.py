import streamlit as st
import base64

def format_key(key):
    # Replace underscores with spaces and capitalize each word
    return key.replace('_', ' ').title()

def json_to_markdown(data, indent_level=0):
    markdown_str = ""
    prefix = " " * indent_level * 2  # Two spaces per indent_level level
    if isinstance(data, dict):
        for key, value in data.items():
            formatted_key = format_key(key)
            markdown_str += f"{prefix}- **{formatted_key}**: "
            if isinstance(value, (dict, list)):
                markdown_str += "\n" + json_to_markdown(value, indent_level + 1)
            else:
                markdown_str += f"{value}\n"
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                markdown_str += json_to_markdown(item, indent_level + 1)
            else:
                markdown_str += f"{prefix}- {item}\n"
    return markdown_str


def clear_generation_state():
    st.session_state.tailored_resume_json = None
    st.session_state.tailored_resume_docx = None
    st.session_state.tailored_resume_pdf = None

    st.session_state.coverletter_json = None
    st.session_state.coverletter_docx = None
    st.session_state.coverletter_pdf = None


# Load an image and encode it in base64
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return encoded

# Function to read the log file and return its content in reverse order
def read_log_file_reversed(log_file):
    with open(log_file, "r") as file:
        lines = file.readlines()
    # Reverse the order of lines
    return '\n'.join(lines[::-1])

