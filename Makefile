init:
	pip3 install -r requirements.txt

clean:
	pystarter clean

run: clean
	gunicorn run:app -w 6 --preload --max-requests-jitter 300

develop: clean
	python run.py

test: clean
	python -m pytest --cov