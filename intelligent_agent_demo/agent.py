
# agent.py
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI  # Updated import
from langchain.memory import ConversationBufferMemory

# Import our custom tools
from tools.search_tool import SearchTool
from tools.weather_tool import WeatherTool
from tools.system_tool import SystemTool
from tools.viz_tool import VisualizationTool


class IntelligentAgent:
    """
    A multi-functional intelligent agent that can perform various tasks
    using natural language understanding and specialized tools.
    """

    def __init__(self, verbose=True):
        """
        Initialize the agent with its tools and language model.

        Args:
            verbose (bool): Whether to print detailed processing information
        """
        # Load environment variables
        load_dotenv()

        # Initialize the language model
        self.llm = ChatOpenAI(
            temperature=0.7,  # Controls creativity vs. determinism
            model_name="gpt-4-turbo",  # You can change this based on needs and budget
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        # Initialize memory to store conversation history
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Initialize all our tools
        self.tools = [
            SearchTool().get_tool(),
            WeatherTool().get_tool(),
            SystemTool().get_tool(),
            VisualizationTool().get_tool()
        ]

        # Initialize the agent with tools and memory
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=verbose,
            memory=self.memory,
            handle_parsing_errors=True
        )

    def run(self, user_input):
        """
        Process the user input and return the agent's response.

        Args:
            user_input (str): The user's query or command

        Returns:
            str: The agent's response
        """
        try:
            response = self.agent.run(input=user_input)
            return response
        except Exception as e:
            return f"I encountered an error: {str(e)}"