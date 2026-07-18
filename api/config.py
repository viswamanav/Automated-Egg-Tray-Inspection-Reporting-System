import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:admin123@localhost:5432/egg_db"
)
MODEL_PATH = os.getenv(
    "MODEL_PATH",
    r"weights\best.pt"
)
EXPECTED_EGGS = int(
    os.getenv("EXPECTED_EGGS", "25")
)
CONFIDENCE = float(
    os.getenv("CONFIDENCE", "0.50")
)
