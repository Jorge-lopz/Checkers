from dotenv import load_dotenv
import os

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_URL = f"postgresql://postgres:{DB_PASSWORD}@db.cldyxcdaelouqxjnkolv.supabase.co:5432/postgres"

print(f"\nDB Password: {DB_PASSWORD}")
print(f"Database URL: {DATABASE_URL}")
