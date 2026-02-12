import logging
import time
import streamlit as st
from bot import RAGAgent
import utils

st.set_page_config(layout="wide", page_title="Interactive RAG Agent", page_icon="🤖")

logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s.%(msecs)04d %(levelname)s {%(module)s} [%(funcName)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Initialize RAG Agent in session state for session isolation
if "agent" not in st.session_state:
    with st.status("Initializing RAG Agent...", expanded=True) as status:
        st.session_state.agent = RAGAgent(logger, st)
        status.update(label="RAG Agent Ready!", state="complete", expanded=False)

agent = st.session_state.agent

# Sidebar with utility functions
with st.sidebar:
    st.title("🤖 RAG Settings")
    st.markdown("---")
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        if "agent" in st.session_state:
            st.session_state.agent.messages = st.session_state.agent.init_messages
        st.rerun()
    st.markdown("---")
    st.info(
        "This agent uses MongoDB and ActionWeaver to provide interactive RAG capabilities."
    )

# Main interface title
st.title("🤖 Interactive RAG Agent")
st.caption("Build and interact with your RAG pipeline in real-time")
st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input(
    placeholder="Ask a question, add a URL (e.g. 'learn https://...'), or search the web..."
):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    utils.format_and_print_user_input(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.status("Thinking...") as status:
            response = agent(prompt)
            status.update(label="Response ready!", state="complete", expanded=False)
        message_placeholder = st.empty()
        full_response = ""

        if isinstance(response, str):
            utils.print_log("Received string response")
            assistant_response = response

            full_response += assistant_response + " "

            # Simulate stream of response with milliseconds delay
            # for chunk in assistant_response.split():
            #     full_response += chunk + " "
            #     time.sleep(0.05)
            #     # Add a blinking cursor to simulate typing
            #     message_placeholder.markdown(full_response + "▌")
            agent.messages.append({"role": "assistant", "content": response})
            message_placeholder.markdown(full_response, unsafe_allow_html=True)
            utils.format_and_print_genai_response(full_response)
        else:
            utils.print_log("Received stream response")
            for chunk in response:
                if isinstance(chunk, str):
                    full_response += chunk
                    time.sleep(0.05)
                elif chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content

                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(
                    full_response + "▌", unsafe_allow_html=True
                )

            agent.messages.append({"role": "assistant", "content": full_response})
            utils.format_and_print_genai_response(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
