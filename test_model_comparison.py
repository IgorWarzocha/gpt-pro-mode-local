#!/usr/bin/env python3
"""
Test script to compare standard vs pro-mode responses from the local model.
"""

import subprocess
import json
import time
from typing import Dict, Any

def curl_request(prompt: str, system_prompt: str = None) -> Dict[str, Any]:
    """Make a curl request to LM Studio and return the response."""
    
    # Build messages array
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    # Build the curl command
    curl_data = {
        "model": "qwen3-4b-instruct-2507",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }
    
    curl_cmd = [
        "curl", "-s", 
        "http://localhost:1234/api/v0/chat/completions",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(curl_data)
    ]
    
    # Execute curl command
    result = subprocess.run(curl_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Curl failed: {result.stderr}")
    
    try:
        response = json.loads(result.stdout)
        return response
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON response: {e}\nResponse: {result.stdout}")

def test_standard_vs_promode():
    """Compare standard single response vs pro-mode synthesized response."""
    
    prompt = "What is the meaning of life?"
    system_prompt = "You are a deep thinker. Provide thoughtful, philosophical answers."
    
    print("=" * 60)
    print("MODEL COMPARISON TEST")
    print("=" * 60)
    print(f"Prompt: {prompt}")
    print(f"System Prompt: {system_prompt}")
    print()
    
    # Storage for results
    results = {
        "prompt": prompt,
        "system_prompt": system_prompt,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model": "qwen3-4b-instruct-2507"
    }
    
    # Test 1: Standard single response
    print("1. STANDARD SINGLE RESPONSE")
    print("-" * 40)
    start_time = time.time()
    
    try:
        standard_response = curl_request(prompt, system_prompt)
        
        # Extract content and stats
        content = standard_response["choices"][0]["message"]["content"]
        stats = standard_response.get("stats", {})
        tokens_per_sec = stats.get("tokens_per_second", 0)
        ttft = stats.get("time_to_first_token", 0)
        gen_time = stats.get("generation_time", 0)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        results["standard_response"] = {
            "content": content,
            "stats": stats,
            "total_time": total_time,
            "tokens_per_sec": tokens_per_sec,
            "ttft": ttft,
            "generation_time": gen_time
        }
        
        print(f"Response Time: {total_time:.2f}s")
        print(f"Tokens/sec: {tokens_per_sec:.1f}")
        print(f"TTFT: {ttft:.3f}s")
        print(f"Generation Time: {gen_time:.3f}s")
        print()
        print("RESPONSE:")
        print("-" * 20)
        print(content)
        
    except Exception as e:
        print(f"Error with standard response: {e}")
        return
    
    print()
    print()
    
    # Test 2: Pro-mode response
    print("2. PRO-MODE SYNTHESIZED RESPONSE")
    print("-" * 40)
    start_time = time.time()
    
    try:
        # Import and run pro-mode
        from local_pro_mode import LocalProMode
        
        pro_mode = LocalProMode(model_name="qwen3-4b-instruct-2507")
        pro_mode_result = pro_mode.run(prompt, n_runs=5)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        results["pro_mode_response"] = {
            "final": pro_mode_result["final"],
            "candidates": pro_mode_result["candidates"],
            "total_time": total_time,
            "num_candidates": 5
        }
        
        print(f"Total Time: {total_time:.2f}s")
        print(f"Number of Candidates: 5")
        print()
        print("FINAL SYNTHESIZED RESPONSE:")
        print("-" * 30)
        print(pro_mode_result["final"])
        
        print()
        print("CANDIDATE RESPONSES:")
        print("-" * 20)
        for i, candidate in enumerate(pro_mode_result["candidates"], 1):
            if candidate and candidate.strip():
                print(f"\nCandidate {i}:")
                print("-" * 12)
                print(candidate[:500] + "..." if len(candidate) > 500 else candidate)
        
    except Exception as e:
        print(f"Error with pro-mode response: {e}")
        return
    
    print()
    print("=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    print("Standard Response: Single generation, faster, one perspective")
    print("Pro-Mode Response: Multiple generations + synthesis, slower, more comprehensive")
    print("Pro-Mode advantages:")
    print("- Multiple perspectives on the question")
    print("- Synthesis combines strengths of different approaches")
    print("- Generally more thoughtful and comprehensive answers")
    print("- Reduces randomness through consensus")
    
    # Save results to markdown file
    save_results_to_markdown(results)
    
    print(f"\nResults saved to: model_comparison_results.md")

def save_results_to_markdown(results: dict):
    """Save test results to a markdown file."""
    
    timestamp = results["timestamp"]
    prompt = results["prompt"]
    system_prompt = results["system_prompt"]
    model = results["model"]
    
    markdown_content = f"""# Model Comparison Results

**Timestamp:** {timestamp}  
**Model:** {model}  
**Prompt:** {prompt}  
**System Prompt:** {system_prompt}  

---

## 1. Standard Single Response

**Response Time:** {results['standard_response']['total_time']:.2f}s  
**Tokens/sec:** {results['standard_response']['tokens_per_sec']:.1f}  
**TTFT:** {results['standard_response']['ttft']:.3f}s  
**Generation Time:** {results['standard_response']['generation_time']:.3f}s  

### Response:

{results['standard_response']['content']}

---

## 2. Pro-Mode Synthesized Response

**Total Time:** {results['pro_mode_response']['total_time']:.2f}s  
**Number of Candidates:** {results['pro_mode_response']['num_candidates']}  

### Final Synthesized Response:

{results['pro_mode_response']['final']}

### Candidate Responses:

"""
    
    # Add candidate responses
    for i, candidate in enumerate(results['pro_mode_response']['candidates'], 1):
        if candidate and candidate.strip():
            markdown_content += f"""
#### Candidate {i}:

{candidate}

---
"""
    
    # Add comparison summary
    markdown_content += """
## Comparison Summary

### Standard Response
- **Approach:** Single generation
- **Speed:** Faster ({:.2f}s)
- **Perspective:** One viewpoint
- **Use Case:** Quick answers, simple queries

### Pro-Mode Response  
- **Approach:** Multiple generations + synthesis
- **Speed:** Slower ({:.2f}s)
- **Perspective:** Multiple viewpoints combined
- **Use Case:** Complex questions, comprehensive analysis

### Key Differences
- **Pro-Mode** generates {} different perspectives on the same question
- **Pro-Mode** synthesizes the best elements from all candidates
- **Pro-Mode** generally produces more thoughtful and comprehensive answers
- **Pro-Mode** reduces randomness through consensus approach
- **Standard** approach is {:.1f}x faster than Pro-Mode

### When to Use Each

**Use Standard Response when:**
- You need quick answers
- The question is simple/factual
- You're doing rapid prototyping
- Resources are limited

**Use Pro-Mode when:**
- The question is complex/philosophical
- You want comprehensive analysis
- Quality is more important than speed
- You want multiple perspectives synthesized
""".format(
    results['standard_response']['total_time'],
    results['pro_mode_response']['total_time'],
    results['pro_mode_response']['num_candidates'],
    results['pro_mode_response']['total_time'] / results['standard_response']['total_time']
)
    
    # Write to file
    with open("model_comparison_results.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)

if __name__ == "__main__":
    test_standard_vs_promode()
