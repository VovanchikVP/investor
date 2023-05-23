from pydantic import BaseSettings


class Settings(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = True
    ROOT_PATH: str = ""
    DB_USER: str = "investor"
    DB_PASSWORD: str = "investor"
    DB_HOST: str = "localhost:5433"
    DB_NAME: str = "investor"


settings = Settings()
