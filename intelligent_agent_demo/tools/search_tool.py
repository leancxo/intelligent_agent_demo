# tools/search_tool.py
import os
from langchain.tools import Tool


class SearchTool:
    """Tool for performing web searches to find real-time information."""

    def __init__(self):
        """Initialize the search utility."""
        try:
            from langchain_community.utilities import SerpAPIWrapper
            self.search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))
            self.is_available = True
        except ImportError:
            print("Warning: SerpAPI package not available. Install with: pip install google-search-results")
            self.is_available = False

    def search_web(self, query):
        """
        Search the web for information.

        Args:
            query (str): The search query

        Returns:
            str: Search results or error message
        """
        if not self.is_available:
            return "Web search is currently unavailable. Please install required packages."
        return self.search.run(query)

    def get_tool(self):
        """Return the tool object for the agent to use."""
        return Tool(
            name="WebSearch",
            func=self.search_web,
            description="Useful for when you need to find information from the internet. Input should be a search query."
        )