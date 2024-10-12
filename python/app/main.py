import mysql.connector
from langchain import PromptTemplate
from lib.gen_chain import get_sql_chain

MYSQL_HOST = "mysql"
MYSQL_DATABASE = "mydatabase"
MYSQL_USER = "user"
MYSQL_PASSWORD = "password"
OPENAI_API_KEY="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"
QUESTION_TEST = "siapa orang dengan gaji tertinggi?"

def test_mysql_connection(query):
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        if connection.is_connected():
            cursor = connection.cursor()

            # Create the employee table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS employee (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                salary DECIMAL(10, 2) NOT NULL,
                address VARCHAR(255) NOT NULL
            );
            """
            cursor.execute(create_table_query)
            print("Employee table created successfully.")

            # Populate the employee table with sample data
            insert_query = """
            INSERT INTO employee (name, salary, address)
            VALUES (%s, %s, %s)
            """
            # employees = [
            #     ('Alice Johnson', 50000.00, '123 Main St'),
            #     ('Bob Smith', 60000.00, '456 Oak St'),
            #     ('Carol White', 55000.00, '789 Pine St')
            # ]
            # cursor.executemany(insert_query, employees)
            # connection.commit()  # Commit the changes to the database

            # print(f"{cursor.rowcount} records inserted successfully into employee table.")

            # Check and display the connected database
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"Connected to MySQL database: {record[0]}")

            # Retrieve and display the data from the employee table
            # cursor.execute("SELECT * FROM employee;")
            # test query from llm translate
            cursor.execute(query)
            rows = cursor.fetchall()
            print("Employee records:")
            for row in rows:
                print(row)

            cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def test_langchain():
    prompt = PromptTemplate(input_variables=["name"], template="Hello, {name}!")
    print(prompt.format(name="World"))

if __name__ == "__main__":
    test_mysql_connection(
        get_sql_chain(openai_api_key=OPENAI_API_KEY, question=QUESTION_TEST)
    )
    test_langchain()

