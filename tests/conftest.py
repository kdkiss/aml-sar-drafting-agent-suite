import pytest
import os
from unittest.mock import patch


@pytest.fixture
def sample_transaction_data():
    """Sample transaction data for testing"""
    return {
        "transaction_data": "Customer: Test Customer (Account #123-456-789)",
        "customer_profile": "Test customer profile",
        "alert_details": "Test alert details",
        "activity_type": "Structuring"
    }


@pytest.fixture
def mock_env_vars():
    """Mock environment variables"""
    with patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test-key',
        'INPUT_FILE': 'test_input.json'
    }):
        yield