import pytest
import json
from unittest.mock import patch, mock_open
from aml_sar_drafting_agent_suite.tools.baseline_comparator import BaselineComparatorTool


class TestBaselineComparatorTool:
    
    def test_tool_initialization(self):
        """Test tool initializes correctly"""
        tool = BaselineComparatorTool()
        assert tool.name == "behavioral_baseline_comparator"
        assert "baseline" in tool.description.lower()
    
    def test_extract_account_number(self):
        """Test account number extraction"""
        tool = BaselineComparatorTool()
        
        text = "Customer: John Smith (Account #123-456-789)"
        result = tool._extract_account_number(text)
        assert result == "123-456-789"
        
        text_no_account = "Customer: John Smith"
        result = tool._extract_account_number(text_no_account)
        assert result is None
    
    def test_extract_business_name(self):
        """Test business name extraction"""
        tool = BaselineComparatorTool()
        
        text = "Business Name: Rodriguez Import Export LLC"
        result = tool._extract_business_name(text)
        assert result == "Rodriguez Import Export LLC"
        
        text_alt = "Customer: Maria Rodriguez (Account #789) Rodriguez Import Export LLC"
        result = tool._extract_business_name(text_alt)
        assert result == "Rodriguez Import Export LLC"
    
    @patch("builtins.open", new_callable=mock_open, read_data='{"test_key": {"customer_baseline": {"cash_monthly": 5000}}}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_baseline(self, mock_exists, mock_file):
        """Test baseline loading from file"""
        tool = BaselineComparatorTool()
        result = tool._load_baseline("test_key")
        assert result == {"customer_baseline": {"cash_monthly": 5000}}
    
    def test_percentage_calculation(self):
        """Test percentage calculation"""
        tool = BaselineComparatorTool()
        
        # Normal case
        result = tool._pct(150, 100)
        assert result == 50.0
        
        # Zero baseline
        result = tool._pct(100, 0)
        assert result is None
        
        # None baseline
        result = tool._pct(100, None)
        assert result is None
    
    @patch("builtins.open", new_callable=mock_open, read_data='{}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_run_no_baseline(self, mock_exists, mock_file):
        """Test tool execution with no baseline data"""
        tool = BaselineComparatorTool()
        
        transaction_data = "Customer: Test Customer (Account #123)"
        current_metrics = {"cash_monthly": 10000}
        
        result = tool._run(transaction_data, current_metrics)
        result_dict = json.loads(result)
        
        assert result_dict["resolved_key"] == "123"
        assert result_dict["has_baseline"] is False
        assert "metrics" in result_dict