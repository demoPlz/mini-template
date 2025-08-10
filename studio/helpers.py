import os

from langchain_openai import ChatOpenAI, AzureChatOpenAI
from openai import OpenAI, AzureOpenAI

from dotenv import load_dotenv
load_dotenv()     

def get_llm(**kw):
    """
    Return a Chat‑compatible LLM whose backend (OpenAI, Azure, local stub…)
    is selected by env‑vars.  Extra **kw flow through so nodes can override
    temperature, max_tokens, etc. without knowing the backend.

    Mini challenge evaluation server uses azure openai to run your submission.
    You don't need to fill in the azure openai endpoint and api key, 
    but you need to fill in the openai api key and model name to run locally.
    """
    provider = os.getenv("LLM_PROVIDER", "openai")

    if provider.lower() == "azure":
        return AzureChatOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key       =os.environ["AZURE_OPENAI_API_KEY"],
            deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT", "gpt-4o"], # For submission, the default value is always gpt-4o, but you can choose from o1, o3 and o4-mini too.
            api_version   =os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
            **kw,
        )
    elif provider.lower() == "local-echo":
        from langchain.llms.fake import FakeListLLM
        return FakeListLLM(responses=["This is a stub."])  
    else:  
        return ChatOpenAI(
            api_key =os.getenv("OPENAI_API_KEY"),
            model_name=os.getenv("OPENAI_MODEL", "gpt-4o"),
            **kw,
        )