import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

CURRENT_DATABASE = os.getenv("CURRENT_DATABASE")
SQLITE_DATABASE_PATH = os.getenv("SQLITE_DATABASE_PATH", "database.db")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

if CURRENT_DATABASE == "sqlite":
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_DATABASE_PATH}"
elif CURRENT_DATABASE == "mysql":
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USERNAME}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
elif CURRENT_DATABASE == "postgresql":
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USERNAME}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"