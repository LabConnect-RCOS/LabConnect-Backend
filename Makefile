init:
	python3 -m pip install -r requirements.txt

clean:
	pystarter clean

run: 
	gunicorn run:app -w 6 --preload --max-requests-jitter 300

develop:
	python3 run.py

test: drop create
	python3 -m pytest --cov --cov-report=html:coverage_report

drop:
	python3 db_init.py clear

create:
	python3 db_init.py create
