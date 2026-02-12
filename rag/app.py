import logging
import time
import streamlit as st
from bot import RAGAgent
import utils

st.set_page_config(layout="wide", page_title="RAG Agent")

logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s.%(msecs)04d %(levelname)s {%(module)s} [%(funcName)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_agent():
    if "agent" not in st.session_state:
        logger.info("Loading RAG Bot ...")
        st.session_state.agent = RAGAgent(logger, st)
    return st.session_state.agent


agent = get_agent()

with st.sidebar:
    st.title("🤖 RAG Agent")
    st.markdown("---")
    st.markdown(
        """
        ### 💡 How to use
        - **🔍 Search**: "Search the web for..."
        - **📚 Learn**: "Learn https://example.com"
        - **💬 Ask**: "What is MongoDB Atlas?"
        - **⚙️ Config**: "Change chunk size to 500"
        """
    )
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.agent.messages = st.session_state.agent.init_messages
        st.rerun()

st.title("Interactive RAG")
st.caption("Powered by MongoDB and ActionWeaver")
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input(
    placeholder="Ask a question, search the web, or provide a URL to learn..."
):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    utils.format_and_print_user_input(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        with st.status("Thinking...", expanded=True) as status:
            response = agent(prompt)
            status.update(label="Thinking... Done!", state="complete", expanded=False)

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
                message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)

            agent.messages.append({"role": "assistant", "content": full_response})
            utils.format_and_print_genai_response(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
