# 2025/11/17
# zhangzhong

# 模型和embedding的话写一个工厂函数先

from langchain_community.embeddings import ZhipuAIEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding

# from langchain_community.chat_models import ChatZhipuAI
from llama_index.llms.deepseek import DeepSeek

# 引入这个就会出错？why？？？
# llama index用的是浪chain < 0.1 版本的langchain
# 而我们用的是langchian 1.x 所以不对，服了。。。
# from llama_index.llms.langchain import LangChainLLM
from llama_index.llms.openai_like import (
    OpenAILike,
)  # 看看我发现了什么！这个应该可以用！还是不行。。。有BUG
from llama_index.llms.zhipuai import ZhipuAI


def get_deepseek(model_name: str, deepseek_api_key: str) -> DeepSeek:
    llm = DeepSeek(model=model_name, api_key=deepseek_api_key)
    return llm


def get_bigmodel_llm(model_name: str, bigmodel_api_key: str):
    # chat = OpenAILike(
    #     model=model_name,
    #     api_key=bigmodel_api_key,
    #     api_base="https://open.bigmodel.cn/api/paas/v4/chat/",
    # )
    chat = ZhipuAI(
        model=model_name,
        api_key=bigmodel_api_key,
        # api_base="https://open.bigmodel.cn/api/paas/v4/chat/",
    )
    return chat


def get_llm(model_name: str, api_key: str):
    if model_name.startswith("deepseek"):
        return get_deepseek(model_name, api_key)
    elif model_name.startswith("glm") or model_name.startswith("bigmodel"):
        return get_bigmodel_llm(model_name, api_key)
    else:
        raise ValueError(f"Unsupported model name: {model_name}")


# def get_glm_llm(api_key: str):
#     pass


def get_glm_embedding(bigmodel_api_key: str) -> LangchainEmbedding:
    embeddings = ZhipuAIEmbeddings(
        model="embedding-3",
        api_key=bigmodel_api_key,
        # With the `embedding-3` class
        # of models, you can specify the size
        # of the embeddings you want returned.
        # dimensions=1024
    )
    embed_model = LangchainEmbedding(embeddings)
    return embed_model
