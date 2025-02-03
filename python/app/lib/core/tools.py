from typing import List, Callable, Union

from functools import cache
from lib.metadata.prompt import REFINE_REACT_AGENT_PROMPT

from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool, QueryEngineTool

class ToolCalling:
    """
    A utility class for creating and managing various LlamaIndex tools and agents.
    
    Attributes:
        llm: The language model used for tool creation and agent interactions.
    """
    
    @cache
    def function_tool(self, function: Callable, name: str, description: str) -> FunctionTool:
        """
        Create a FunctionTool with caching for repeated calls.
        
        Args:
            function: The function to be wrapped as a tool.
            name: Name of the tool.
            description: Description of the tool's functionality.
        
        Returns:
            A FunctionTool instance.
        """
        return FunctionTool.from_defaults(
            fn=function,
            name=name, 
            description=description,
        )
    
    @cache
    def query_engine_tool(self, engine, name: str, description: str) -> QueryEngineTool:
        """
        Create a QueryEngineTool with caching for repeated calls.
        
        Args:
            engine: The query engine to be wrapped as a tool.
            name: Name of the tool.
            description: Description of the tool's functionality.
        
        Returns:
            A QueryEngineTool instance.
        """
        return QueryEngineTool.from_defaults(
            query_engine=engine,
            name=name,
            description=description,
        )
        
    @cache
    def react_agent_tool(
        self,
        list_tool: List[Union[FunctionTool, QueryEngineTool]], 
        max_iterations: int = 10
    ) -> ReActAgent:
        """
        Create a ReActAgent with the given tools.
        
        Args:
            list_tool: List of tools for the agent.
            context: Optional context for the agent.
            max_iterations: Maximum number of iterations for the agent.
        
        Returns:
            A ReActAgent instance.
        """
        
        return ReActAgent.from_tools(
            tuple(list_tool),
            max_iterations=max_iterations,
            context=REFINE_REACT_AGENT_PROMPT,
            timeout=180,
            verbose=True,
        )
        