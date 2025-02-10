from typing import List, Union

from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent import ReActAgent
from lib.utils.call_api import call_api

from lib.core.tools import ToolCalling, FuzzyMatcher
from lib.core.engine import NLSQLQueryEngine

from lib.metadata.config import gen_config_sql
from lib.metadata.prompt import REFINE_REACT_AGENT_PROMPT

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker



async def tool_colonizing(
    llm: OpenAI,
    sql_database: SQLDatabase,
    list_table: List[str],
) -> List[QueryEngineTool]:
    """
    Populate and configure agents for multiple tables and vector stores retrieval.
    
    Args:
        llm: Lite model Gemini for various task
        database: SQLAlchemy engine of BigQuery
        list_tables: List of table names to process
    
    Returns:
        Configured list of query engine tool
    """
    try:
        tool = ToolCalling()
        agent_tools = []
        
        Session = sessionmaker(bind=sql_database.engine)
        session = Session()
        result = session.execute(text("SELECT DISTINCT name FROM highways"))
        location_names = [row[0] for row in result.fetchall()]
        session.close()

        # Initialize fuzzy matcher
        fuzzy_matcher = FuzzyMatcher(location_names)

        nlsql_engine = NLSQLQueryEngine(
            llm=llm,
            sql_database=sql_database,
            fuzzy_matcher=fuzzy_matcher
        )

        ## Setup NL SQL Table Retriever Tool ##
        query_sql_tool = tool.query_engine_tool(
            engine=await nlsql_engine.create_engine(sql_database, tuple(list_table)),  # ✅ Now properly passing sql_database and list_table
            name = "sql_query_engine",
            description = (
                "Useful for translating a natural language query into a SQL query to retrieve informations from database"
            )
        )
        agent_tools.append(query_sql_tool)

        api_tool = tool.function_tool(
                function = call_api,
                name = "call_api_tool",
                description = (
                    "This tool call an api for retrieving traffic info for the given road segment."
                    " The input parameter must be one of the following values: info traffic, info jalan tol"
                )
            )
        agent_tools.append(api_tool)

        return agent_tools
    
    except Exception as e:
        print(f"Error in call_agent: {e}")
        raise

async def llamaindex(
        question
    ):
    LIST_TABLES = ["rest_area_place_facilities","rest_area_place_types","rest_area_places","tbl_master_tarif", "highways", "rest_areas"]
    db_engine = create_engine(f"mysql+pymysql://user:password@mysql:3306/mydatabase")
    SQLDATABASE = SQLDatabase(db_engine, include_tables=LIST_TABLES)
    
    llm = OpenAI(
        model="gpt-4o",
        max_tokens=2048,
        temperature=0.1,
        context_window=15000
    )

    agent_tools = await tool_colonizing(
        llm=llm,
        sql_database=SQLDATABASE,
        list_table=LIST_TABLES
    )
   
    query_engine = ReActAgent.from_tools(
        agent_tools,
        # memory=memory,
        context=REFINE_REACT_AGENT_PROMPT,
        max_iterations=10,
        timeout=180,
        verbose=True,
    )

    response = query_engine.query(question)

    return response