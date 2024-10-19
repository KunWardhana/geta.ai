def get_sql_chain(openai_api_key,question):
    from langchain_openai import OpenAI, OpenAIEmbeddings, ChatOpenAI
    from langchain_chroma import Chroma
    import os
    from langchain_core.example_selectors.semantic_similarity import SemanticSimilarityExampleSelector
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.prompts.few_shot import FewShotChatMessagePromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from lib.tools import(sanitize_output, remove_new_lines)

    #@title Few Shots
    examples = [
        {
            "input": "how many employee in this company",
            "query": "SELECT COUNT(*) from employee"
        },
        {
            "input": "siapa pegawai dengan gaji terbesar?",
            "query": "SELECT name from employee order by salary desc"
        },
        {
            "input": "siapa pegawai yang tinggal di bandung?",
            "query": "SELECT name from employee where lower(address) like '%bandung%'"
        },
    ]

    to_vectorize = [" ".join(example.values()) for example in examples]
    example_metadatas = [{"id": i, **example} for i, example in enumerate(examples)]
    embeddings = OpenAIEmbeddings(api_key=os.environ.get("OPENAI_API_KEY", openai_api_key))
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples=examples,
        embeddings=embeddings,
        vectorstore_cls=vectorstore,
        k=2,
        input_keys=["input"]
    )

    example_prompt = ChatPromptTemplate.from_messages(
    [
        ('human', '{input}'),
        ('ai', '{query}\n')
    ]
    )

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        input_variables=["input"],
        example_selector=example_selector,
        example_prompt=example_prompt
    )

    INSTRUCTION = """This is a task converting text into MySql statement.
    We will first give you the dataset schema and then ask a question in text.
    You are asked to generate a syntactically correct MySql statement.
    You are provided with some few-shot examples. From the user's question, you must find the most appropriate context from the few-shot examples, and generate the correct query.
    Unless the few-shot examples do not accommodate the user's question, the generated query must be strictly as similar as possible from the query from few-shot examples.
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 20 results.
    Your query result alias should be in English only, referencing to the few-shot examples below.
    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
    """

    final_gen_sql_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", INSTRUCTION),
            # MessagesPlaceholder('chat_history'),
            few_shot_prompt,
            ("human", "{input}"),
            ("ai", "")
        ]
    )

    gen_sql_query_llm = ChatOpenAI(
    model = "gpt-4",
    max_tokens=4097,
    temperature=0.1,
    api_key=os.environ.get("OPENAI_API_KEY", openai_api_key))

    sql_query_chain = final_gen_sql_prompt | gen_sql_query_llm | StrOutputParser() | sanitize_output | remove_new_lines

    sql_query = sql_query_chain.invoke(question)

    return sql_query


def transform_query_result_to_sentence(openai_api_key, executed_query_result, context):
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    import os

    INSTRUCTION = """You are provided with the context of the user's question and the output of an executed SQL query. 
    Your task is to transform this output into a clear and concise sentence or paragraph that provides the information requested by the user.
    Be sure to include relevant information from the context to ensure the response is meaningful and clear.
    """

    prompt_message = f"{INSTRUCTION}\nContext: {context}\nSQL Query Output: {executed_query_result}\n"



    response_llm = ChatOpenAI(
        model="gpt-4",
        max_tokens=4097,
        temperature=0.7,
        api_key=os.environ.get("OPENAI_API_KEY", openai_api_key)
    )

    response_sentence = response_llm(prompt_message)

    return response_sentence

def classify_question(openai_api_key,question):
    from langchain_openai import ChatOpenAI
    import os

    INSTRUCTION = """
        You are an input prompt classifier for a financial-related chatbot. 
        This chatbot is named Andrea.AI and can answer everything related to Frequently Asked Questions (FAQ) and employee analysis within the Indonesian Transportation National Company (Free road).
        If the user asks about Andrea.AI or what she can answer, you must return 'general' as your output.
        If the user asks about name, salary, address of employee related, you must return 'database' as your output.
        Don't print the "output: ". Please only the 'general' or 'database'
        Classify the user's input prompt into 'general', or 'database'!

        input: Hello andrea.ai?
        output: general
        input: What can andrea.ai do?
        output: general
        input: What can you do?
        output: general
        input: Who are you?
        output: general
        input: What is your name?
        output: general
        input: Please introduce yourself
        output: general
        input: What type of question that you can answer?
        output: general
        input: Lupa password
        output: database
        input: Employee with highest paid?
        output: database
        input: Employee who live in oak?
        output: database
        input: Bagaimana cara mengisi survei EES?
        output: database
        input: Apakah pengisian survei dapat dilakukan dimobile phone?
        output: database
        input: Siapa saja yang dapat mengisi survei?
        output: database
        input: Bagaimana cara mengisi EDP untuk Learder?
        output: database
        input: Bagaimana cara mengisi EDP untuk Karyawan?
        output: database
        input: Bagaimana melakukan penilaian Self Declare ?
        output: database
        input: Passcode tidak muncul pada layar
        output: database
        input: Bagimana cara mengisi WB ?
        output: database
        input: Mengapa Atasan tidak bisa menurunkan WB ?
        output: database
        input: Bagaimana cara membuat WB bagi Karyawan yang mutasi ?
        output: database
        input: Bagaimana melakukan penialaian JMPD ?
        output: database
        input: Bagaimana cara melihat Nilai JMPD
        output: database
        input: Bagaimana cara melakukan pengajuan lembur ?
        output: database
        input: Bagaimana cara melakukan pengajuan cuti ?
        output: database
        input: Bagaimana cara melihat e-SPT ?
        output: database
        input: Bagaimana cara melihat e-Payslip
        output: database
        input: Bagaimana cara menggunakan fitur Feedback?
        output: database
        input: Bagaimana Cara update e-CV ?
        output: database
        input: Bagaimana cara download e-CV?
        output: database
        input: Bagaimana cara melakukan simulasi Simpensiun?
        output: database
        input: Bagaimana cara mengajuakan SPPD?
        output: database
        input: Bagaimana cara melihat nilai Talent Class ? 
        output: database
        input: Bagaimana cara Registrasi pelatihan ?
        output: database
        input: Kenapa Learning Point  tidak muncul setelah melakukan check-out?
        output: database
        input: Mengapa setelah membuka konten, poin tidak bertambah ?
        output: database
        input: Apakah fitur kolaboratif sudah bisa digunakan?
        output: database
        input: Bagaimana cara melihat learning point pemebelajaran?
        output: database
        input: Bagaimana cara check in pelatihan ?
        output: database
        input: Bagiamana cara check out pelatihan ?
        output: database
        input: Apakah saya bisa menambahkan riwayat pelatihan mandiri?
        output: database
        input: Bagaimana cara upload konten Video di JM-click ?
        output: database
        input: Bagaimana cara upload konten e-Book di JM-click ?
        output: database
        input: Bagaimana cara upload konten Podcast di JM-click ?
        output: database
        input: Bagaimana cara upload konten Makalah di JM-click ?
        output: database
        input: Bagaimana cara mengisi Learning Diary di JM-Click ?
        output: database
        input: Bagimana cara mengisi survey NPS pada Website dan Mobile?
        output: database
        input: Bagaimana cara menilai behavior
        output: database
        input: Bagaimana ketentuan range nilai NPS  ?
        output: database
        input: Kapan dilaksanakan Survey NPS
        output: database
        input: Bagaimana cara merubah password?
        output: database
        input: Bagaimana jika saat membuka JM-Click lambat ?
        output: database
        input: Bagaimana jika gagal koneksi wifi kantor
        output: database
        input: Bagaimana jika photo profil tidak muncul
        output: database
        input: Bagaimana jika terjadi blank hitam ketika membuka JM-Click 
        output: database
        
        input: {input}
        output:
    """

    prompt_message = f"{INSTRUCTION}\nQuestion: {question}\n"

    response_llm = ChatOpenAI(
        model="gpt-4",
        max_tokens=4097,
        temperature=0.7,
        api_key=os.environ.get("OPENAI_API_KEY", openai_api_key)
    )

    response_sentence = response_llm(prompt_message)

    return response_sentence

def general_question(openai_api_key,question):
    from langchain_openai import ChatOpenAI
    import os
    
    GENERAL_QUESTION = """
        Context:
            You are a chatbot named "Andrea.AI".
            Your main task is to answer question or sentences from an input.
            Below are the example questions that you are capable of answering:
            - Sales January - December 2023
            - Sales in 2023
            - Tell me about sales in 2022
            - Tell me about sales in Jakarta in Q2 2023
            - Top 23 products in Semester 1 2022
            - Top products in Bandung Semester 1 2022
            - Top products in Jatim in 2022
            - Tell me about top departments in 2023
            - What is the top department in 2022?T
            - Tell me about top product category in Aceh in 2022
            - Forecast sales for 2024
            - Predict sales in 2024
            - Predict sales in Jakarta for 2024
            - Predict sales in Surabaya for 2024
            - Yearly sales growth 2022-2023
            - yoy sales growth 2022 to 2023

        Instruction:
        Answer user's question based on the provided context above as best as possible in a professional way. If the user's question can't be answered using the provided context and information, you must elaborate the answer with your knowledge. Do not answer that you do not know the answer. You have the capability to answer any questions!

        User's input: {input}
        Answer:
    """

    prompt_message = f"{GENERAL_QUESTION}\nQuestion: {question}\n"

    response_llm = ChatOpenAI(
        model="gpt-4",
        max_tokens=4097,
        temperature=0.7,
        api_key=os.environ.get("OPENAI_API_KEY", openai_api_key)
    )

    response_sentence = response_llm(prompt_message)

    return response_sentence

def analyze_from_excel(openai_api_key,question):
    from langchain_community.document_loaders import UnstructuredExcelLoader
    from langchain.document_loaders import CSVLoader
    from langchain.indexes import VectorstoreIndexCreator
    from langchain.chains import RetrievalQA
    from langchain.llms import OpenAI
    import pandas as pd
    import os
    from langchain.embeddings import OpenAIEmbeddings

    llm = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", openai_api_key))
    embeddings = OpenAIEmbeddings(api_key=os.environ.get("OPENAI_API_KEY", openai_api_key))

    loader = UnstructuredExcelLoader("faq.xlsx", mode="elements")
    # docs = loader.load()

    index = VectorstoreIndexCreator(
        embedding=embeddings,# vectorstore_cls=DocArrayInMemorySearch
        ).from_loaders([loader])

    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=index.vectorstore.as_retriever(), input_key="question")
    query = question
    response = chain({"question": query})
    
    return response
