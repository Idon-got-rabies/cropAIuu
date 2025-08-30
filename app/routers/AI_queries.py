import base64

from fastapi import FastAPI, HTTPException, APIRouter, Depends
import httpx
import os
import logging
from fastapi import APIRouter, HTTPException
from fastapi import UploadFile, Form ,File, UploadFile
from fastapi.responses import JSONResponse
import httpx
import base64

from app import schemas

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
        async with httpx.AsyncClient(timeout=120) as client:

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
async def diseases_ai(
    image: UploadFile = File(...),
    language: str = Form("en")
):
    """
    Scan an uploaded plant leaf image and return:
    - Disease prediction text
    - AI advice for treatment
    - Image in base64 for frontend display
    """
    prompt = (
        "You are a Disease analysis AI. "
        "You are here to help farmers. "
        "Scan the image provided and identify the disease with highest accuracy. "
        "Provide appropriate countermeasures and responses. "
        "Encourage the farmer to be environmentally conscious."
    )

    try:
        # Read uploaded image
        image_bytes = await image.read()

        # Prepare multipart/form-data
        files = {"file": (image.filename, image_bytes, image.content_type)}
        data = {"language": language, "prompt": prompt}  # include prompt if API supports it

        # Send request to the AI API
        async with httpx.AsyncClient(timeout=60) as client:
            try:
                resp = await client.post(DISEASE_API_URL, data=data, files=files)
                resp.raise_for_status()
            except httpx.HTTPError as http_err:
                status_code = getattr(http_err.response, "status_code", 500)
                raise HTTPException(
                    status_code=status_code,
                    detail=f"AI API HTTP error: {http_err}"
                )

        # Try to parse JSON text prediction
        try:
            result_json = resp.json()
            ai_reply = result_json.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception:
            ai_reply = "No text prediction returned"

        # Encode the binary image (from resp.content) in base64
        image_base64 = base64.b64encode(resp.content).decode("utf-8")

        return JSONResponse(content={
            "prediction_text": ai_reply,
            "image_base64": image_base64
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))