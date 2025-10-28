# Example Scenarios

This document provides detailed examples of the different SAR types supported by the AML SAR Drafting Agent Suite.

## Available Examples

### 1. Structuring / CTR Avoidance
**File**: `data/example_input.json`
**Scenario**: Maria Rodriguez making cash deposits just below $10,000 threshold
**Key Indicators**:
- 12 deposits totaling $112,000 over 45 days
- All deposits between $8,800-$9,800
- 301% increase from customer baseline
- Immediate wire transfers to international recipients

### 2. Trade-Based Money Laundering (TBML)
**File**: `data/trade_based_laundering_example.json`
**Scenario**: Global Trade Solutions Inc with pricing and documentation anomalies
**Key Indicators**:
- $15.5M wire volume (180% above baseline)
- Invoice amounts 15-20% higher than wire transfers
- Shipping weights inconsistent with electronics
- Multiple invoices with same container numbers
- Unit prices 40-60% below market rates

### 3. Layering / Complex Money Movement
**File**: `data/layering_example.json`
**Scenario**: Robert Thompson rapidly moving funds through multiple jurisdictions
**Key Indicators**:
- $1.59M total volume in 45 days (10x stated income)
- 26 transactions across 15+ high-risk jurisdictions
- Same-day or next-day fund transfers
- Minimal fund retention (<48 hours average)
- New account with immediate high activity

### 4. Check Kiting / Check Fraud
**File**: `data/check_kiting_example.json`
**Scenario**: Jennifer Walsh exploiting float across multiple banks
**Key Indicators**:
- $451,000 in check deposits, $449,000 in withdrawals
- 67% check return rate ($290,000 returned)
- Same-day withdrawals before 2 PM cutoff
- Coordinated across 4 different banks
- 5913% increase from customer baseline

### 5. Elder Financial Abuse
**File**: `data/elder_fraud_example.json`
**Scenario**: Dorothy Miller (86) victimized by multiple scam types
**Key Indicators**:
- $152,150 in international wire transfers
- 85% account depletion in 45 days
- Multiple scam typologies (tech support, romance, lottery)
- 13 high-risk countries involved
- Customer confusion and family concerns

## Running Examples

```bash
# Set the example you want to run
export INPUT_FILE=data/trade_based_laundering_example.json

# Run the analysis
uv run aml_sar_drafting_agent_suite

# Or use the CLI command
crewai run
```

## Expected Outputs

Each example generates four output files:
1. **Transaction Analysis**: Detailed pattern analysis with baseline comparisons
2. **Regulatory Research**: Applicable BSA/AML rules and guidance
3. **SAR Narrative**: Examination-ready narrative with five essential elements
4. **Quality Review**: QA assessment with pass/fail determination

## Baseline Data

The `data/baselines.json` file contains historical and peer baseline data for all examples, enabling the BaselineComparatorTool to calculate meaningful percentage deviations for suspicious activity quantification.