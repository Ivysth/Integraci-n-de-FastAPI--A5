from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

# API KEY DIRECTA
genai.configure(api_key="API_KEY_AQUI")

model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pregunta(BaseModel):
    mensaje: str

@app.post("/preguntar")
def preguntar(datos: Pregunta):

    try:

        respuesta = model.generate_content(datos.mensaje)

        return {
            "respuesta": respuesta.text
        }

    except Exception as e:

        return {
            "respuesta": f"Error Gemini: {str(e)}"
        }