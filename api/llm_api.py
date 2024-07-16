"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai


# Load environment variables from the .env file (if present)
load_dotenv('env/dev.env')

# Access environment variables as if they came from the actual environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
  ]
)


def send_prompt(message:str):
    # message="Create a task to bring milk from shop on 24 Jun 5pm, and the contact number is +9199448283"
    # prompt=f'''
    #           Given the following text: {message}. Extract the task description, date, time, and contact information. Create a sutiable name for the task as well. Output should look like:\n           name: [Name of task]\n           description: [Description of task not including time and date]\n           timeStamp: [Date with time in ISO-8601 format]\n           Contact: [Contact information with +1 extension code]\n          Do not include any other generated text or information.
    #         '''
    generation_config["response_mime_type"]="application/json"
    prompt=message
    response = chat_session.send_message(prompt)
    print(response)
    res_json={"output":response.text}
    return res_json

def send_msq_with_prompt(message:str,prompt_req:str):
    prompt = f'''
              Given the following text: {message}. {prompt_req}
            '''
    response = chat_session.send_message(prompt)
    print(response.text)
    # res_json=json.loads(response.text)
    return response.text
    
def send_category_prompt(message:str):
    # message="Create a task to bring milk from shop on 24 Jun 5pm, and the contact number is +9199448283"
    # prompt=f'''
    #           Given the following link: {message}
    #           Classify above url is of youtube or not. Answer "1" if its youtube link, else "0". No additional information required answer in 1 or 0.
    #         '''
    # response = chat_session.send_message(prompt)
    # print(response.text)
    
    if(message.find('youtube')!=-1):
        return True
    else:
        return False
