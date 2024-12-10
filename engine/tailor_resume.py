import json
import copy
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
    generate_resume_files
)

def tailor_resume(jd_text, resume_text):
    logging.info("Tailoring resume...")

    JD_TEXT_PLACEHOLDER = "<JD_TEXT>"
    CV_TEXT_PLACEHOLDER = "<CV_TEXT>"

    try:
        prompt = read_prompt("engine/prompts/tailor_resume_prompt.txt")
        prompt = prompt.replace(JD_TEXT_PLACEHOLDER, json.dumps(jd_text))
        prompt = prompt.replace(CV_TEXT_PLACEHOLDER, json.dumps(resume_text))
        llm_response = get_llm_response(prompt)
        logging.debug(f"\t llm_response type: {type(llm_response)}")
        
        response = llm_response.replace("```json", "").replace("```JSON", "").replace("```", "").replace("None","").replace("JSON\n", "")
        tailored_resume_json = json.loads(response)
        logging.debug(f"\t tailored_resume_json type: {type(tailored_resume_json)}")

        # tailored_resume_json = copy.deepcopy(resume_text)

        # logging.info("\tTailoring skills...")
        # tailor_skills_prompt = read_prompt("engine/prompts/tailor_skills_prompt.txt")
        # skills_base_json = {"skills": tailored_resume_json["skills"]}
        # gemini_response = get_llm_response(
        #     tailor_skills_prompt + \
        #     "--\n<JOB_DETAIL>" + json.dumps(jd_text) + "\n</JOB_DETAIL>\n" + \
        #     "--\n<SKILLS>" + json.dumps(skills_base_json) + "\n</SKILLS>")
        # response = gemini_response.replace("```json", "").replace("```JSON", "").replace("```", "").replace("None","").replace("JSON\n", "")
        # skills_tailord_json = json.loads(response)
        # for skillset in skills_tailord_json["skills"]:
        #     if type(skillset['skills']) == list:
        #         converted_string = ", ".join(skillset['skills'])
        #         skillset['skills'] = converted_string
        # tailored_resume_json["skills"] = skills_tailord_json["skills"]


        # logging.info("\tTailoring work experience...")
        # tailor_workexp_prompt = read_prompt("engine/prompts/tailor_workexp_prompt.txt")
        # workexp_base_json = {"work_experience": tailored_resume_json["work_experience"]}
        # gemini_response = get_llm_response(
        #     tailor_workexp_prompt + \
        #     "--\n<JOB_DETAIL>" + json.dumps(jd_text) + "\n</JOB_DETAIL>\n" + \
        #     "--\n<WORK>" + json.dumps(workexp_base_json) + "\n</WORK>")
        # response = gemini_response.replace("```json", "").replace("```JSON", "").replace("```", "").replace("None","").replace("JSON\n", "")
        # workexp_tailord_json = json.loads(response)
        # tailored_resume_json["work_experience"] = workexp_tailord_json["work_experience"]
        

        # logging.info("\tTailoring projects...")
        # tailor_projects_prompt = read_prompt("engine/prompts/tailor_projects_prompt.txt")
        # projects_base_json = {"projects": tailored_resume_json["projects"]}
        # gemini_response = get_llm_response(
        #     tailor_projects_prompt + \
        #     "--\n<JOB_DETAIL>" + json.dumps(jd_text) + "\n</JOB_DETAIL>\n" + \
        #     "--\n<PROJECTS>" + json.dumps(projects_base_json) + "\n</PROJECTS>")
        # response = gemini_response.replace("```json", "").replace("```JSON", "").replace("```", "").replace("None","").replace("JSON\n", "")
        # projets_tailord_json = json.loads(response)
        # tailored_resume_json["projects"] = projets_tailord_json["projects"]
        
        (tailored_resume_docx, 
         tailored_resume_pdf) = generate_resume_files(tailored_resume_json)

        return (tailored_resume_json, 
                tailored_resume_docx, 
                tailored_resume_pdf)
    
    except Exception as e:
        logging.error(f"Error: error tailoring resume. \n Detailed error: {e}")
        return None
    