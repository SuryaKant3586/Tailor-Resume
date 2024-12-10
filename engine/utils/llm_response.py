import os
import logging
logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

from dotenv import load_dotenv
load_dotenv()  ## load all our environment variables

# Import the Generative AI model if needed
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
logging.info("Key:", os.getenv("GOOGLE_API_KEY"))


def get_llm_response(input):
    logging.info("\t\tGetting Gemini response...")
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        gemini_response = model.generate_content(input)
        logging.debug(f"\t\t\t gemini_response type: {type(gemini_response)}")
        return gemini_response.text
    
    except Exception as e:
        logging.error(f"Error: error analysing jd. \n Detailed error: {e}")
        return None

# function to take directory and file name as input and return the txt file contents as string
def read_prompt(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"read_prompt Error reading file:{file_path}\nDetailed Error:{e}"
    

