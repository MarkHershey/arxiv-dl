REMOVE = rm -rvf

all:
	python3 -m pip install -U pip build twine && python3 -m build
clean:
	$(REMOVE) build
	$(REMOVE) logs
	$(REMOVE) dist
	$(REMOVE) arxiv_dl.egg-info
	$(REMOVE) ./**/__pycache__
	$(REMOVE) ./*/**/__pycache__
	$(REMOVE) tmp/*
	$(REMOVE) .pytest_cache
	$(REMOVE) .DS_Store
publish:
	python3 -m twine upload dist/*
testpublish:
	python3 -m twine upload --repository testpypi dist/*