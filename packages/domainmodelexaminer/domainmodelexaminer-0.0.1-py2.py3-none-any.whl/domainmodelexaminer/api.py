"""
DMX API

This is copied to main.py by the Dockerfile.
"""

from fastapi import FastAPI
import domainmodelexaminer as dmx

tags_metadata = [
  {
    "name": "examine",
    "description": "Pass the GitHub repo url here e.g. examine/?url=https://github.com/jataware/dummy-model.git",
  },
  {
    "name": "root",
    "description": "Confirms the beast is alive.",
  },
]

app = FastAPI(
  title="Domain Model eXaminer",
  description="Performs machine reading over the model codebase in order to automatically extract key metadata.",
  version="0.0.1",
  openapi_tags = tags_metadata
  )


@app.get("/", tags=["root"])
def read_root():
  return {"status": "running"}

@app.get("/examine/", tags=["examine"])
async def get_examination(url):
  yaml = dmx.examine(url)
  return yaml



