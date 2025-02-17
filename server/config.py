from decouple import config
from pydantic import BaseModel

class Settings(BaseModel):
    "Server Config Class"

    root_url: str = config("ROOT_URL", default="http://localhost:8000")
    mongo_uri: str = config("MONGODB_URL")

CONFIG = Settings()