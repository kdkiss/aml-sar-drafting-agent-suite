import pytest
import json
from unittest.mock import patch, mock_open, MagicMock
from aml_sar_drafting_agent_suite.main import load_inputs, run, train, test


class TestMain:
    
    @patch("builtins.open", new_callable=mock_open, read_data='{"test": "data"}')
    def test_load_inputs_success(self, mock_file):
        """Test successful input loading"""
        result = load_inputs("test.json")
        assert result == {"test": "data"}
    
    def test_load_inputs_file_not_found(self):
        """Test input loading with missing file"""
        with pytest.raises(Exception) as exc_info:
            load_inputs("nonexistent.json")
        assert "Input file not found" in str(exc_info.value)
    
    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    def test_load_inputs_invalid_json(self, mock_file):
        """Test input loading with invalid JSON"""
        with pytest.raises(Exception) as exc_info:
            load_inputs("invalid.json")
        assert "Error parsing JSON file" in str(exc_info.value)
    
    @patch('aml_sar_drafting_agent_suite.main.load_inputs')
    @patch('aml_sar_drafting_agent_suite.main.AmlSarDraftingAgentSuite')
    def test_run_success(self, mock_crew_class, mock_load_inputs):
        """Test successful crew run"""
        mock_load_inputs.return_value = {"test": "data"}
        mock_crew_instance = MagicMock()
        mock_crew_class.return_value.crew.return_value = mock_crew_instance
        
        run()
        
        mock_load_inputs.assert_called_once()
        mock_crew_instance.kickoff.assert_called_once_with(inputs={"test": "data"})
    
    @patch('aml_sar_drafting_agent_suite.main.load_inputs')
    @patch('aml_sar_drafting_agent_suite.main.AmlSarDraftingAgentSuite')
    def test_train_success(self, mock_crew_class, mock_load_inputs):
        """Test successful crew training"""
        mock_load_inputs.return_value = {"test": "data"}
        mock_crew_instance = MagicMock()
        mock_crew_class.return_value.crew.return_value = mock_crew_instance
        
        with patch('sys.argv', ['main.py', '3', 'test.pkl']):
            train()
        
        mock_crew_instance.train.assert_called_once_with(
            n_iterations=3,
            filename='test.pkl',
            inputs={"test": "data"}
        )
    
    @patch('aml_sar_drafting_agent_suite.main.load_inputs')
    @patch('aml_sar_drafting_agent_suite.main.AmlSarDraftingAgentSuite')
    def test_test_success(self, mock_crew_class, mock_load_inputs):
        """Test successful crew testing with mocked sys.argv"""
        mock_load_inputs.return_value = {"test": "data"}
        mock_crew_instance = MagicMock()
        mock_crew_instance.test.return_value = "test_result"
        mock_crew_class.return_value.crew.return_value = mock_crew_instance
        
        with patch('sys.argv', ['main.py', '2', 'gpt-4']):
            result = test()
        
        assert result == "test_result"
        mock_crew_instance.test.assert_called_once_with(
            n_iterations=2,
            openai_model_name='gpt-4',
            inputs={"test": "data"}
        )