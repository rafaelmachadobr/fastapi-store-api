shell:
	@poetry shell

run:
	@uvicorn src.store.main:app --reload --host 0.0.0.0 --port 8000

precommit-install:
	@poetry run pre-commit install

test:
	@poetry run pytest

test-matching:
	@poetry run pytest -s -rx -k $(K) --pdb store ./tests/
