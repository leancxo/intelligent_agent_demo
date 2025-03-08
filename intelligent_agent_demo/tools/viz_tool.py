# tools/viz_tool.py
import os
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from langchain.tools import Tool


class VisualizationTool:
    """Tool for creating data visualizations."""

    def __init__(self):
        """Initialize the visualization tool."""
        # Create a directory to store visualizations
        self.viz_dir = "visualizations"
        if not os.path.exists(self.viz_dir):
            os.makedirs(self.viz_dir)

    def create_visualization(self, viz_request):
        """
        Create a data visualization.

        Args:
            viz_request (str): Format should be "type|data|title"
                - type: bar, line, scatter, pie
                - data: comma-separated values for x:y pairs (x1,y1,x2,y2,...)
                - title: chart title

        Returns:
            str: Path to saved visualization or error message
        """
        try:
            # Parse the visualization request
            parts = viz_request.split('|', 2)
            if len(parts) < 3:
                return "Error: Format should be 'type|data|title'"

            viz_type, data_str, title = parts

            # Parse the data
            data_points = data_str.split(',')
            if len(data_points) % 2 != 0:
                return "Error: Data should be comma-separated x,y pairs"

            x_values = [data_points[i] for i in range(0, len(data_points), 2)]
            y_values = [float(data_points[i + 1]) for i in range(0, len(data_points), 2)]

            # Create the visualization
            plt.figure(figsize=(10, 6))

            if viz_type.lower() == 'bar':
                plt.bar(x_values, y_values)
            elif viz_type.lower() == 'line':
                plt.plot(x_values, y_values, marker='o')
            elif viz_type.lower() == 'scatter':
                plt.scatter(x_values, y_values)
            elif viz_type.lower() == 'pie':
                plt.pie(y_values, labels=x_values, autopct='%1.1f%%')
            else:
                return f"Error: Unsupported visualization type '{viz_type}'"

            plt.title(title)
            plt.grid(True)

            # Save the visualization
            filename = f"{self.viz_dir}/{title.replace(' ', '_')}.png"
            plt.savefig(filename)
            plt.close()

            return f"Visualization created and saved as {filename}"

        except Exception as e:
            return f"Error creating visualization: {str(e)}"

    def get_tool(self):
        """Return the tool object for the agent to use."""
        return Tool(
            name="DataVisualization",
            func=self.create_visualization,
            description="""
            Create data visualizations. Input format should be 'type|data|title' where:
            - type: bar, line, scatter, or pie
            - data: comma-separated values for x:y pairs (x1,y1,x2,y2,...)
            - title: chart title
            Example: 'bar|Jan,10,Feb,15,Mar,7,Apr,22|Monthly Sales'
            """
        )