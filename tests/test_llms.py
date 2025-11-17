# 2025/11/17
# zhangzhong
# https://developers.llamaindex.ai/python/framework/understanding/using_llms/


from llama_index.core.llms import ChatMessage, ChatResponse, TextBlock, ImageBlock
from learn.model import get_llm
from learn.settings import settings
from llama_index.core.tools import FunctionTool


MODEL_NAME = "glm-4"
API_KEY = settings.bigmodel_api_key


def test_llm_complete() -> None:
    llm = get_llm(MODEL_NAME, API_KEY)
    response = llm.complete("Hello, how are you?")
    print(response)


async def test_llm_async_complete() -> None:
    llm = get_llm(MODEL_NAME, API_KEY)
    response = await llm.acomplete("Hello, how are you?")
    print(response)


def test_llm_stream_complete() -> None:
    llm = get_llm(MODEL_NAME, API_KEY)

    for chunk in llm.stream_complete("Tell me a story about a brave knight."):
        print(chunk.delta, end="", flush=True)


async def test_llm_async_stream_complete() -> None:
    llm = get_llm(MODEL_NAME, API_KEY)

    # asynchronous iterator (generator)
    # async astream_complete(*args, **kwargs) -> AsyncGenerator[CompletionResponse, None]
    # 我知道为什么不对了，因为async for需要in后面是一个AsyncGenerator
    # 但是deepseek的astream_complete返回的一个coroutine，必须await之后才能得到一个AsyncGenerator
    handle = await llm.astream_complete("Tell me a story about a brave knight.")

    async for chunk in handle:
        print(chunk.delta, end="", flush=True)


# 大模型的chat api和complete api有什么区别呢？check the Completion_Chat_API.md
# The LLM class also implements a chat method, which allows you to have more sophisticated interactions:
def test_llm_chat() -> None:
    messages = [
        ChatMessage(role="system", content="You are a helpful assistant."),
        ChatMessage(role="user", content="Tell me a joke."),
    ]
    llm = get_llm(MODEL_NAME, API_KEY)
    chat_response: ChatResponse = llm.chat(messages)
    print(chat_response)


async def test_llm_async_chat() -> None:
    messages = [
        ChatMessage(role="system", content="You are a helpful assistant."),
        ChatMessage(role="user", content="Tell me a joke."),
    ]
    llm = get_llm(MODEL_NAME, API_KEY)
    chat_response: ChatResponse = await llm.achat(messages)
    print(chat_response)


def test_llm_stream_chat() -> None:
    messages = [
        ChatMessage(role="system", content="You are a helpful assistant."),
        ChatMessage(role="user", content="Tell me a story about a brave knight."),
    ]
    llm = get_llm(MODEL_NAME, API_KEY)

    for chunk in llm.stream_chat(messages):
        print(chunk.delta, end="", flush=True)


async def test_llm_async_stream_chat() -> None:
    messages = [
        ChatMessage(role="system", content="You are a helpful assistant."),
        ChatMessage(role="user", content="Tell me a story about a brave knight."),
    ]
    llm = get_llm(MODEL_NAME, API_KEY)

    handle = await llm.astream_chat(messages)

    async for chunk in handle:
        print(chunk.delta, end="", flush=True)


# 咱这边应该也可以找到一个多模态的模型吧，比如zhipu的模型，不过llama index不支持啊，看看有没又类似langchianembedding的langchain llm吧
# https://developers.llamaindex.ai/python/examples/llm/langchain/
# 惊了！真的有，哈哈哈
# Multi-Modal LLMs
# llm = OpenAI(model="gpt-4o")

# messages = [
#     ChatMessage(
#         role="user",
#         blocks=[
#             ImageBlock(path="image.png"),
#             TextBlock(text="Describe the image in a few sentences."),
#         ],
#     )
# ]


# resp = llm.chat(messages)
# print(resp.message.content)
# langchain也是支持的。llama index用起来还是太费劲了
def test_multimodal_llm_chat() -> None:
    messages = [
        ChatMessage(
            role="user",
            blocks=[
                ImageBlock(path="image.png"),
                TextBlock(text="Describe the image in a few sentences."),
            ],
        )
    ]
    # TIPs: 看起来应该是API的格式是不对的，最新的zhipuai需要zai这个包，但是llamaindex里面的包应该很久没有更新过了
    llm = get_llm("glm-4.5v", API_KEY)
    chat_response: ChatResponse = llm.chat(messages)
    print(chat_response)


# 这个也不行。。。
# def test_llm_tool_calling() -> None:
#     # Tool Calling
#     def generate_song(name: str, artist: str) -> dict:
#         """Generates a song with provided name and artist."""
#         return {"name": name, "artist": artist}

#     tool = FunctionTool.from_defaults(fn=generate_song)

#     llm = get_llm("deepseek-chat", settings.deepseek_api_key)
#     response = llm.predict_and_call(
#         [tool],
#         "Pick a random song for me, Use the tool.",
#     )
#     print(response)
