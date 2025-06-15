from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.language_models.chat_models import BaseChatModel
from dotenv import load_dotenv

load_dotenv()

GPT_4O_MINI = ChatOpenAI(model="gpt-4o-mini")
LLAMA_3_8B_8192 = ChatGroq(model="llama3-8b-8192")

llms = {
    "gpt-4o-mini": GPT_4O_MINI,
    "llama3-8b-8192": LLAMA_3_8B_8192,
}


def get_llm(model_name: str) -> BaseChatModel:
    return llms[model_name]
