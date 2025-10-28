# Environment Setup Guide

This guide explains how to configure your environment variables for the AML SAR Drafting Agent Suite.

## Quick Start

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your values:**
   ```bash
   nano .env
   # or
   vim .env
   # or use your favorite editor
   ```

3. **Load environment variables:**
   
   The CrewAI framework automatically loads `.env` files, but you can also manually load them:
   
   ```bash
   # Linux/Mac
   export $(cat .env | xargs)
   
   # Or use python-dotenv
   pip install python-dotenv
   ```

## Required Variables

### OPENAI_API_KEY
**Required for all operations**

Your OpenAI API key for running the agents.

```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

Get your API key from: https://platform.openai.com/api-keys

### INPUT_FILE
**Required for run, train, and test commands**

Path to the JSON file containing your SAR case data.

```bash
INPUT_FILE=example_input.json
```

**Default:** `example_input.json`

**Examples:**
```bash
# Use example data
INPUT_FILE=example_input.json

# Use custom case file
INPUT_FILE=cases/case_2024_001.json

# Use absolute path
INPUT_FILE=/path/to/your/case_data.json
```

## Optional Variables

### OPENAI_MODEL_NAME
Model to use for testing.

```bash
OPENAI_MODEL_NAME=gpt-4o-mini
```

**Default:** `gpt-4o-mini`

**Options:**
- `gpt-4o-mini` (fast, cost-effective)
- `gpt-4o` (more capable)
- `gpt-4-turbo` (balanced)

### TRAIN_ITERATIONS
Number of iterations for training mode.

```bash
TRAIN_ITERATIONS=5
```

**Default:** `5`

### TRAIN_FILENAME
Output file for training data.

```bash
TRAIN_FILENAME=training_data.pkl
```

**Default:** `training_data.pkl`

### TEST_ITERATIONS
Number of iterations for testing mode.

```bash
TEST_ITERATIONS=3
```

**Default:** `3`

### TASK_ID
Task ID for replay functionality.

```bash
TASK_ID=task_abc123xyz
```

**Default:** None (must be provided for replay)

### CREWAI_PLATFORM_INTEGRATION_TOKEN
Required for CrewAI Enterprise features and triggers.

```bash
CREWAI_PLATFORM_INTEGRATION_TOKEN=your_token_here
```

Get your token from: https://app.crewai.com/settings

### OUTPUT_DIR
Custom output directory for results.

```bash
OUTPUT_DIR=output
```

**Default:** `output`

## Usage Examples

### Example 1: Basic Usage with Default Input

```bash
# .env file
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
INPUT_FILE=example_input.json
```

```bash
python main.py run
```

### Example 2: Multiple Case Files

Create different input files for different cases:

```bash
# .env for Case 1
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
INPUT_FILE=cases/structuring_case.json

# .env for Case 2
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
INPUT_FILE=cases/layering_case.json
```

Or override at runtime:

```bash
INPUT_FILE=cases/structuring_case.json python main.py run
```

### Example 3: Testing Configuration

```bash
# .env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
INPUT_FILE=example_input.json
TEST_ITERATIONS=5
OPENAI_MODEL_NAME=gpt-4o
```

```bash
python main.py test
```

### Example 4: Training Mode

```bash
# .env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
INPUT_FILE=example_input.json
TRAIN_ITERATIONS=10
TRAIN_FILENAME=sar_training.pkl
```

```bash
python main.py train
```

## Loading Environment Variables in Python

If you need to manually load environment variables in your code:

```python
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access variables
api_key = os.getenv("OPENAI_API_KEY")
input_file = os.getenv("INPUT_FILE", "example_input.json")
```

## Security Best Practices

### 1. Never Commit .env Files

Add to `.gitignore`:

```bash
# .gitignore
.env
.env.local
.env.*.local
*.pkl
output/
```

### 2. Use Different .env Files for Different Environments

```bash
.env.development
.env.staging
.env.production
```

Load specific environment:

```bash
# Development
ln -s .env.development .env

# Production
ln -s .env.production .env
```

### 3. Rotate API Keys Regularly

- Change your OpenAI API key periodically
- Use separate keys for development and production
- Monitor API usage for anomalies

### 4. Restrict File Permissions

```bash
chmod 600 .env
```

This ensures only you can read the file.

## Troubleshooting

### "Input file not found" Error

**Problem:** The INPUT_FILE path is incorrect or file doesn't exist.

**Solution:**
```bash
# Check current directory
pwd

# Verify file exists
ls -la example_input.json

# Use absolute path if needed
INPUT_FILE=/full/path/to/example_input.json
```

### "Invalid JSON" Error

**Problem:** The JSON file has syntax errors.

**Solution:**
```bash
# Validate JSON
python -m json.tool example_input.json

# Or use jq
jq . example_input.json
```

### Environment Variables Not Loading

**Problem:** Variables set in .env are not being recognized.

**Solution:**
```bash
# Manually export variables (Linux/Mac)
export $(cat .env | xargs)

# Or source the file
set -a
source .env
set +a

# Install python-dotenv if using Python directly
pip install python-dotenv
```

### API Key Issues

**Problem:** OpenAI API authentication fails.

**Solution:**
```bash
# Verify key format (should start with sk-proj- or sk-)
echo $OPENAI_API_KEY

# Test key with curl
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Generate new key at platform.openai.com if needed
```

## Example Complete Setup

```bash
# 1. Clone repository
git clone <your-repo>
cd aml-sar-drafting-agent-suite

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env

# 4. Edit .env with your credentials
nano .env

# 5. Verify configuration
cat .env

# 6. Run the crew
python main.py run

# 7. Check output
ls -la output/
```

## Reference: All Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | None | OpenAI API key |
| `INPUT_FILE` | Yes | `example_input.json` | Path to input JSON file |
| `OPENAI_MODEL_NAME` | No | `gpt-4o-mini` | Model for testing |
| `TRAIN_ITERATIONS` | No | `5` | Training iterations |
| `TRAIN_FILENAME` | No | `training_data.pkl` | Training output file |
| `TEST_ITERATIONS` | No | `3` | Test iterations |
| `TASK_ID` | No | None | Task ID for replay |
| `CREWAI_PLATFORM_INTEGRATION_TOKEN` | No* | None | CrewAI Enterprise token |
| `OUTPUT_DIR` | No | `output` | Output directory |

\* Required only for Enterprise features and triggers