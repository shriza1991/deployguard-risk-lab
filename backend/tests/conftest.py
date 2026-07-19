import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ["DATABASE_URL"] = "postgresql:///./test-risklab.db"
os.environ["JWT_SECRET_KEY"] = "test-only-secret-with-sufficient-length"

from app.main import app  # noqa: E402


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)

