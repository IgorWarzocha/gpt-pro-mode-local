# GPT Pro Mode - Local Edition

[![Twitter Follow](https://img.shields.io/twitter/follow/mattshumer_?style=social)](https://x.com/mattshumer_)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**A local version of Matt Shumer's GPT Pro Mode that runs entirely on your machine using LM Studio.**

## 🌟 What is Pro Mode?

Pro Mode enhances AI responses by:
1. **Generating multiple candidate responses** in parallel (typically 3-7)
2. **Synthesizing the best answer** by combining strengths from all candidates
3. **Producing higher-quality, more comprehensive responses** than single-generation approaches

## 🚀 Quick Start

### Prerequisites

1. **Install LM Studio**: Download from [lmstudio.ai](https://lmstudio.ai/)
2. **Load a Model**: Open LM Studio, search and download your preferred model (e.g., Llama 3.2, Mistral, Qwen3)
3. **Start Server**: Go to the "Server" tab in LM Studio and click "Start Server"
4. **Check Model Name**: Note the exact model name displayed in the Server tab

### Installation

```bash
# Clone this repository
git clone https://github.com/IgorWarzocha/gpt-pro-mode-local.git
cd gpt-pro-mode-local

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### As a CLI Tool

```bash
# Basic usage
python local_pro_mode.py "Explain quantum computing" -n 5

# With custom model
python local_pro_mode.py "What is machine learning?" -n 7 -m "qwen3-4b-thinking-2507"

# Show all candidates
python local_pro_mode.py "Write a poem about AI" -n 3 --show-candidates

# Custom LM Studio URL
python local_pro_mode.py "Hello world" -n 3 -u "http://localhost:1234/api/v0"
```

#### As a Python Module

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

#### Compare Standard vs Pro-Mode

```bash
# Run comparison test
python test_model_comparison.py

# This will create model_comparison_results.md with detailed analysis
```

## 📊 Performance Comparison

| Aspect | Standard Response | Pro-Mode Response |
|--------|------------------|-------------------|
| **Speed** | ~2-5 seconds | ~15-60 seconds |
| **Quality** | Single perspective | Multiple synthesized perspectives |
| **Depth** | Basic coverage | Comprehensive analysis |
| **Consistency** | Variable | High (consensus-based) |
| **Use Case** | Quick answers | Complex/important questions |

## 🔧 Configuration

### Default Settings
- **Base URL**: `http://localhost:1234/api/v0`
- **Default Model**: `qwen3-4b-thinking-2507`
- **Max Tokens**: 30,000
- **Max Workers**: 16 (for parallel generation)

### Environment Variables
```bash
# Optional: Set default model
export DEFAULT_MODEL="your-preferred-model"

# Optional: Set custom LM Studio URL
export LM_STUDIO_URL="http://localhost:1234/api/v0"
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Prompt Input  │───▶│  Candidate Gen  │───▶│   Synthesis    │
└─────────────────┘    │ (Parallel, n=5) │    │   Process      │
                       └─────────────────┘    └─────────────────┘
                              │                       │
                              ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │ Candidate 1-5  │    │ Final Answer   │
                       └─────────────────┘    └─────────────────┘
```

### Key Components

1. **LocalProMode Class**: Main interface for pro-mode functionality
2. **Parallel Generation**: Uses ThreadPoolExecutor for concurrent candidate generation
3. **Enhanced LM Studio API**: Leverages v0 REST API for detailed stats
4. **Synthesis Engine**: Combines multiple responses into one optimal answer

## 📈 Enhanced Features

### LM Studio v0 API Integration
- **Performance Stats**: Tokens/sec, Time To First Token (TTFT), generation time
- **Model Information**: Architecture, quantization, context length
- **Runtime Details**: Backend engine, version, supported formats

### Smart Synthesis
- **Multi-perspective Analysis**: Combines different viewpoints
- **Error Correction**: Identifies and fixes inconsistencies
- **Redundancy Removal**: Eliminates repetitive content
- **Strength Merging**: Preserves the best elements from each candidate

## 🧪 Testing & Validation

### Run Tests
```bash
# Basic functionality test
python local_pro_mode.py "Test prompt" -n 3

# Performance comparison
python test_model_comparison.py

# Example usage patterns
python example_usage.py
```

### Expected Output
```
Generating 3 candidates...
    Stats: 84.7 tokens/sec, TTFT: 0.023s
  Candidate 1/3 completed
    Stats: 83.4 tokens/sec, TTFT: 0.016s
  Candidate 2/3 completed
    Stats: 82.7 tokens/sec, TTFT: 0.016s
  Candidate 3/3 completed
Synthesizing 3 candidates into final answer...
Synthesis stats: 94.0 tokens/sec, TTFT: 0.138s, Generation time: 11.666s

==================================================
FINAL SYNTHESIZED ANSWER:
==================================================
[Your synthesized response here...]
```

## 🔍 Troubleshooting

### Common Issues

**Connection Errors**
```bash
# Check if LM Studio is running
curl http://localhost:1234/api/v0/models

# If this fails, start LM Studio server
```

**Model Not Found**
```bash
# List available models
curl http://localhost:1234/api/v0/models

# Use exact model name from the list
python local_pro_mode.py "prompt" -m "exact-model-name"
```

**Memory Issues**
```bash
# Reduce number of candidates
python local_pro_mode.py "prompt" -n 3  # Instead of 5 or 7
```

**Slow Performance**
```bash
# Check model stats
curl http://localhost:1234/api/v0/models | jq '.data[] | select(.state=="loaded")'

# Consider using a smaller model for faster inference
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Fork the repository
git clone https://github.com/YOUR_USERNAME/gpt-pro-mode-local.git
cd gpt-pro-mode-local

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If exists
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Matt Shumer** for creating the original Pro Mode concept
- **LM Studio** for providing excellent local inference tools
- **OpenAI** for the API compatibility standards

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/IgorWarzocha/gpt-pro-mode-local/issues)
- **Email**: igorwarzocha@gmail.com
- **Discussions**: [GitHub Discussions](https://github.com/IgorWarzocha/gpt-pro-mode-local/discussions)

## 🗺️ Roadmap

- [ ] Support for multiple local backends (Ollama, vLLM, etc.)
- [ ] Web interface for easier usage
- [ ] Batch processing capabilities
- [ ] Performance optimization and caching
- [ ] Advanced synthesis strategies
- [ ] Model-specific tuning profiles

---

**Made with ❤️ by Igor Warzocha and contributors**