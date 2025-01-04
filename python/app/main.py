import mysql.connector
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain import PromptTemplate
from lib.gen_chain import get_sql_chain, transform_query_result_to_sentence, classify_question, general_question, analyze_from_excel
import chromadb.api
from langchain.memory import ConversationBufferMemory

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
