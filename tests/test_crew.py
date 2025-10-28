import pytest
from unittest.mock import Mock, patch
from aml_sar_drafting_agent_suite.crew import AmlSarDraftingAgentSuite


class TestAmlSarDraftingAgentSuite:
    
    def test_crew_initialization(self):
        """Test that crew initializes without errors"""
        crew_suite = AmlSarDraftingAgentSuite()
        assert crew_suite is not None
    
    def test_agents_creation(self):
        """Test that all agents are created"""
        crew_suite = AmlSarDraftingAgentSuite()
        
        # Mock the config to avoid file dependencies
        crew_suite.agents_config = {
            'transaction_analyst': {'role': 'test', 'goal': 'test', 'backstory': 'test'},
            'regulatory_researcher': {'role': 'test', 'goal': 'test', 'backstory': 'test'},
            'narrative_drafter': {'role': 'test', 'goal': 'test', 'backstory': 'test'},
            'quality_reviewer': {'role': 'test', 'goal': 'test', 'backstory': 'test'}
        }
        
        assert crew_suite.transaction_analyst() is not None
        assert crew_suite.regulatory_researcher() is not None
        assert crew_suite.narrative_drafter() is not None
        assert crew_suite.quality_reviewer() is not None
    
    def test_tasks_creation(self):
        """Test that all tasks are created"""
        crew_suite = AmlSarDraftingAgentSuite()
        
        # Mock the config
        crew_suite.tasks_config = {
            'analyze_transactions': {'description': 'test', 'expected_output': 'test'},
            'research_regulations': {'description': 'test', 'expected_output': 'test'},
            'draft_sar_narrative': {'description': 'test', 'expected_output': 'test'},
            'review_sar_quality': {'description': 'test', 'expected_output': 'test'}
        }
        
        assert crew_suite.analyze_transactions() is not None
        assert crew_suite.research_regulations() is not None
        assert crew_suite.draft_sar_narrative() is not None
        assert crew_suite.review_sar_quality() is not None
    
    @patch('aml_sar_drafting_agent_suite.crew.Crew')
    def test_crew_creation(self, mock_crew):
        """Test that crew is created with correct parameters"""
        crew_suite = AmlSarDraftingAgentSuite()
        crew_suite.agents = []
        crew_suite.tasks = []
        
        crew_suite.crew()
        
        mock_crew.assert_called_once()
        call_args = mock_crew.call_args[1]
        assert 'agents' in call_args
        assert 'tasks' in call_args
        assert 'verbose' in call_args