from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    
    
@dataclass
class Postgres:
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    
    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    
@dataclass
class Config:
    tg_bot: TgBot
    postgres: Postgres


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(
                      token=env('BOT_TOKEN'),
                    ),
                  postgres=Postgres(
                      DB_HOST=env('DB_HOST'),
                      DB_PORT=env('DB_PORT'),
                      DB_USER=env('DB_USER'),
                      DB_PASS=env('DB_PASS'),
                      DB_NAME=env('DB_NAME'),
                    ),
                  )

# Загружаем конфиг в переменную config
settings: Config = load_config()