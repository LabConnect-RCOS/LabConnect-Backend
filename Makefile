init:
	pip3 install -r requirements.txt

clean:
	pystarter clean

run: 
	gunicorn run:app -w 6 --preload --max-requests-jitter 300

develop:
	python3 run.py

test: 
	python3 -m pytest --cov --cov-report=html:coverage_report
