from .tailor_resume import tailor_resume
from .write_coverletter import write_coverletter
from .utils import extract_text_from_file


def generate(jd_text, resume_file):
    resume_text = extract_text_from_file(resume_file)

    # If both analyses are available, proceed with further evaluation and tailoring
    (tailored_resume_json,
     tailored_resume_docx,
     tailored_resume_pdf) = tailor_resume(jd_text, 
                                          resume_text)
    (coverletter_json,
     coverletter_docx,
     coverletter_pdf) = write_coverletter(jd_text, 
                                          tailored_resume_json)
    
    return (
        tailored_resume_json,       coverletter_json,
        tailored_resume_docx,       coverletter_docx,
        tailored_resume_pdf,        coverletter_pdf
    )
