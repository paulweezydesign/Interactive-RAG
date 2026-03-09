import sys
import os
import time
import unittest
from unittest.mock import MagicMock, patch

# Add the rag directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rag')))

# Mock dependencies for testing in restricted environments
sys.modules['actionweaver'] = MagicMock()
sys.modules['actionweaver.llms.azure.chat'] = MagicMock()
sys.modules['actionweaver.llms.openai.tools.chat'] = MagicMock()
sys.modules['actionweaver.llms.openai.functions.tokens'] = MagicMock()
sys.modules['langchain.vectorstores'] = MagicMock()
sys.modules['langchain.embeddings'] = MagicMock()
sys.modules['langchain.document_loaders'] = MagicMock()
sys.modules['langchain.text_splitter'] = MagicMock()
sys.modules['selenium'] = MagicMock()
sys.modules['selenium.webdriver.chrome.options'] = MagicMock()
sys.modules['bs4'] = MagicMock()

class MockDoc:
    def __init__(self, content):
        self.page_content = content

class TestRAGAgentPerformance(unittest.TestCase):
    @patch('bot.OpenAIChatCompletion')
    @patch('bot.GPT4AllEmbeddings')
    @patch('bot.pymongo.MongoClient')
    @patch('bot.webdriver.Chrome')
    def test_summarize_chunks_parallel(self, mock_chrome, mock_mongo, mock_embeddings, mock_llm):
        from bot import RAGAgent
        st_mock = MagicMock()
        logger_mock = MagicMock()
        agent = RAGAgent(logger_mock, st_mock)

        # Mock LLM to simulate a delay
        def mock_create(*args, **kwargs):
            time.sleep(0.1) # Simulate 100ms LLM call
            return "Summary"

        agent.llm.create = mock_create

        docs = [MockDoc(f"Content {i}") for i in range(10)]

        start_time = time.time()
        agent.summarize_chunks(docs)
        end_time = time.time()

        duration = end_time - start_time
        # In parallel, 10 chunks with 0.1s delay should take much less than 1.0s
        self.assertLess(duration, 0.5)

if __name__ == "__main__":
    unittest.main()
