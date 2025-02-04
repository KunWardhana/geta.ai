import mysql.connector
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from lib.core.retriever import llamaindex
from dotenv import load_dotenv
from typing import AsyncGenerator
import asyncio
import os
import requests
import pandas as pd

load_dotenv()

class QuestionRequest(BaseModel):
    question: str

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
X_API_KEY = os.environ.get("X_API_KEY")

def test_mysql_connection(query, question):
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
        connection.close()

        # response = transform_query_result_to_sentence(OPENAI_API_KEY, rows, question)
        response = 'INI BELUM DI BUTUHIN'
        return response
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

async def llamaindex_stream(question: str) -> AsyncGenerator[str, None]:
    try:
        response = llamaindex(question)

        for chunk in response.response.split(): 
            yield chunk + " "
            await asyncio.sleep(0.05) 

    except Exception as e:
        yield f"Error: {str(e)}"

@app.get("/")
async def home():
    return {"message": "Welcome to the FastAPI app!"}


@app.post("/prompt_llm")
async def api_llm_prompt(data: QuestionRequest):
    """
    Endpoint to process a question and return results based on its type.
    """
    try:
        question = data.question
        print(f"Received question: {question}")

        response = llamaindex(
            question
        )

        return {"result": str(response)}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/test_langchain")
async def api_test_langchain():
    try:
        chromadb.api.client.SharedSystemClient.clear_system_cache()
        prompt = PromptTemplate(input_variables=["name"], template="Hello, {name}!")
        result = prompt.format(name="World")
        return {"result": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/fetch_faq_data")
async def fetch_data():
    """
    Fetch data from the API and save it as a CSV file.
    """
    api_url = "https://api-gateway.jasamarga.co.id/prd/jmclick-ess/faq"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTEyOCwidXNlciI6IjEwNjkxIiwicHJvZmlsZV9pZCI6MTMyNjY3LCJ1c2VybmFtZSI6IjEwNjkxIiwidl91c2VybmFtZSI6IjEwNjkxIiwia2RfY29tcCI6IkpTTVIiLCJrZF9jb21wX2FzYWwiOiJKU01SIiwia2RfY29tcF9wZW51Z2FzYW4iOm51bGwsImtlbG9tcG9rX2phYmF0YW4iOiJOb24gT3BlcmFzaW9uYWwiLCJuYW1hIjoiTU9IQU1BRCBERU5JUyBKVUxJQU5TWUFIIiwidW5pdF9rZXJqYV9pZCI6NDAwMDAwMjAsImtkdW5pdCI6NDAwMDAwMjAsInVuaXQiOiJJbmZvcm1hdGlvbiBUZWNobm9sb2d5IEdyb3VwIiwidXNlcmlkIjoiMTA2OTFKU01SIiwicG9zaXRpb25faWQiOjMwMDExOTE2LCJwaG90byI6Imh0dHBzOi8vY2RuLmphc2FtYXJnYS5jby5pZC9hZ2dyZWdhdG9yLWRhdGEtZGV2L0VtcGxveWVlRmlsZS9Qcm9maWxlLzEwNjkxLnBuZyIsInJvbGUiOm51bGwsImFjY2VzcyI6dHJ1ZSwianRpIjoibzdqeHRpIiwic3ViIjoiMTAuMS4xMi4yNDIiLCJtdWx0aV9yb2xlIjpbXSwiaWF0IjoxNzM1OTY3MjMwLCJleHAiOjE3MzY1NzIwMzB9.AeJ0k_injHzMv-eNNNaKyGkL2V2uiq6hG57_UUtWHCU",
        "x-api-key": X_API_KEY,
    }
    file_path = "faq_data.csv"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        json_data = response.json()

        if 'data' in json_data:
            data = json_data['data']
        else:
            raise ValueError("Unexpected JSON format: 'data' key not found.")

        # Convert JSON 'data' to DataFrame and save to CSV
        df = pd.json_normalize(data)
        df.to_csv(file_path, index=False)
        print(f"Data successfully fetched and saved to {file_path}")

        return {"message": f"Data successfully saved to {file_path}"}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from API: {e}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error processing JSON data: {e}")
        
@app.post("/stream_llm")
async def api_llm_stream(data: QuestionRequest):
    """
    FastAPI endpoint to process questions and stream responses.
    """
    return StreamingResponse(llamaindex_stream(data.question), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
