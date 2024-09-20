# Import the required libraries
import streamlit as st
from phi.assistant import Assistant
from phi.tools.hackernews import HackerNews
from phi.llm.openai import OpenAIChat

# Set up the Streamlit app
st.title("HackerNews Story and User Researcher 🌐📰")
st.caption("This app allows you to research top stories and users on HackerNews using the phi assistant.")

# Get OpenAI API key from user
openai_api_key = st.text_input("OpenAI API Key", type="password")

if openai_api_key:
    # Create instances of the Assistant
    story_researcher = Assistant(
        name="HackerNews Story Researcher",
        role="Researches hackernews stories and users.",
        tools=[HackerNews()],
    )

    user_researcher = Assistant(
        name="HackerNews User Researcher",
        role="Reads articles from URLs.",
        tools=[HackerNews()],
    )

    hn_assistant = Assistant(
        name="HackerNews Team",
        team=[story_researcher, user_researcher],
        llm=OpenAIChat(
            model="gpt-3.5-turbo",
            max_tokens=1024,
            temperature=0.5,
            api_key=openai_api_key
        )
    )

    # Input field for the report query
    query = st.text_input("Enter your report query")

    if query:
        # Get the response from the assistant
        response = hn_assistant.run(query, stream=False)
        st.write(response)
