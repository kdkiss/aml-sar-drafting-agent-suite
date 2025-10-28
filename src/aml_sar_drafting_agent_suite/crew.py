from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from crewai_tools import BraveSearchTool
from aml_sar_drafting_agent_suite.tools.baseline_comparator import BaselineComparatorTool

@CrewBase
class AmlSarDraftingAgentSuite():
    """
    AML SAR Drafting Agent Suite - A specialized CrewAI crew for analyzing suspicious 
    financial activity and drafting regulatory-compliant Suspicious Activity Reports (SARs).
    
    This crew orchestrates four specialized agents that work together to:
    1. Analyze transaction patterns for suspicious activity indicators
    2. Research applicable AML/BSA regulations and guidance
    3. Draft examination-ready SAR narratives
    4. Perform quality assurance review before submission
    """

    # Type hints for CrewAI framework - automatically populated by decorators
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def transaction_analyst(self) -> Agent:
        """
        Creates the Transaction Analyst agent responsible for identifying suspicious 
        activity patterns and quantifying deviations from baseline behavior.
        
        Tools:
        - BaselineComparatorTool: Compares current activity against historical and peer baselines
        """
        return Agent(
            config=self.agents_config['transaction_analyst'], # YAML config from agents.yaml
            verbose=True,
            tools=[
                BaselineComparatorTool()  # Custom tool for behavioral analysis
            ]
        )

    @agent
    def regulatory_researcher(self) -> Agent:
        """
        Creates the Regulatory Researcher agent responsible for identifying applicable
        AML/BSA regulations, FinCEN guidance, and current typologies.
        
        Tools:
        - BraveSearchTool: Searches for current regulatory guidance and advisories
        """
        return Agent(
            config=self.agents_config['regulatory_researcher'], # YAML config from agents.yaml
            verbose=True,
            tools=[
                BraveSearchTool()  # External search for regulatory updates
            ]
        )

    @agent
    def narrative_drafter(self) -> Agent:
        """
        Creates the Narrative Drafter agent responsible for drafting examination-ready
        SAR narratives using the five essential elements (who, what, when, where, why).
        
        No external tools - relies on analysis from previous agents and regulatory knowledge.
        """
        return Agent(
            config=self.agents_config['narrative_drafter'], # YAML config from agents.yaml
            verbose=True
        )

    @agent
    def quality_reviewer(self) -> Agent:
        """
        Creates the Quality Reviewer agent responsible for comprehensive QA review
        to ensure SAR meets regulatory standards and examination readiness.
        
        No external tools - performs quality assessment based on regulatory criteria.
        """
        return Agent(
            config=self.agents_config['quality_reviewer'], # YAML config from agents.yaml
            verbose=True
        )

    @task
    def analyze_transactions(self) -> Task:
        """
        Task 1: Analyze transaction data to identify suspicious activity patterns.
        
        Uses BaselineComparatorTool to quantify deviations from normal behavior.
        Outputs: Structured transaction analysis report with red flags and metrics.
        """
        return Task(
            config=self.tasks_config['analyze_transactions'], # YAML config from tasks.yaml
        )

    @task
    def research_regulations(self) -> Task:
        """
        Task 2: Research applicable regulations and guidance for the identified activity type.
        
        Depends on: analyze_transactions (uses activity type and patterns)
        Outputs: Regulatory compliance brief with citations and requirements.
        """
        return Task(
            config=self.tasks_config['research_regulations'], # YAML config from tasks.yaml
        )

    @task
    def draft_sar_narrative(self) -> Task:
        """
        Task 3: Draft examination-ready SAR narrative using five essential elements.
        
        Depends on: analyze_transactions, research_regulations
        Outputs: Complete SAR narrative ready for regulatory submission.
        """
        return Task(
            config=self.tasks_config['draft_sar_narrative'], # YAML config from tasks.yaml
        )

    @task
    def review_sar_quality(self) -> Task:
        """
        Task 4: Perform comprehensive quality assurance review of the SAR package.
        
        Depends on: All previous tasks
        Outputs: QA report with pass/fail determination and enhancement recommendations.
        """
        return Task(
            config=self.tasks_config['review_sar_quality'], # YAML config from tasks.yaml
        )

    @crew
    def crew(self) -> Crew:
        """
        Creates and configures the AML SAR Drafting crew with sequential task execution.
        
        Process Flow:
        1. Transaction Analyst analyzes suspicious patterns
        2. Regulatory Researcher identifies applicable regulations  
        3. Narrative Drafter creates examination-ready SAR
        4. Quality Reviewer performs final QA assessment
        
        Returns:
            Crew: Configured crew ready for SAR analysis and drafting
        """
        return Crew(
            agents=self.agents, # All agents created by @agent decorators
            tasks=self.tasks,   # All tasks created by @task decorators
            process=Process.sequential, # Tasks execute in dependency order
            verbose=True,       # Enable detailed execution logging
        )
