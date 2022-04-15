run_api:
	uvicorn src.order:app --reload
run_client:
	streamlit run src/monitor.py