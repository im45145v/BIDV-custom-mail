.PHONY: setup run test clean help

help:
	@echo "Available commands:"
	@echo "  make setup   - Create virtual environment and install dependencies"
	@echo "  make run     - Run the Streamlit app"
	@echo "  make test    - Run pytest tests"
	@echo "  make clean   - Remove cache and output files"

setup:
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@echo "Setup complete! Activate with: source venv/bin/activate"

run:
	./venv/bin/streamlit run app.py

test:
	./venv/bin/pytest -q tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf media/output/* 2>/dev/null || true
	rm -rf .pytest_cache 2>/dev/null || true
	@echo "Clean complete!"
