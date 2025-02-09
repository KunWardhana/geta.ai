from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Tuple
from functools import lru_cache

from llama_index.llms.openai import OpenAI
from llama_index.core import SQLDatabase
from llama_index.core.prompts.base import PromptTemplate
from llama_index.core.query_engine import NLSQLTableQueryEngine

from lib.metadata.prompt import (
    REFINE_SQL_TEXT_TO_SQL_PROMPT
)

class BaseEngine(ABC):
    """Abstract base class for database engines with common initialization."""
    
    def __init__(
        self,
        llm: OpenAI
    ):
        """
        Initialize the base engine with common parameters.
        
        :param llm: Lite model Gemini for various task
        :param project_id: Cloud project identifier
        """
        self.llm = llm
        
    @abstractmethod
    async def create_engine(self, *args: Any, **kwargs: Any) -> Any:
        """Abstract method to create and return a database engine."""
        pass
    
class NLSQLQueryEngine(BaseEngine):
    """NL Engine for retrieving and querying SQL table schemas."""

    def __init__(self, llm: OpenAI, sql_database: SQLDatabase, fuzzy_matcher):
        """
        Initialize the NLSQL Query Engine with fuzzy matching for location names.
        """
        super().__init__(llm)
        self.sql_database = sql_database
        self.fuzzy_matcher = fuzzy_matcher
    
    def few_shot_examples_fn(self, list_table: List[str]):
        import json

        result_strs = []
        for line in open(f"./lib/few_shot/geta_fewshot_example.jsonl", "r"):
            raw_dict = json.loads(line)
            query = raw_dict["query"]
            response_dict = raw_dict["response"]
                
            result_str = (
                f"Query: {query}\n"
                f"Response: {response_dict}"
            )
            result_strs.append(result_str)
                
        return "\n\n".join(result_strs)
    
    async def preprocess_query(self, user_query: str) -> str:
        """
        Preprocess user query by replacing misspelled location names using fuzzy matching.
        """
        words = user_query.split()
        corrected_words = [self.fuzzy_matcher.find_closest(word) for word in words]
        return " ".join(corrected_words)

    @lru_cache(maxsize=128)
    async def create_engine(
        self,
        database: SQLDatabase,
        list_table: Tuple[str]
    ) -> NLSQLTableQueryEngine:
        """
        Create a NLSQLTableQueryEngine with connection to bigquery.
        
        Args:
            database: The database engine.
            table_name: The table/view name.
        
        Returns:
            A NLSQLTableQueryEngine instance.
        """
        query_engine = NLSQLTableQueryEngine(
            sql_database=database, 
            tables=list_table,
            verbose=True,
            markdown_respons=True,
            synthesize_response=True,
            refresh_schema=False,
            llm=self.llm,
        )
        
        generate_examples = self.few_shot_examples_fn(list_table)
        refine_template_prompt = REFINE_SQL_TEXT_TO_SQL_PROMPT.replace('[few_shot_examples]', generate_examples)

        custom_prompt = PromptTemplate(template=refine_template_prompt)
        query_engine.update_prompts(
            {"sql_retriever:text_to_sql_prompt": custom_prompt}
        )

        query_engine.preprocess_query = self.preprocess_query
        return query_engine