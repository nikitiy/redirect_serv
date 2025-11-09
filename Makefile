# Redirect_serv Makefile

# Dependencies
install:
	poetry install --no-dev

dev-install:
	poetry install

# Code quality
lint:
	poetry run black --check src/
	poetry run isort --check-only src/

format:
	poetry run black src/
	poetry run isort src/

# Testing
test:
	poetry run pytest tests/ -v

test-cov:
	poetry run pytest tests/ -v --cov=src/redirect_serv --cov-report=html --cov-report=term

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/

# Quick start
run_server:
	uvicorn src.redirect_serv.main:app --reload
