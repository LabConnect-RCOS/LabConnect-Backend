init:
	pip3 install -r requirements.txt

run:
	gunicorn run:app -w 6 --preload --max-requests-jitter 300

develop:
	python3 run.py

test: clean
	python -m pytest --cov --cov-report=html:coverage_report
