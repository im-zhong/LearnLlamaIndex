# 2025/12/1
# zhangzhong
# https://llamahub.ai/l/readers/llama-index-readers-file?from=readers


from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import DocxReader


# 结果用的还是docx2txt,
# 不行啊，图片也解析不出来！
def test_docx_loader() -> None:
    # Docx Reader example
    parser = DocxReader()
    file_extractor = {".docx": parser}
    documents = SimpleDirectoryReader(
        "./data", file_extractor=file_extractor
    ).load_data()
    print(len(documents))
    print(documents)
