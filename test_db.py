from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:Aegis123@localhost:5432/aegisai"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("✅ SUCCESS")
except Exception as e:
    print("❌ ERROR")
    print(e)