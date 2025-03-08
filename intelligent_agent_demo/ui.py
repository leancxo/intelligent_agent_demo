# ui.py
import streamlit as st
import os
from agent import IntelligentAgent


def main():
    """Main function to run the Streamlit UI."""
    # Set page configuration
    st.set_page_config(
        page_title="Pat's Intelligent Agent Demo",
        page_icon="🤖",
        layout="wide"
    )

    # Initialize session state for conversation history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "agent" not in st.session_state:
        # Initialize the agent (do this only once)
        st.session_state.agent = IntelligentAgent(verbose=False)

    # Header
    st.title("🤖 Intelligent Agent Demo")
    st.markdown("""
    This Pat created agent can answer questions, search the web, check the weather, 
    manage notes, and create visualizations. Try asking it something!
    """)

    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # If there's an image to display
            if message.get("image"):
                st.image(message["image"])

    # Input for new message
    if prompt := st.chat_input("I thank the master Patrick, How can I help you today?"):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response with a spinner while processing
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Thinking..."):
                # Get response from agent
                response = st.session_state.agent.run(prompt)

                # Check if response contains a reference to a visualization
                image_path = None
                if "visualization" in response.lower() and ".png" in response:
                    # Extract image path
                    import re
                    match = re.search(r"(?:saved as|created at) ([\w\/\._-]+\.png)", response)
                    if match:
                        image_path = match.group(1)

                # Display the response
                message_placeholder.markdown(response)

                # Display the image if it exists
                if image_path and os.path.exists(image_path):
                    st.image(image_path)

        # Add assistant response to history
        message_data = {"role": "assistant", "content": response}
        if image_path and os.path.exists(image_path):
            message_data["image"] = image_path

        st.session_state.messages.append(message_data)


if __name__ == "__main__":
    main()