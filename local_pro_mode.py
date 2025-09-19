#!/usr/bin/env python3
"""
Local Pro Mode - Run pro-mode inference with local models via LM Studio.
Can be used as a CLI tool or imported as a module.
"""

import argparse
import sys
from typing import List, Dict, Any
import time
import concurrent.futures as cf
from openai import OpenAI

# Configuration
BASE_URL = "http://localhost:1234/api/v0"
MODEL = "qwen3-4b-thinking-2507"  # Replace with your loaded model name in LM Studio
MAX_COMPLETION_TOKENS = 30000


class LocalProMode:
    def __init__(self, model_name: str = None, base_url: str = None):
        """
        Initialize LocalProMode with custom model and base URL.
        
        Args:
            model_name: Name of the model loaded in LM Studio
            base_url: Base URL for LM Studio API (default: http://localhost:1234/v1)
        """
        self.model = model_name or MODEL
        self.base_url = base_url or BASE_URL
        self.client = self._make_client()
    
    def _make_client(self) -> OpenAI:
        """Create OpenAI client configured for LM Studio."""
        return OpenAI(
            base_url=self.base_url,
            api_key="not-needed"  # LM Studio doesn't require API key
        )
    
    def _one_completion(self, prompt: str, temperature: float) -> str:
        """Single completion with retry logic."""
        delay = 0.5
        for attempt in range(3):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=MAX_COMPLETION_TOKENS,
                    top_p=1,
                    stream=False,
                )
                # Print enhanced stats from v0 API
                if hasattr(resp, 'stats'):
                    stats = resp.stats
                    print(f"    Stats: {stats.get('tokens_per_second', 0):.1f} tokens/sec, "
                          f"TTFT: {stats.get('time_to_first_token', 0):.3f}s")
                return resp.choices[0].message.content
            except Exception as e:
                if attempt == 2:
                    raise
                print(f"Attempt {attempt + 1} failed, retrying... Error: {e}")
                time.sleep(delay)
                delay *= 2
        return ""
    
    def _build_synthesis_messages(self, candidates: List[str]) -> List[Dict[str, str]]:
        """Build messages for synthesis pass."""
        numbered = "\n\n".join(
            f"<cand {i+1}>\n{txt}\n</cand {i+1}>" for i, txt in enumerate(candidates)
        )
        system = (
            "You are an expert editor. Synthesize ONE best answer from the candidate "
            "answers provided, merging strengths, correcting errors, and removing repetition. "
            "Do not mention the candidates or the synthesis process. Be decisive and clear."
        )
        user = (
            f"You are given {len(candidates)} candidate answers delimited by <cand i> tags.\n\n"
            f"{numbered}\n\nReturn the single best final answer."
        )
        return [{"role": "system", "content": system},
                {"role": "user", "content": user}]
    
    def run(self, prompt: str, n_runs: int) -> Dict[str, Any]:
        """
        Run pro-mode: generate n_runs candidates and synthesize final answer.
        
        Args:
            prompt: The input prompt
            n_runs: Number of candidate generations
            
        Returns:
            Dict with "final" (synthesized answer) and "candidates" (list of candidates)
        """
        if n_runs < 1:
            raise ValueError("n_runs must be >= 1")
        
        print(f"Generating {n_runs} candidates...")
        
        # Parallel candidate generations
        max_workers = min(n_runs, 16)
        candidates: List[str] = [""] * n_runs
        
        with cf.ThreadPoolExecutor(max_workers=max_workers) as ex:
            fut_to_idx = {
                ex.submit(self._one_completion, prompt, 0.9): i
                for i in range(n_runs)
            }
            
            for fut in cf.as_completed(fut_to_idx):
                i = fut_to_idx[fut]
                try:
                    candidates[i] = fut.result()
                    print(f"  Candidate {i + 1}/{n_runs} completed")
                except Exception as e:
                    print(f"  Candidate {i + 1}/{n_runs} failed: {e}")
                    candidates[i] = ""
        
        # Filter out empty candidates
        filtered = [c for c in candidates if c and c.strip()]
        if not filtered:
            raise RuntimeError("All candidate generations failed.")
        
        print(f"Synthesizing {len(filtered)} candidates into final answer...")
        
        # Synthesis pass
        messages = self._build_synthesis_messages(filtered)
        final_resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
            max_tokens=MAX_COMPLETION_TOKENS,
            top_p=1,
            stream=False,
        )
        
        # Print enhanced stats for synthesis
        if hasattr(final_resp, 'stats'):
            stats = final_resp.stats
            print(f"Synthesis stats: {stats.get('tokens_per_second', 0):.1f} tokens/sec, "
                  f"TTFT: {stats.get('time_to_first_token', 0):.3f}s, "
                  f"Generation time: {stats.get('generation_time', 0):.3f}s")
        
        final = final_resp.choices[0].message.content
        
        return {"final": final, "candidates": candidates}


def main():
    """CLI interface for LocalProMode."""
    parser = argparse.ArgumentParser(
        description="Local Pro Mode - Generate and synthesize multiple responses using local models"
    )
    parser.add_argument(
        "prompt", 
        help="The prompt to process"
    )
    parser.add_argument(
        "-n", "--num-candidates", 
        type=int, 
        default=5,
        help="Number of candidate generations (default: 5)"
    )
    parser.add_argument(
        "-m", "--model", 
        default=MODEL,
        help=f"Model name in LM Studio (default: {MODEL})"
    )
    parser.add_argument(
        "-u", "--url", 
        default=BASE_URL,
        help=f"LM Studio base URL (default: {BASE_URL})"
    )
    parser.add_argument(
        "--show-candidates", 
        action="store_true",
        help="Show all candidate responses"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize pro-mode with custom settings
        pro_mode = LocalProMode(model_name=args.model, base_url=args.url)
        
        # Run pro-mode
        result = pro_mode.run(args.prompt, args.num_candidates)
        
        # Print results
        print("\n" + "="*50)
        print("FINAL SYNTHESIZED ANSWER:")
        print("="*50)
        print(result["final"])
        
        if args.show_candidates:
            print("\n" + "="*50)
            print("CANDIDATE RESPONSES:")
            print("="*50)
            for i, candidate in enumerate(result["candidates"], 1):
                if candidate and candidate.strip():
                    print(f"\n--- Candidate {i} ---")
                    print(candidate)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()