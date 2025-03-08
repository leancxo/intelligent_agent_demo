# tools/search_tool.py
import os
from langchain.utilities import SerpAPIWrapper
from langchain.tools import Tool


class SearchTool:
    """Tool for performing web searches to find real-time information."""

    def __init__(self):
        """Initialize the search utility."""
        self.search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))

    def search_web(self, query):
        """
        Search the web for information.

        Args:
            query (str): The search query

        Returns:
            str: Search results
        """
        return self.search.run(query)

    def get_tool(self):
        """Return the tool object for the agent to use."""
        return Tool(
            name="WebSearch",
            func=self.search_web,
            description="Useful for when you need to find information from the internet. Input should be a search query."
        )