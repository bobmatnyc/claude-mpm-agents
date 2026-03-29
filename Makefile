.PHONY: test

test:
	uv run python -m pytest tests/ -v
