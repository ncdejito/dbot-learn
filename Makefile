run_api:
	uvicorn src.order:app --reload
run_client:
	streamlit run src/monitor.py
test:
	pytest --cov=src tests/
	rm assets/coverage.svg
	coverage-badge -o assets/coverage.svg