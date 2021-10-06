REMOVE = rm -rvf

all:
	python setup.py sdist bdist_wheel
clean:
	$(REMOVE) build
	$(REMOVE) logs
	$(REMOVE) dist
	$(REMOVE) arxiv_dl.egg-info
	$(REMOVE) ./**/__pycache__
publish:
	python -m twine upload dist/*
