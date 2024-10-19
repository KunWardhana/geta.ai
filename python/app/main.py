import mysql.connector
from flask import Flask, request, jsonify
from langchain import PromptTemplate
from lib.gen_chain import get_sql_chain, transform_query_result_to_sentence, classify_question, general_question, analyze_from_excel
from flask_cors import CORS
import chromadb.api


app = Flask(__name__)
CORS(app)

MYSQL_HOST = "mysql"
MYSQL_DATABASE = "mydatabase"
MYSQL_USER = "user"
MYSQL_PASSWORD = "password"
OPENAI_API_KEY="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"
QUESTION_TEST = "siapa orang dengan gaji tertinggi?"

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
            print("Employee records:")
            for row in rows:
                print(row)

            cursor.close()
        connection.close()
        response = transform_query_result_to_sentence(OPENAI_API_KEY, rows, question)
        return response
    except mysql.connector.Error as err:
        print(f"Error: {err}")


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask app!"})

@app.route('/test_mysql', methods=['POST'])
def api_test_mysql_connection():
    chromadb.api.client.SharedSystemClient.clear_system_cache()
    data = request.get_json()
    question = data.get('question', QUESTION_TEST)
    question_type = classify_question(openai_api_key=OPENAI_API_KEY, question=question)
    print(question_type.content)
    # toket = question_type.content.split(": ")[1]
    toket = question_type.content
    # print(question_type.content)
    if toket  == 'general':
        return jsonify(str(general_question(openai_api_key=OPENAI_API_KEY, question=question).content))
    else:
        try:
            # output = test_mysql_connection(
            #     get_sql_chain(openai_api_key=OPENAI_API_KEY, question=question), question
            # )
            output = analyze_from_excel(openai_api_key=OPENAI_API_KEY, question=question)
            return jsonify(str(output['result'])), 200
        except Exception as e:
            # Tangkap semua error dan tampilkan pesan error
            return jsonify({"error": str(e)}), 500

@app.route('/test_langchain', methods=['GET'])
def api_test_langchain():
    chromadb.api.client.SharedSystemClient.clear_system_cache()
    prompt = PromptTemplate(input_variables=["name"], template="Hello, {name}!")
    result = prompt.format(name="World")
    return jsonify({"result": result}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)