import json
import logging
logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

from .utils import (
    read_prompt,
    get_llm_response,
    generate_coverletter_files
)

def write_coverletter(jd_analysed_json, tailored_resume_json):
    logging.info("Writing cover letter...")

    JD_TEXT_PLACEHOLDER = "<JD_TEXT>"
    CV_TEXT_PLACEHOLDER = "<CV_TEXT>"

    try:
        prompt = read_prompt("engine/prompts/write_coverletter_prompt.txt")
        prompt = prompt.replace(JD_TEXT_PLACEHOLDER, json.dumps(jd_analysed_json))
        prompt = prompt.replace(CV_TEXT_PLACEHOLDER, json.dumps(tailored_resume_json))
        llm_response = get_llm_response(prompt)
        logging.debug(f"\t llm_response type: {type(llm_response)}")
        
        response = llm_response.replace("```json", "").replace("```JSON", "").replace("```", "").replace("None","").replace("JSON\n", "")
        coverletter_json = json.loads(response)
        logging.debug(f"\t coverletter_json type: {type(coverletter_json)}")

    
    except Exception as e:
        logging.error(f"Error: error with writing cover letter. \n Detailed error: {e}")
        return None
    
    (coverletter_docx, coverletter_pdf) = generate_coverletter_files(coverletter_json=coverletter_json,
                                                                     resume_json=tailored_resume_json)

    return (coverletter_json, 
            coverletter_docx, 
            coverletter_pdf)
