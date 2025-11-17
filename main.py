# 2025/11/16
# zhangzhong
# https://developers.llamaindex.ai/python/framework/getting_started/starter_example/
# https://developers.llamaindex.ai/python/framework/getting_started/starter_example_local/

import asyncio
from llama_index.core.agent.workflow import FunctionAgent, AgentWorkflow
from llama_index.core.workflow import Context
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from langchain_community.embeddings import ZhipuAIEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding


# from llama_index.llms.openai import OpenAI
# from llama_index.llms.zhipuai import ZhipuAI
from llama_index.llms.deepseek import DeepSeek
import os

# 我们已经设置了vscode读取.env, 如果没有出现你想要的环境变量
# 可以重新启动一个shell，会读取.env文件
bigmodel_api_key = os.environ.get("BIGMODEL_API_KEY")
deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY")
assert bigmodel_api_key is not None, (
    "Please set the BIGMODEL_API_KEY environment variable."
)
assert deepseek_api_key is not None, (
    "Please set the DEEPSEEK_API_KEY environment variable."
)

# Now we can create a tool for searching through documents using LlamaIndex.
# By default, our VectorStoreIndex will use a text-embedding-ada-002 embeddings from OpenAI to embed and retrieve the text.

# Settings control global defaults
# Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
# Settings.llm = Ollama(
#     model="llama3.1",
#     request_timeout=360.0,
#     # Manually set the context window to limit memory usage
#     context_window=8000,
# )
# 我要怎么使用一个embedding模型呢？我记得zhipu这边是有的
# https://developers.llamaindex.ai/python/examples/embeddings/langchain/
# https://docs.langchain.com/oss/python/integrations/text_embedding/zhipuai
# 曲线救国，llama index支持langchain的embedding模型，那我就用langchain的zhipuai embedding模型
embeddings = ZhipuAIEmbeddings(
    model="embedding-3",
    api_key=bigmodel_api_key,
    # With the `embedding-3` class
    # of models, you can specify the size
    # of the embeddings you want returned.
    # dimensions=1024
)
embed_model = LangchainEmbedding(embeddings)

# llm = llm = ZhipuAI(model="glm-4", api_key=api_key)
llm = DeepSeek(model="deepseek-chat", api_key=deepseek_api_key)

# Settings control global defaults
Settings.embed_model = embed_model
Settings.llm = llm


# Create a RAG tool using LlamaIndex
# documents = SimpleDirectoryReader("data").load_data()
# index = VectorStoreIndex.from_documents(
#     documents,
#     # we can optionally override the embed_model here
#     # embed_model=Settings.embed_model,
# )
# query_engine = index.as_query_engine(
#     # we can optionally override the llm here
#     # llm=Settings.llm,
# )

# Store index on disk
# Save the index
# index.storage_context.persist("storage")

storage_context = StorageContext.from_defaults(persist_dir="storage")
index = load_index_from_storage(
    storage_context,
    # we can optionally override the embed_model here
    # it's important to use the same embed_model as the one used to build the index
    # embed_model=Settings.embed_model,
)
query_engine = index.as_query_engine(
    # we can optionally override the llm here
    # llm=Settings.llm,
)


# Define a simple calculator tool
# As you can see, these are regular Python functions. 
# When deciding what tool to use, your agent will use the tool’s name, parameters, 
# and docstring to determine what the tool does and whether it’s appropriate for the task at hand.
# So it’s important to make sure the docstrings are descriptive and helpful. 
# It will also use the type hints to determine the expected parameters and return type.
def multiply(a: float, b: float) -> float:
    return a * b


async def search_documents(query: str) -> str:
    """Useful for answering natural language questions about an personal essay written by Paul Graham."""
    response = await query_engine.aquery(query)
    return str(response)


# Adding Chat History
# The AgentWorkflow is also able to remember previous messages. This is contained inside the Context of the AgentWorkflow.
# If the Context is passed in, the agent will use it to continue the conversation.

# Create an agent workflow with our calculator tool
# agent = FunctionAgent(
#     tools=[multiply],
#     llm=llm,
#     system_prompt="You are a helpful assistant that can multiply two numbers.",
# )

# Create an enhanced workflow with both tools
agent = AgentWorkflow.from_tools_or_functions(
    [multiply, search_documents],
    llm=Settings.llm,
    system_prompt="""You are a helpful assistant that can perform calculations
    and search through documents to answer questions.""",
)

# create context
ctx = Context(agent)


async def main():
    # Run the agent
    # should return 52.5
    response = await agent.run(user_msg="What is 12.5 multiplied by 4.2?")
    # response : 12.5 multiplied by 4.2 equals 52.5.
    print(response)

    # run agent with context
    response = await agent.run("My name is Logan", ctx=ctx)
    response = await agent.run("What is my name?", ctx=ctx)
    print(response)

    response = await agent.run("What did the author do in college? Also, what's 7 * 8?")
    print(response)


# Execute the main function
if __name__ == "__main__":
    asyncio.run(main())
