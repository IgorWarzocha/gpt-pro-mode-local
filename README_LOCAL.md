# Local Pro Mode

Run the pro-mode framework with your local models via LM Studio.

## Installation

```bash
pip install openai
```

## Setup

1. **Install LM Studio**: Download from https://lmstudio.ai/
2. **Load a Model**: Open LM Studio, search and download a model
3. **Start Server**: Go to the "Server" tab and click "Start Server"
4. **Check Model Name**: Note the exact model name displayed in the Server tab

## Usage

### As a CLI Tool

```bash
# Basic usage
python local_pro_mode.py "Explain quantum computing" -n 5

# With custom model
python local_pro_mode.py "What is machine learning?" -n 7 -m "llama-3.2-3b-instruct"

# Show all candidates
python local_pro_mode.py "Write a poem about AI" -n 3 --show-candidates

# Custom LM Studio URL
python local_pro_mode.py "Hello world" -n 3 -u "http://localhost:1234/v1"
```

### As a Python Module

```python
from local_pro_mode import LocalProMode

# Initialize
pro_mode = LocalProMode(model_name="your-model-name")

# Run pro-mode
result = pro_mode.run("Your prompt here", n_runs=5)

# Get results
print(result["final"])  # Synthesized answer
print(result["candidates"])  # All candidate responses
```

## Configuration

- **Default URL**: `http://localhost:1234/v1`
- **Default Model**: `your-model-name` (change this in the code or via CLI)
- **Max Tokens**: 30,000
- **Max Workers**: 16 (for parallel generation)

## How It Works

1. **Parallel Generation**: Generates `n_runs` candidate responses in parallel
2. **Synthesis**: Combines all candidates into a single, improved response
3. **Local Inference**: Uses your local LM Studio instance instead of cloud APIs

## Troubleshooting

- **Connection Errors**: Ensure LM Studio server is running on port 1234
- **Model Not Found**: Check the exact model name in LM Studio's Server tab
- **Memory Issues**: Reduce the number of candidates (`-n` flag)
- **Slow Performance**: Adjust `max_workers` in the code or use fewer candidates

## Examples

See `example_usage.py` for more detailed examples of using LocalProMode as a module.