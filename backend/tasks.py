# tasks.py
from celery_app import app
import requests

@app.task
def fetch_data():
    try:
        response = requests.get("https://httpbin.org/json")
        print("Fetched data:", response.json())
    except Exception as e:
        print("Error:", e)
