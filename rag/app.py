import logging
import time
import streamlit as st
from bot import RAGAgent
import utils

st.set_page_config(
    page_title="Interactive RAG Bot 🤖",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s.%(msecs)04d %(levelname)s {%(module)s} [%(funcName)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@st.cache_resource
def get_agent():
    logger.info("Loading RAG Bot ...")
    return RAGAgent(logger, st)


st.title("🤖 Interactive RAG Bot")
st.markdown(
    """
    Build and interact with your RAG pipeline in real-time.
    Powered by **MongoDB Atlas** and **ActionWeaver**.
    """
)
st.divider()

agent = get_agent()

with st.sidebar:
    st.header("About")
    st.info(
        """
        This bot can:
        - 🔍 **Answer questions** using its knowledge base.
        - 🌐 **Search the web** if it doesn't know the answer.
        - 📚 **Learn from URLs** (just paste them!).
        - ⚙️ **Configure RAG** settings on the fly.
        """
    )

    st.header("Settings")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        agent.messages = agent.init_messages
        st.rerun()

    st.header("Current RAG Config")
    st.json(agent.rag_config)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input(placeholder="Ask a question, add a URL, or configure RAG..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    utils.format_and_print_user_input(prompt)
    response = agent(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        if type(response) == str:
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
