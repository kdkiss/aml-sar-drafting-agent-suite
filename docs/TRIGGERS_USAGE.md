# Using Triggers with AML SAR Drafting Agent Suite

This guide explains how to use CrewAI triggers to automatically run your SAR drafting crew based on real-time events.

## What are Triggers?

Triggers enable you to automatically run your CrewAI deployments when specific events occur in your connected integrations, creating powerful event-driven workflows that respond to real-time changes in your business systems.

## Key Concepts

### Trigger Payload

All @start() methods in your flows will accept an additional parameter called crewai_trigger_payload. CrewAI automatically injects this payload into tasks by appending it to the first task's description by default.

### Integration Types

Your SAR crew can be triggered by various systems:
- **AML Monitoring Systems**: Automatic alerts from transaction monitoring platforms
- **Email**: Incoming emails with alert notifications (Gmail, Outlook)
- **Webhooks**: Direct API calls from internal compliance systems
- **Cloud Storage**: New files uploaded (OneDrive, Google Drive)
- **Ticketing Systems**: New cases in JIRA, ServiceNow, etc.

## Local Testing

### Method 1: Command Line with JSON String

```bash
# Pass trigger payload as JSON string
python main.py run_with_trigger '{
  "trigger_source": "AML_System",
  "transaction_data": "...",
  "customer_profile": "...",
  "alert_details": "...",
  "activity_type": "Structuring"
}'
```

### Method 2: Command Line with JSON File

```bash
# Pass trigger payload from file using @ prefix
python main.py run_with_trigger @trigger_payload.json
```

### Method 3: CrewAI CLI (Recommended for Testing)

The CrewAI CLI provides powerful commands to help you develop and test trigger-driven automations without deploying to production.

```bash
# List available triggers
crewai triggers list

# Test with realistic trigger payload
crewai triggers run <trigger_name>
```

**Important:** Using crewai run will NOT simulate trigger calls and won't pass the trigger payload. Use crewai triggers run to simulate trigger execution during development.

## Production Deployment

### Step 1: Connect Integration

1. Navigate to your deployment in the CrewAI dashboard
2. Go to **Tools & Integrations**
3. Connect your desired integration (e.g., Gmail, webhook endpoint)
4. Complete OAuth or API key authentication

### Step 2: Enable Trigger

1. Go to the **Triggers** tab in your deployment
2. Find your integration trigger
3. Toggle it to **Enabled** (blue)

### Step 3: Configure Environment Variables

Ensure all required variables are set:
```bash
export OPENAI_API_KEY="your-key"
export CREWAI_PLATFORM_INTEGRATION_TOKEN="your-token"
# Add any integration-specific tokens
```

### Step 4: Handle Trigger Payload in Tasks

Your crew's first task will automatically receive the trigger payload. You can control this behavior:

```python
@task
def analyze_transactions(self) -> Task:
    return Task(
        config=self.tasks_config['analyze_transactions'],
        allow_crewai_trigger_context=True  # Explicitly enable trigger context
    )
```

## Trigger Payload Structure

### Standard Fields

Every trigger payload includes:
```json
{
  "crewai_trigger_payload": {
    "trigger_source": "source_system",
    "trigger_time": "ISO 8601 timestamp",
    "trigger_type": "event_type"
  }
}
```

### SAR-Specific Fields

For AML SAR drafting, ensure your payload includes:
```json
{
  "transaction_data": "string",
  "customer_profile": "string", 
  "alert_details": "string",
  "activity_type": "string",
  "metadata": {
    "priority": "high|medium|low",
    "case_number": "string",
    "assigned_to": "string"
  }
}
```

## Example: Webhook Trigger

### 1. Set up webhook endpoint in CrewAI
- Get your webhook URL from the CrewAI dashboard
- Configure authentication (API key or shared secret)

### 2. Send POST request to trigger

```bash
curl -X POST https://api.crewai.com/v1/crews/<crew_id>/trigger \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d @trigger_payload.json
```

### 3. Monitor execution

- Check execution logs in CrewAI dashboard
- View outputs in the **Executions** tab
- Set up alerts for failures

## Example: Email Trigger

### Gmail Integration

1. **Connect Gmail** in Tools & Integrations
2. **Enable Gmail trigger** in Triggers tab
3. **Configure filter**: Set up rules (e.g., subject contains "AML Alert")
4. **Map email data** to payload fields

When an email arrives matching your filter:
```json
{
  "trigger_source": "gmail",
  "trigger_type": "email_received",
  "email": {
    "from": "aml-system@bank.com",
    "subject": "High Risk Alert - Structuring",
    "body": "Alert details...",
    "attachments": []
  }
}
```

Your crew would need to parse the email body to extract the required fields.

## Troubleshooting

### Trigger Not Firing

Verify the trigger is enabled in your deployment's Triggers tab, check integration connection status under Tools & Integrations, and ensure all required environment variables are properly configured.

### Payload Structure Issues

Use crewai triggers run to test locally and see the exact payload structure. Always test with crewai triggers run before deploying to see the complete payload.

### Execution Failures

Check the execution logs for error details and verify your crew can handle the crewai_trigger_payload parameter.

## Best Practices

1. **Test Locally First**: Always use `crewai triggers run` to test before production
2. **Validate Payload**: Check that all required fields are present in the trigger payload
3. **Error Handling**: Implement robust error handling in your tasks
4. **Monitor Executions**: Set up alerts for failed executions
5. **Document Payload Structure**: Maintain clear documentation of expected payload format
6. **Use Structured Data**: When possible, use JSON or structured formats rather than plain text
7. **Add Metadata**: Include tracking fields (case_number, priority, timestamps) for auditing

## Security Considerations

- **Authenticate Triggers**: Always use API keys or OAuth for production triggers
- **Validate Input**: Sanitize and validate all trigger payload data
- **Encrypt Sensitive Data**: Ensure PII and transaction data are encrypted in transit
- **Audit Logs**: Maintain comprehensive logs of all triggered executions
- **Access Control**: Restrict who can trigger your crew in production

## Sample Workflow

```
1. AML Monitoring System detects suspicious activity
   ↓
2. System generates alert and sends webhook to CrewAI
   ↓
3. CrewAI trigger fires and starts your SAR crew
   ↓
4. Transaction Analyst analyzes the data
   ↓
5. Regulatory Researcher finds applicable regulations
   ↓
6. Narrative Drafter creates SAR
   ↓
7. Quality Reviewer validates output
   ↓
8. Final SAR saved to output/sar_quality_review.md
   ↓
9. Notification sent back to compliance team
```

## Additional Resources

- [CrewAI Trigger Documentation](https://docs.crewai.com/en/enterprise/guides/automation-triggers)
- [CrewAI Trigger Payload Samples](https://github.com/crewAIInc/enterprise-trigger-payload-samples)
- [Integration Playbooks](https://docs.crewai.com/en/enterprise/guides/automation-triggers#integration-playbooks)