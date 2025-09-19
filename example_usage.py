#!/usr/bin/env python3
"""
Example usage of LocalProMode as a Python module.
"""

from local_pro_mode import LocalProMode

def main():
    # Initialize with your model name
    pro_mode = LocalProMode(model_name="llama-3.2-3b-instruct")  # Replace with your model
    
    # Example 1: Simple usage
    prompt = "Explain quantum computing in simple terms."
    result = pro_mode.run(prompt, n_runs=3)
    
    print("=== FINAL ANSWER ===")
    print(result["final"])
    
    # Example 2: Technical question with more candidates
    prompt2 = "What are the main differences between REST and GraphQL APIs?"
    result2 = pro_mode.run(prompt2, n_runs=7)
    
    print("\n=== FINAL ANSWER 2 ===")
    print(result2["final"])
    
    # Example 3: Creative writing
    prompt3 = "Write a short story about a robot discovering emotions."
    result3 = pro_mode.run(prompt3, n_runs=5)
    
    print("\n=== FINAL ANSWER 3 ===")
    print(result3["final"])

if __name__ == "__main__":
    main()