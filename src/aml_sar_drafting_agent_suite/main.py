#!/usr/bin/env python
import sys
import warnings
import os
import json
from datetime import datetime
from aml_sar_drafting_agent_suite.crew import AmlSarDraftingAgentSuite

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def load_inputs(input_file=None):
    """
    Load SAR input data from JSON file containing transaction data, customer profile,
    alert details, and activity type for analysis.
    
    Args:
        input_file: Optional path to input file, defaults to INPUT_FILE env var
        
    Returns:
        dict: Parsed JSON data with required SAR analysis inputs
        
    Raises:
        Exception: If file not found or JSON parsing fails
    """
    # Priority: parameter > environment variable > default fallback
    if input_file is None:
        input_file = os.getenv("INPUT_FILE", "example_input.json")
    
    try:
        with open(input_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception(f"Input file not found: {input_file}")
    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing JSON file: {e}")


def run():
    """
    Main execution function that runs the complete AML SAR analysis workflow.
    
    Process:
    1. Loads input data from configured JSON file
    2. Extracts account number for dynamic output file naming
    3. Executes the four-agent SAR analysis workflow
    4. Generates examination-ready SAR documentation
    
    Raises:
        Exception: If crew execution fails or input processing errors occur
    """
    # Load SAR analysis inputs from JSON file
    inputs = load_inputs()
    
    # Extract account number for dynamic output file naming (e.g., "123-456-789_sar_narrative.md")
    import re
    transaction_data = inputs.get('transaction_data', '')
    account_match = re.search(r'Account #([0-9\-]+)', transaction_data)
    account_number = account_match.group(1) if account_match else 'unknown'
    inputs['account_number'] = account_number
    
    try:
        # Execute the complete SAR analysis and drafting workflow
        AmlSarDraftingAgentSuite().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = load_inputs()
    
    try:
        AmlSarDraftingAgentSuite().crew().train(
            n_iterations=int(sys.argv[1]) if len(sys.argv) > 1 else 5,
            filename=sys.argv[2] if len(sys.argv) > 2 else "training_data.pkl",
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        task_id = sys.argv[1] if len(sys.argv) > 1 else os.getenv("TASK_ID")
        if not task_id:
            raise Exception("No task_id provided. Use: python main.py replay <task_id>")
        
        AmlSarDraftingAgentSuite().crew().replay(task_id=task_id)
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution with multiple iterations to evaluate performance and consistency.
    
    Args (via sys.argv):
        n_iterations: Number of test iterations (default: 3)
        openai_model_name: LLM model to use for testing (default: gpt-4o-mini)
        
    Returns:
        CrewOutput: Test results with performance metrics and outputs
        
    Raises:
        Exception: If testing fails or crew execution errors occur
    """
    inputs = load_inputs()
    
    try:
        # Run crew testing with configurable iterations and model
        result = AmlSarDraftingAgentSuite().crew().test(
            n_iterations=int(sys.argv[1]) if len(sys.argv) > 1 else 3,
            openai_model_name=sys.argv[2] if len(sys.argv) > 2 else "gpt-4o-mini",
            inputs=inputs
        )
        return result
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    """
    Execute SAR analysis workflow triggered by external events (webhooks, emails, etc.).
    
    This function enables enterprise integration by accepting trigger payloads from
    various sources and automatically processing suspicious activity alerts.
    
    Usage:
        1. From command line with JSON string:
           python main.py run_with_trigger '{"transaction_data": "...", ...}'
        
        2. From command line with JSON file:
           python main.py run_with_trigger @trigger_payload.json
        
        3. Test locally with CrewAI CLI:
           crewai triggers run <trigger_name>
           
    Returns:
        CrewOutput: SAR analysis results with timestamp and trigger metadata
    """
    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")
    
    payload_arg = sys.argv[1]
    
    try:
        # Check if argument is a file reference (starts with @)
        if payload_arg.startswith('@'):
            file_path = payload_arg[1:]
            with open(file_path, 'r') as f:
                trigger_payload = json.load(f)
        else:
            trigger_payload = json.loads(payload_arg)
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")
    except FileNotFoundError:
        raise Exception(f"Trigger payload file not found: {payload_arg[1:]}")
    
    # Transform trigger payload into standardized SAR analysis inputs
    # Supports triggers from AML monitoring systems, email alerts, webhooks, etc.
    inputs = {
        "crewai_trigger_payload": trigger_payload,  # Preserve original trigger data
        "transaction_data": trigger_payload.get("transaction_data", ""),
        "customer_profile": trigger_payload.get("customer_profile", ""),
        "alert_details": trigger_payload.get("alert_details", ""),
        "activity_type": trigger_payload.get("activity_type", "")
    }
    
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    
    try:
        print(f"\n{'='*80}")
        print("RUNNING WITH TRIGGER PAYLOAD")
        print(f"{'='*80}\n")
        print(f"Trigger source: {trigger_payload.get('trigger_source', 'Unknown')}")
        print(f"Trigger time: {trigger_payload.get('trigger_time', 'Unknown')}\n")
        
        result = AmlSarDraftingAgentSuite().crew().kickoff(inputs=inputs)
        
        # Save comprehensive trigger execution results for audit trail
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output/trigger_result_{timestamp}.txt"
        with open(output_file, 'w') as f:
            # Create detailed execution log with trigger metadata
            f.write(f"{'='*80}\n")
            f.write("TRIGGER-DRIVEN SAR EXECUTION\n")
            f.write(f"Executed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*80}\n\n")
            f.write("TRIGGER PAYLOAD:\n")
            f.write(json.dumps(trigger_payload, indent=2))
            f.write("\n\n")
            f.write(f"{'='*80}\n")
            f.write("SAR ANALYSIS RESULT:\n")
            f.write(f"{'='*80}\n\n")
            f.write(result.raw)
        
        print(f"\n✅ Trigger result saved to: {output_file}")
        return result
        
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")