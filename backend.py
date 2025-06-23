import streamlit as st
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pytesseract
from PIL import Image
from llm_summary import compare_images
load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
model = os.getenv("AZURE_OPENAI_MODEL_NAME")
version = os.getenv("AZURE_OPENAI_API_VERSION")

# print(f"API Key: {api_key}")

# def analyze_graphs(image1_path, image2_path):
#     try:
#         summary = compare_images(image1_path, image2_path)
#         return summary
#     except Exception as e:
#         return f"Error: {e}"

def analyze_graphs(image1_path, image2_path, restaurant_name=None, start_date_1=None, end_date_1=None, start_date_2=None, end_date_2=None):
    try:
        summary = compare_images(
            image1_path,
            image2_path,
            restaurant_name=restaurant_name,
            start_date_1=start_date_1,
            end_date_1=end_date_1,
            start_date_2=start_date_2,
            end_date_2=end_date_2
        )
        return summary
    except Exception as e:
        return f"Error: {e}"
