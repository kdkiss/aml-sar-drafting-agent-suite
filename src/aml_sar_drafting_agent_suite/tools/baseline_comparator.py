# tools/baseline_comparator.py
import re
import json
import pathlib
from typing import Optional, Dict
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

BASE_PATH = pathlib.Path("data/baselines.json")


class BaselineComparatorInput(BaseModel):
    transaction_data: str = Field(..., description="Raw transaction text that includes account number or business name")
    current_metrics: Dict[str, float] = Field(..., description="e.g. {'cash_deposits_monthly': 24889, 'wire_volume_monthly': 184500}")
    customer_id: Optional[str] = Field(None, description="Override if already known; otherwise extracted")


class BaselineComparatorTool(BaseTool):
    """
    Custom CrewAI tool for comparing customer transaction metrics against historical 
    and peer baselines to identify suspicious deviations.
    
    This tool is essential for quantifying suspicious activity by calculating percentage
    deviations from normal behavior patterns, supporting regulatory SAR requirements.
    """
    name: str = "behavioral_baseline_comparator"
    description: str = (
        "Compares current activity metrics to historical and peer baselines. "
        "Resolves identity via explicit customer_id, or Account #, or Business Name fallback."
    )
    args_schema: type = BaselineComparatorInput

    def _extract_account_number(self, text: str) -> Optional[str]:
        """Extract account number from transaction data using regex pattern."""
        m = re.search(r'Account\s*#\s*([0-9\-]+)', text, re.IGNORECASE)
        return m.group(1).strip() if m else None

    def _extract_business_name(self, text: str) -> Optional[str]:
        """Extract business name from transaction data for baseline lookup."""
        # Primary pattern: "Business Name: Company LLC"
        m = re.search(r'Business\s*Name:\s*(.+)', text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        # Fallback pattern: Look for LLC in customer line
        m2 = re.search(r'([A-Za-z0-9&\-,\. ]+LLC)', text)
        return m2.group(1).strip() if m2 else None

    def _load_baseline(self, key: str) -> Dict:
        """Load baseline data from JSON file for the specified customer key."""
        if not BASE_PATH.exists():
            return {}
        with open(BASE_PATH, "r") as f:
            data = json.load(f)
        return data.get(key, {})

    def _pct(self, cur: float, base: Optional[float]) -> Optional[float]:
        """Calculate percentage change from baseline, handling zero/null cases."""
        if base is None or base == 0:
            return None
        return round(((cur - base) / base) * 100, 2)

    def _run(self, transaction_data: str, current_metrics: Dict[str, float], customer_id: Optional[str] = None) -> str:
        """
        Main execution method that compares current metrics against baselines.
        
        Args:
            transaction_data: Raw transaction text containing customer identifiers
            current_metrics: Dictionary of current activity metrics (e.g., wire_volume_monthly)
            customer_id: Optional explicit customer identifier
            
        Returns:
            JSON string containing baseline comparison results with percentage deviations
        """
        # Resolve baseline key priority: explicit → acct# → business name
        cust_id = customer_id or self._extract_account_number(transaction_data)
        if not cust_id:
            cust_id = self._extract_business_name(transaction_data)

        baseline_entry = self._load_baseline(cust_id) if cust_id else {}

        cust_base = baseline_entry.get("customer_baseline", {})
        peer_base = baseline_entry.get("peer_baseline", {})

        result = {
            "resolved_key": cust_id,
            "resolution_source": (
                "explicit" if customer_id else
                "account_number" if self._extract_account_number(transaction_data) else
                "business_name" if cust_id else
                "none"
            ),
            "has_baseline": bool(baseline_entry),
            "metrics": {}
        }

        for metric, current_val in current_metrics.items():
            cb = cust_base.get(metric)
            pb = peer_base.get(metric)
            result["metrics"][metric] = {
                "current": current_val,
                "customer_baseline": cb,
                "peer_baseline": pb,
                "delta_vs_customer_pct": self._pct(current_val, cb),
                "delta_vs_peer_pct": self._pct(current_val, pb)
            }

        return json.dumps(result, ensure_ascii=False, indent=2)
