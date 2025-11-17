from learn.settings import settings


def test_settings():
    assert settings.bigmodel_api_key != ""
    assert settings.deepseek_api_key != ""
