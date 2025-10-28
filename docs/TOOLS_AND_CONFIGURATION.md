# Tools and Configuration Documentation

## BaselineComparatorTool

### Overview
Custom CrewAI tool for comparing customer transaction metrics against historical and peer baselines to identify suspicious deviations.

### Usage
```python
from aml_sar_drafting_agent_suite.tools.baseline_comparator import BaselineComparatorTool

tool = BaselineComparatorTool()
result = tool._run(
    transaction_data="Customer: John Smith (Account #123-456-789)...",
    current_metrics={
        "wire_volume_monthly": 50000,
        "transaction_count_monthly": 15
    }
)
```

### Parameters
- **transaction_data** (str): Raw transaction text containing customer identifiers
- **current_metrics** (Dict[str, float]): Dictionary of current activity metrics
- **customer_id** (Optional[str]): Explicit customer identifier override

### Returns
JSON string containing baseline comparison results with percentage deviations.

### Example Response
```json
{
  "resolved_key": "123-456-789",
  "resolution_source": "account_number",
  "has_baseline": true,
  "metrics": {
    "wire_volume_monthly": {
      "current": 50000,
      "customer_baseline": 25000,
      "peer_baseline": 30000,
      "delta_vs_customer_pct": 100.0,
      "delta_vs_peer_pct": 66.67
    }
  }
}
```

## Crew Configuration

### Agents
- **transaction_analyst**: Analyzes suspicious patterns with BaselineComparatorTool
- **regulatory_researcher**: Researches regulations with BraveSearchTool
- **narrative_drafter**: Drafts SAR narratives (no external tools)
- **quality_reviewer**: Performs QA review (no external tools)

### Tasks
- **analyze_transactions**: Pattern analysis and baseline comparison
- **research_regulations**: Regulatory compliance research
- **draft_sar_narrative**: SAR narrative creation
- **review_sar_quality**: Quality assurance review

### Input Schema
```json
{
  "transaction_data": "string - Transaction details with account info",
  "customer_profile": "string - Customer background and history", 
  "alert_details": "string - Alert information and metrics",
  "activity_type": "string - Type of suspicious activity"
}
```

### Output Files
- `{account_number}_transaction_analysis.md`
- `{account_number}_regulations.md`
- `{account_number}_sar_narrative.md`
- `{account_number}_sar_quality_review.md`