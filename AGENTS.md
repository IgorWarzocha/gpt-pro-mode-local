# Agent Guidelines

## Commands
- Install: `pip install -r requirements.txt`
- Run: `uvicorn main:app --host 0.0.0.0 --port 8000`
- Test: `curl -X POST http://localhost:8000/pro-mode -H "Content-Type: application/json" -d '{"prompt":"test","num_gens":2}'`

## Code Style
- Use type hints consistently (typing module)
- Follow FastAPI/Pydantic patterns for API models
- Use descriptive function names with underscores
- Handle exceptions with HTTPException for API errors
- Use concurrent.futures for parallel processing
- Constants in UPPER_SNAKE_CASE at module level
- Private functions start with underscore