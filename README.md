# AI Recipe Generator 

This was my final project for **CSC 221** at **The City College of New York (CCNY)**. It is a web application that uses Artificial Intelligence to generate cooking recipes and matching food images.

## Features
- **Smart Recipe Generation:** Uses **Google Vertex AI (Gemini)** to create detailed, structured JSON recipes.
- **AI Imagery:** Uses **Imagen 3.0** to generate high-quality, professional food photos for every dish.
- **FastAPI Backend:** A high-performance Python API managing the logic and AI calls.
- **Cloud Hosted:** Configured for deployment on **Google App Engine**.

## Tech Stack
- **Language:** Python 3.11
- **Framework:** FastAPI
- **Cloud/AI:** Google Cloud Platform (GCP), Vertex AI, Imagen
- **Frontend:** HTML5, CSS (Vanilla), JavaScript

## Project Structure
- `final.py`: The main FastAPI application logic.
- `app.yaml`: Configuration for Google App Engine.
- `static/`: Contains the frontend user interface.
- `requirements.txt`: List of necessary Python libraries.

## Usage
Enter a dish name and a maximum cooking time. The AI will generate a step-by-step recipe and a custom image of the meal!
