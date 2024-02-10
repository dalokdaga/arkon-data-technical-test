from fastapi import FastAPI
import importlib

app = FastAPI()

"""
Initialize URL
"""
url_module = importlib.import_module("app.api.urls")
