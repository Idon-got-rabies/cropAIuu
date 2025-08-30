import base64

from fastapi import FastAPI, HTTPException, APIRouter, Depends
import httpx
import os
import logging

from app import schemas

router = APIRouter(prefix="/ask-ai",
                   tags=["AI Queries"])

SYSTEM_PROMPT = (
    "You are CropAI, an agricultural ai chatbot."
    "You are here to help farmers"
    "Always respond clearly and concisely and as accurately as possible"
    "Remember that the farmer is most likely a local farmer so make sure ur advice is easy to understand"
    "You are to provide advice on agriculture, climate change and how farming affects it, farming practices that help in the fight "
    "against climate change, and growing tips and how to maximise yields and other such things"
    "remember to make your answers as concise as possible, not too long"
)

API_KEY = os.getenv("INFLECTION_API_KEY")
API_URL = os.getenv("INFLECTION_API_URL")
DISEASE_API_URL = os.getenv("DISEASE_API_URL")

@router.post("/")
async def ask_chat_bot(prompt: schemas.PromptRequest ):
    print(f"=== DEBUG INFO ===")
    print(f"API_URL: {API_URL}")
    print(f"API_KEY exists: {bool(API_KEY)}")
    print(f"Prompt received: {prompt.prompt}")
    try:
        async with httpx.AsyncClient(timeout=60) as client:

                resp = await client.post(
                    API_URL,
                    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                    json={
                        "model": "Pi-3.1",
                        "messages":[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": prompt.prompt}
                        ]
                    }
                )

                print(f"=== RESPONSE INFO ===")
                print(f"Status code: {resp.status_code}")
                print(f"Response text: {resp.text}")
                if resp.status_code != 200:
                    raise HTTPException(status_code=resp.status_code, detail=resp.text)

                data = resp.json()

                ai_reply = data["choices"][0]["message"]["content"]
                return {"answer": ai_reply}

    except HTTPException:
        raise

    except Exception as e:

        error_msg = f"Unexpected error: {type(e).__name__}: {str(e)}"

        print(f"Exception details: {error_msg}")

        logging.error(error_msg)

        raise HTTPException(status_code=500, detail=error_msg)



@router.post("/predict/")
async def diseases_ai(image: schemas.DiseaseImage,
                      language: str = "en"
                      ):
    prompt = ("You are a Disease analysis ai"
              "you are here to help farmers"
              "you will scan the image provided and identify the disease with the highest accuracy possible "
              "you will also make sure to give appropriate countermeasures and responses to the disease itself"
              "make sure to encourage the farmer to be as environmentally conscious as possible")
    try:
        image_bytes = await image.image.read()
        files = {
            "file": (image.filename, image_bytes, image.content_type)
        }
        data = {
            "language": language
        }

        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                DISEASE_API_URL,
                data=data,
                files=files

            )
            data = resp.json()
            ai_reply = data["choices"][0]["message"]["content"]

            return {"answer": ai_reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))