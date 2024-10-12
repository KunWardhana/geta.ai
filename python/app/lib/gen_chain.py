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