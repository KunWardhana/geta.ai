import mysql.connector
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain import PromptTemplate
from lib.gen_chain import get_sql_chain, transform_query_result_to_sentence, classify_question, general_question, analyze_from_excel
import chromadb.api
from langchain.memory import ConversationBufferMemory

import requests
import pandas as pd

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

MYSQL_HOST = "mysql"
MYSQL_DATABASE = "mydatabase"
MYSQL_USER = "user"
MYSQL_PASSWORD = "password"
OPENAI_API_KEY = "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"
QUESTION_TEST = "siapa orang dengan gaji tertinggi?"
X_API_KEY = "a186751c-791c-4bf3-8fd5-5bd27e220f59"

# Initialize global memory for conversation history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


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

        response = transform_query_result_to_sentence(OPENAI_API_KEY, rows, question)
        return response
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")


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

        data = question
        question_type = classify_question(openai_api_key=OPENAI_API_KEY, question=data)

        if question_type.content == 'general':
            return {"result": str(general_question(openai_api_key=OPENAI_API_KEY, question=question).content)}
        else:
            output = analyze_from_excel(openai_api_key=OPENAI_API_KEY, question=question, memory=memory)
            return {"result": str(output)}
        # if question.lower() == "general":
        #     response = {"result": "This is a general question response"}
        # else:
        #     response = {"result": f"Response for question: {question}"}

        # return response

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
