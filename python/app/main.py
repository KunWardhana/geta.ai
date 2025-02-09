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

    with open ('prompt_history.txt', 'a') as file:
        file.write("Question : " + question + "\n")

    try:
        with open ('prompt_history.txt', 'r') as file:
            question_prompt = file.read()
        

        print ("Ini prompt-nya" + question_prompt)
        response = await llamaindex(question_prompt)
        
        with open ('prompt_history.txt', 'a') as file:
            file.write("Prompt : " + str(response) + "\n")
        
        # print("Ini adalah : " + response)

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

        print(response)

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
    BASE_URL = "https://travoy.jasamarga.co.id:3000"
    api_url =  BASE_URL + "/v4/login"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Body parameters
    data = {
        "username": "rahmatisni@gmail.com",
        "password": "Abc123123",
    }
    
    try:
        response = requests.post(api_url, data=data, headers=headers)
        response.raise_for_status()

        json_data = response.json()

        print("Status Code:", response.status_code)
        print("Response Body:", response.text)

        if response.status_code == 200:
            response_json = response.json()
            access_token = response_json.get("data", {}).get("access_token", "No access token found")
            print("Access Token:", access_token)
        else:
            print("Failed to get response, Status Code:", response.status_code)

        return response.text

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
