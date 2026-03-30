from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import base64
import re
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from vertexai.preview.vision_models import ImageGenerationModel


PROJECT_ID = "your-project-id"  # Replace with your actual GCP project ID
REGION = "us-central1"
vertexai.init(project=PROJECT_ID, location=REGION)


app = FastAPI(title="CSC 221 - Final Challenge")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("static/index.html") as f:
            return f.read()
    except FileNotFoundError:
        return "static/index.html not found."


@app.get("/id", response_class=PlainTextResponse)
def get_id():
    return "11111111_Ordonez"


@app.post("/recipe")
async def recipe(request: Request):
    data = await request.json()
    dish = data.get("description", "Spaghetti")
    max_time = data.get("max_time", 60)

    
    prompt = f"""
Generate a **detailed, realistic cooking recipe** in JSON format for this dish:
Dish: {dish}
Maximum total time (prep + cook): {max_time} minutes.

Include:
- Ingredients grouped by sections (e.g., Dough, Sauce, Toppings)
- Step-by-step instructions for each section
- Return only valid JSON (no extra text)

JSON format:
{{
  "name": "",
  "prep_time": "",
  "cook_time": "",
  "ingredients": [
    {{"Section": ["ingredient 1", "ingredient 2"]}}
  ],
  "instructions": [
    {{"Section": ["step 1", "step 2"]}}
  ],
  "image": ""
}}
"""

    
    try:
        recipe_model = GenerativeModel("gemini-2.5-flash")
        response = recipe_model.generate_content(prompt)
        print("RAW AI RESPONSE:", response.text)

        clean_text = re.sub(r"^```json|```$", "", response.text, flags=re.MULTILINE).strip()
        recipe = json.loads(clean_text)

    except Exception as e:
        print("Vertex AI (Gemini) error:", e)
        # fallback recipe
        recipe = {
            "name": dish,
            "prep_time": "10",
            "cook_time": "20",
            "ingredients": [{"Example": ["Ingredient 1", "Ingredient 2"]}],
            "instructions": [{"Example": ["Step 1", "Step 2"]}],
            "image": ""
        }

    
    try:
        image_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        image_prompt = f"Professional, high-quality food photo of {dish}"
        
        images = image_model.generate_images(
            prompt=image_prompt,
            number_of_images=1,
            aspect_ratio="1:1",
            language="en"
        )
        
        if images:
            image_bytes = images[0]._image_bytes
            recipe["image"] = base64.b64encode(image_bytes).decode("utf-8")
        else:
            recipe["image"] = ""
    except Exception as e:
        print("Imagen error:", e)
        recipe["image"] = ""  # fallback to empty

    return JSONResponse(recipe)
