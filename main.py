from typing import Union

from fastapi import FastAPI, Form, Response
from fastapi.responses import JSONResponse
from httpx import request
from api.llm_api import send_category_prompt, send_msq_with_prompt, send_prompt
from api.twilio_whatsapp import send_to_phone
from twilio.twiml.messaging_response import MessagingResponse
from api.url_loader import fetch_detail_from_youtube, fetch_details_from_webpage
from flask import request

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/prompt")
def read_item(prompt: Union[str, None] = None):
    res=send_prompt(prompt)
    send_to_phone(res)
    return res


def message_category(message: Union[str, None] = None):
    res=send_category_prompt(message)
    # respone_msg=""
    if(res):
        print("its yt video")
        text_from_yt=fetch_detail_from_youtube(message)
        respone_msg=send_msq_with_prompt(text_from_yt,'Summaries the above mentioned text in 100 words. Keep it precise and crisp. Return text in paragraph format')
    else:
        print("its document")
        text_from_web=fetch_details_from_webpage(message)
        respone_msg=send_msq_with_prompt(text_from_web,'Summaries the above mentioned text in 100 words. Keep it precise and crisp. Return text in paragraph format')

    send_to_phone(respone_msg)
    return respone_msg

# Define a route to handle incoming requests
@app.post('/whatsapp')
async def chat(From: str = Form(...), Body: str = Form(...)):
   response = MessagingResponse() 
#    message_category(Body)

   msg = response.message(message_category(Body))
#    return Response(content=str(response), media_type="application/xml")
   return '200'

