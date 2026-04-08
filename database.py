# database.py

from sqlalchemy import create_engine
from urllib.parse import quote_plus

# 🔹 UPDATE THESE VALUES
DB_USER = "root"
DB_PASSWORD = "Sudheer@0099123"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "retail_db"

# 🔹 CREATE ENGINE
_enc_password = quote_plus(DB_PASSWORD)

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{_enc_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def get_engine():
    return engine