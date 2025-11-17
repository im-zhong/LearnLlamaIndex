# 2025/11/17
# zhangzhong

# 写一个settings全局对象，可以简单的获取api key就足够了
import os
from pydantic import BaseModel


class Settings(BaseModel):
    bigmodel_api_key: str = os.environ.get("BIGMODEL_API_KEY", "")
    deepseek_api_key: str = os.environ.get("DEEPSEEK_API_KEY", "")

    class Config:
        env_file = ".env"


settings = Settings()
