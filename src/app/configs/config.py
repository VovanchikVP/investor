from pydantic import BaseSettings


class Settings(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = True
    ROOT_PATH: str = ""


settings = Settings()
